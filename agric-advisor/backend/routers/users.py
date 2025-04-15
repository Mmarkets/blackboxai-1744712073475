from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated, List

from config.dependencies import get_db
from models.user import User
from schemas.user import UserCreate, UserResponse
from utils.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)
from utils.roles import require_admin
from typing import Optional

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    # Check if user already exists
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate role if provided
    if hasattr(user_data, 'role') and user_data.role not in ["farmer", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role specified"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        role=user_data.role if hasattr(user_data, 'role') else "farmer"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Admin-only endpoint to list all users"""
    return db.query(User).all()

@router.patch(
    "/{user_id}/role", 
    response_model=UserResponse,
    responses={
        403: {"description": "Forbidden - Admin privileges required"},
        400: {"description": "Bad Request - Invalid role specified"},
        404: {"description": "Not Found - User not found"}
    }
)
async def update_user_role(
    user_id: int,
    new_role: str = Body(..., description="New role (either 'farmer' or 'admin')"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Update a user's role (Admin only)
    
    - **user_id**: ID of user to update
    - **new_role**: Must be either 'farmer' or 'admin'
    - **Returns**: Updated user object
    """
    if new_role not in ["farmer", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role specified"
        )
    
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db_user.role = new_role
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/farmers", response_model=List[UserResponse])
async def get_farmers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all farmers (accessible to all authenticated users)"""
    return db.query(User).filter(User.role == "farmer").all()

@router.post("/login")
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    # Authenticate user
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_current_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
