from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    symptoms = Column(Text)
    prevention = Column(Text)
    treatment = Column(Text)
    affected_crop_id = Column(Integer, ForeignKey("crops.id"))
    
    affected_crop = relationship("Crop", back_populates="diseases")

    def __repr__(self):
        return f"<Disease(id={self.id}, name={self.name})>"
