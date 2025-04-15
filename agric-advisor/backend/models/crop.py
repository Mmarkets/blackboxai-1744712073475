from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from config.database import Base

class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    ideal_climate = Column(String)
    planting_season = Column(String)
    growth_duration = Column(String)
    water_requirements = Column(String)
    diseases = relationship("Disease", back_populates="affected_crop")

    def __repr__(self):
        return f"<Crop(id={self.id}, name={self.name})>"
