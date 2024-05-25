from pydantic import BaseModel
from datetime import datetime

class EmployeeCreate(BaseModel):
    username: str
    password: str

class EmployeeResponse(BaseModel):
    username: str

    class Config:
        orm_mode = True

class CreateVehicle(BaseModel):
    vehicle_id: int
    vehicle_type: str
    predicted_number_plate: str
    actual_number_plate: str

    class Config:
        orm_mode = True

class CreateParkingSlots(BaseModel):
    slot_id: int
    vehicle_id: int
    slot_type: str

    class Config:
        orm_mode = True

class CreateParkingFees(BaseModel):
    parking_fee_id: int
    vehicle_id: int
    entry_time: datetime
    exit_time: datetime
    parking_fees: int

    class Config:
        orm_mode = True
