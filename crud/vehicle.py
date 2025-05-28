from sqlalchemy.orm import Session
from models.vehicle import Vehicle, FuelType
from schemas.vehicle import VehicleCreate
from itertools import combinations
from typing import List


def create_vehicle(db: Session, vehicle: VehicleCreate):
    db_vehicle = Vehicle(
        passengerCapacity=vehicle.passengerCapacity,
        range=vehicle.range,
        Fuel=vehicle.fuelType,
    )
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


def read_vehicles(db: Session):
    return db.query(Vehicle).all()


def calculate_trip_time_minutes(distance_km: float):
    if distance_km <= 50:
        return distance_km * 2
    return 50 * 2 + (distance_km - 50)


def calculate_profit(distance_km: float, vehicle_combination: List[Vehicle]):
    # Revenue: €2/km/customer + €2/half-hour/customer
    trip_time = calculate_trip_time_minutes(distance_km)
    time_blocks = int((trip_time + 29) // 30)  # Round up to nearest 30 mins
    revenue = (2 * distance_km + 2 * time_blocks)

    # Refueling cost: €2/km for gasoline, €1/km for others
    cost = 0
    for v in vehicle_combination:
        if v.Fuel == FuelType.gasoline:
            cost += 2 * distance_km
        else:
            cost += 1 * distance_km

    return revenue - cost


def generate_suggestions(passengers: int, distance: float, vehicles: List[Vehicle]):
    suggestions = []

    for r in range(1, len(vehicles) + 1):
        for combo in combinations(vehicles, r):
            total_capacity = sum(v.passengerCapacity for v in combo)
            if total_capacity >= passengers and all(v.range >= distance for v in combo):
                profit = calculate_profit(distance, combo)
                suggestions.append({
                    "vehicle_ids": [v.id for v in combo],
                    "total_capacity": total_capacity,
                    "profit": round(profit, 2)
                })

    # Sort suggestions by profit (descending)
    suggestions.sort(key=lambda x: x["profit"], reverse=True)
    return suggestions


def enrich_suggestions(distance: float, suggestions: List[dict], all_vehicles: List[Vehicle]):
    enriched = {}
    for suggestion in suggestions:
        trip_time = calculate_trip_time_minutes(distance)
        time_blocks = int((trip_time + 29) // 30)
        travel_fee = (2 * distance + 2 * time_blocks)

        for vid in suggestion["vehicle_ids"]:
            v = next((veh for veh in all_vehicles if veh.id == vid), None)
            if not v:
                continue

            # Avoid duplicates
            if v.id in enriched:
                continue

            if v.Fuel == FuelType.gasoline:
                refuel_cost = 2 * distance
            else:
                refuel_cost = 1 * distance

            profit = travel_fee + refuel_cost

            enriched[v.id] = {
                "id": v.id,
                "passengerCapacity": v.passengerCapacity,
                "range": v.range,
                "fuel": v.Fuel,
                "profit": round(profit, 2),
                "travel_fee": round(travel_fee, 2),
                "refueling_fee": round(refuel_cost, 2),
            }

    return list(enriched.values())
