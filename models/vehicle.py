from sqlalchemy import Column, Integer, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

from database import Base  # To use the same base model.


class FuelType(enum.Enum):
    gasoline = "gasoline"
    mildHybrid = "mildHybrid"
    pureElectric = "pureElectric"


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    passengerCapacity = Column(Integer, nullable=False)
    range = Column(Integer, nullable=False)
    Fuel = Column(Enum(FuelType), nullable=False)
