from pydantic import BaseModel
from typing import Optional

class CropBase(BaseModel):
    name: str
    description: Optional[str] = None
    growth_period: int
    water_requirements: str

class CropCreate(CropBase):
    pass

class CropResponse(CropBase):
    id: int

    class Config:
        from_attributes = True
