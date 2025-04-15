from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, List

from config.dependencies import get_db
from models.crop import Crop
from schemas.crop import CropCreate, CropResponse
from utils.auth import get_current_user
from utils.roles import require_farmer
from models.user import User

router = APIRouter(prefix="/crops", tags=["crops"])

@router.get("/", response_model=List[CropResponse])
async def get_crops(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    return db.query(Crop).all()

@router.post("/", response_model=CropResponse)
async def create_crop(
    crop: CropCreate,
    current_user: Annotated[User, Depends(require_farmer)],
    db: Session = Depends(get_db)
):
    db_crop = Crop(**crop.dict())
    db.add(db_crop)
    db.commit()
    db.refresh(db_crop)
    return db_crop
