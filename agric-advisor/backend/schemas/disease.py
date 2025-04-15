from pydantic import BaseModel
from typing import Optional

class DiseaseBase(BaseModel):
    name: str
    description: Optional[str] = None
    symptoms: str
    treatment: str

class DiseaseCreate(DiseaseBase):
    pass

class DiseaseResponse(DiseaseBase):
    id: int

    class Config:
        from_attributes = True
