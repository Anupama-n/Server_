from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from datetime import datetime
import models
import schemas
from database import get_db_vehicle
from login import verify_token  
from typing import List, Optional
from pytz import timezone

router = APIRouter()

def calculate_parking_fees(entry_time: datetime, exit_time: Optional[datetime], vehicle_type: str) -> int:
    """Calculates parking fees based on entry and exit times and vehicle type."""
    entry_time = entry_time.astimezone(timezone("UTC"))
    if exit_time:
        exit_time = exit_time.astimezone(timezone("UTC"))
        parking_duration = exit_time - entry_time
        parking_hours = parking_duration.total_seconds() // 3600 + (1 if parking_duration.total_seconds() % 3600 > 0 else 0)  # round up to the next full hour

        if vehicle_type.lower() == "2 wheeler":
            hourly_rate = 20
        elif vehicle_type.lower() == "4 wheeler":
            hourly_rate = 40
        else:
            raise HTTPException(status_code=400, detail="Invalid vehicle type")
        
        parking_fees = int(parking_hours) * hourly_rate
        return parking_fees
    else:
        return 0

@router.post("/vehicles/", response_model=schemas.CreateVehicle)
def create_vehicle(vehicle: schemas.CreateVehicle, db: Session = Depends(get_db_vehicle), token: dict = Depends(verify_token)):
    """Creates a new vehicle entry in the database. Only accessible to logged-in users."""
    print("Received vehicle data:", vehicle)
    parking_fees = calculate_parking_fees(vehicle.entry_time, vehicle.exit_time, vehicle.vehicle_type)
    
    new_vehicle = models.Vehicle(
        vehicle_id=vehicle.vehicle_id,
        vehicle_type=vehicle.vehicle_type,
        entry_time=vehicle.entry_time,
        predicted_number_plate=vehicle.predicted_number_plate,
        actual_number_plate=vehicle.actual_number_plate,
        exit_time=vehicle.exit_time,
        parking_fees=parking_fees
    )
    db.add(new_vehicle)
    db.commit()
    print("Transaction committed successfully")
    db.refresh(new_vehicle)

    if vehicle.exit_time is None:
        parking_slot = db.query(models.ParkingSlots).filter_by(vehicle_id=None).first()
        if parking_slot:
            parking_slot.vehicle_id = new_vehicle.vehicle_id
            db.commit()

    return new_vehicle

@router.put("/vehicles/{actual_number_plate}/exit", response_model=schemas.CreateVehicle)
def update_exit_time(actual_number_plate: str, exit_time: datetime, db: Session = Depends(get_db_vehicle), token: dict = Depends(verify_token)):
    """Updates the exit time of a vehicle. Only accessible to logged-in users."""
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.actual_number_plate == actual_number_plate).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    vehicle.exit_time = exit_time
    vehicle.parking_fees = calculate_parking_fees(vehicle.entry_time, vehicle.exit_time, vehicle.vehicle_type)
    db.commit()
    db.refresh(vehicle)

    parking_slot = db.query(models.ParkingSlots).filter_by(vehicle_id=vehicle.vehicle_id).first()
    if parking_slot:
        parking_slot.vehicle_id = None
        db.commit()

    return vehicle

@router.post("/parking_slots/", response_model=schemas.CreateParkingSlots)
def create_parking_slot(slot: schemas.CreateParkingSlots, db: Session = Depends(get_db_vehicle), token: dict = Depends(verify_token)):
    """Creates a new parking slot entry in the database. Only accessible to logged-in users."""
    new_slot = models.ParkingSlots(
        slot_id=slot.slot_id,
        vehicle_id=None, 
        slot_type=slot.slot_type
    )
    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)
    return new_slot


@router.get("/parking-slots/available", response_model=List[schemas.CreateParkingSlots])
def get_available_parking_slots(db: Session = Depends(get_db_vehicle)):
    """Fetches available parking slots."""
    available_slots = db.query(models.ParkingSlots).filter(models.ParkingSlots.vehicle_id == None).all()

    if not available_slots:
        raise HTTPException(status_code=404, detail="No available parking slots")

    return available_slots

@router.put("/parking_slots/{slot_id}/park_vehicle/{vehicle_id}")
def park_vehicle(slot_id: int, vehicle_id: int, db: Session = Depends(get_db_vehicle), token: dict = Depends(verify_token)):
    """Parks a vehicle in a specified parking slot. Only accessible to logged-in users."""
    slot = db.query(models.ParkingSlots).filter(models.ParkingSlots.slot_id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Parking slot not found")
    
    slot.vehicle_id = vehicle_id
    db.commit()

    return {"message": f"Vehicle {vehicle_id} parked in slot {slot_id}"}


@router.get("/vehicles/{actual_number_plate}", response_model=schemas.CreateVehicle)
def get_vehicle_details(actual_number_plate: str, db: Session = Depends(get_db_vehicle)):
    """Fetches vehicle details based on actual_number_plate."""
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.actual_number_plate == actual_number_plate).first()
    
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    vehicle_details = {
        "vehicle_id": vehicle.vehicle_id,
        "vehicle_type": vehicle.vehicle_type,
        "entry_time": vehicle.entry_time,
        "predicted_number_plate": vehicle.predicted_number_plate,
        "actual_number_plate": vehicle.actual_number_plate,
        "exit_time": vehicle.exit_time,
        "parking_fees": vehicle.parking_fees,
    }
    
                
            

    return vehicle_details

@router.get("/parking-slots/{actual_number_plate}", response_model=List[schemas.CreateParkingSlots])
def get_parking_slots(actual_number_plate: str, db: Session = Depends(get_db_vehicle)):
    """Fetches parking slots of a vehicle based on actual_number_plate."""
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.actual_number_plate == actual_number_plate).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    parking_slots = db.query(models.ParkingSlots).filter(models.ParkingSlots.vehicle_id == vehicle.vehicle_id).all()

    if parking_slots:
        return parking_slots
  
    raise HTTPException(status_code=404, detail="Parking slots not found for the vehicle")