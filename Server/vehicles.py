from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
import models
import schemas
from database import *

router = APIRouter()

@router.post("/vehicles/", response_model=schemas.CreateVehicle)
def create_vehicle(vehicle: schemas.CreateVehicle, db: Session = Depends(get_db_vehicle)):
    new_vehicle = models.Vehicle(
        vehicle_id=vehicle.vehicle_id,
        vehicle_type=vehicle.vehicle_type,
        predicted_number_plate=vehicle.predicted_number_plate,
        actual_number_plate=vehicle.actual_number_plate
    )
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle

@router.post("/parking_slots/", response_model=schemas.CreateParkingSlots)
def create_parking_slot(slot: schemas.CreateParkingSlots, db: Session = Depends(get_db_vehicle)):
    new_slot = models.ParkingSlots(
        slot_id=slot.slot_id,
        vehicle_id=slot.vehicle_id,
        slot_type=slot.slot_type
    )
    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)
    return new_slot

@router.post("/parking_fees/", response_model=schemas.CreateParkingFees)
def create_parking_fee(fee: schemas.CreateParkingFees, db: Session = Depends(get_db_vehicle)):
    new_fee = models.ParkingFees(
        parking_fee_id=fee.parking_fee_id,
        vehicle_id=fee.vehicle_id,
        entry_time=fee.entry_time,
        exit_time=fee.exit_time,
        parking_fees=fee.parking_fees
    )
    db.add(new_fee)
    db.commit()
    db.refresh(new_fee)
    return new_fee