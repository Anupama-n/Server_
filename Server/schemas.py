from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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
    entry_time: datetime
    predicted_number_plate: str
    actual_number_plate: str
    exit_time: Optional[datetime] = None
    parking_fees: Optional[int] = 0


    class Config:
        orm_mode = True


class CreateParkingSlots(BaseModel):
    slot_id: int
    slot_type: str
    vehicle_id: Optional[int] = None

    class Config:
        orm_mode = True