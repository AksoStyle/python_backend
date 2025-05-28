from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from models import vehicle as vehicle_model
from schemas import vehicle as vehicle_schema
from crud import vehicle as vehicle_crud
from database import engine
from database import SessionLocal
from typing import List
from schemas.vehicle import SuggestionResponse, VehicleSuggestion


vehicle_model.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    print("Opening DB session")
    db = SessionLocal()
    try:
        yield db
    finally:
        print("Closing DB session")
        db.close()


@app.post("/vehicles/", response_model=vehicle_schema.VehicleRead)
def add_vehicle(vehicle: vehicle_schema.VehicleCreate, db: Session = Depends(get_db)):
    return vehicle_crud.create_vehicle(db=db, vehicle=vehicle)


@app.get("/vehicles", response_model=list[vehicle_schema.VehicleRead])
def get_vehicles(db: Session = Depends(get_db)):
    return vehicle_crud.read_vehicles(db=db)


@app.get("/suggestions/", response_model=vehicle_schema.SuggestionResponse)
def suggest_vehicle_assignments(
    passengers: int = Query(..., gt=0),
    distance: float = Query(..., gt=0),
    db: Session = Depends(get_db)
):
    vehicles = vehicle_crud.read_vehicles(db=db)
    raw_suggestions = vehicle_crud.generate_suggestions(passengers, distance, vehicles)
    enriched = vehicle_crud.enrich_suggestions(distance, raw_suggestions, vehicles)
    return {"suggestions": enriched}
