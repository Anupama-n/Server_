from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from database import Base
from passlib.context import CryptContext

class Employee(Base): 
    __tablename__ = "employee"
    username = Column(String, primary_key= True, index = True)
    password = Column (String)

class Vehicle(Base):
    __tablename__ = "Vehicle_info"
    vehicle_id = Column(Integer, primary_key=True, index=True)
    vehicle_type = Column(String, nullable=False)  # Add this column
    predicted_number_plate = Column(String, nullable=False)
    actual_number_plate = Column(String, nullable=False)


class ParkingSlots(Base):
    __tablename__= "Parking_slots"
    slot_id = Column(Integer, primary_key=True, index=True)
    vehicle_id =Column(Integer, ForeignKey('Vehicle_info.vehicle_id'), index=True)
    slot_type= Column(String, nullable=False)

class ParkingFees(Base):
    __tablename__ = "Parking_fees"
    parking_fee_id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey('Vehicle_info.vehicle_id'), index=True)
    entry_time = Column(TIMESTAMP)
    exit_time = Column(TIMESTAMP)
    parking_fees = Column(Integer)



