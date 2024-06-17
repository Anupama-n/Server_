from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Employee(Base): 
    __tablename__ = "employee"
    username = Column(String, primary_key=True, index=True)
    password = Column(String)

class Vehicle(Base):
    __tablename__ = "Vehicle_info"
    vehicle_id = Column(Integer, primary_key=True, index=True)
    vehicle_type = Column(String, nullable=False)
    entry_time = Column(TIMESTAMP, nullable=False)
    predicted_number_plate = Column(String, nullable=False, unique=True)
    actual_number_plate = Column(String)
    exit_time = Column(TIMESTAMP, nullable=True)
    parking_fees = Column(Integer, nullable=False)
    parking_slot = relationship("ParkingSlots", back_populates="vehicle")


class ParkingSlots(Base):
    __tablename__ = "Parking_slots"
    slot_id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey('Vehicle_info.vehicle_id'), index=True, nullable=True)
    slot_type = Column(String, nullable=False)
    vehicle = relationship("Vehicle", back_populates="parking_slot")