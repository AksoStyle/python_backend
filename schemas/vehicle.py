from pydantic import BaseModel
from enum import Enum
from typing import List


class FuelType(str, Enum):
    gasoline = "gasoline"
    mildHybrid = "mildHybrid"
    pureElectric = "pureElectric"


class VehicleCreate(BaseModel):
    passengerCapacity: int
    range: float
    fuelType: FuelType


class VehicleRead(BaseModel):
    id: int
    passengerCapacity: int
    range: int
    Fuel: FuelType

    class Config:
        from_attributes = True


class VehicleSuggestion(BaseModel):
    id: int
    passengerCapacity: int
    range: float
    fuel: FuelType
    profit: float
    travel_fee: float
    refueling_fee: float

    class Config:
        from_attributes = True


class SuggestionResponse(BaseModel):
    suggestions: List[VehicleSuggestion]
