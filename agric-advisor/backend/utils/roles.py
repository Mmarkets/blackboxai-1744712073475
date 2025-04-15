from fastapi import HTTPException, status, Depends
from models.user import User
from utils.auth import get_current_user

async def require_admin(current_user: User = Depends(get_current_user)):
    """Verify the current user has admin role"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

async def require_farmer(current_user: User = Depends(get_current_user)):
    """Verify the current user has farmer role"""
    if current_user.role != "farmer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Farmer account required"
        )
    return current_user
