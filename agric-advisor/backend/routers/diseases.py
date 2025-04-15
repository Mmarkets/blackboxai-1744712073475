from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, List

from config.dependencies import get_db
from models.disease import Disease
from schemas.disease import DiseaseCreate, DiseaseResponse
from utils.auth import get_current_user
from utils.roles import require_farmer
from models.user import User

router = APIRouter(prefix="/diseases", tags=["diseases"])

@router.get("/", response_model=List[DiseaseResponse])
async def get_diseases(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    return db.query(Disease).all()

@router.post("/", response_model=DiseaseResponse)
async def create_disease(
    disease: DiseaseCreate,
    current_user: Annotated[User, Depends(require_farmer)],
    db: Session = Depends(get_db)
):
    db_disease = Disease(**disease.dict())
    db.add(db_disease)
    db.commit()
    db.refresh(db_disease)
    return db_disease
