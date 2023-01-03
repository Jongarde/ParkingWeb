from pydantic import BaseModel
from typing import Optional

class Owner(BaseModel):
    dni: str
    name: str
    handicap: bool

class Vehicle(BaseModel):
    registration: str
    brand: str
    model: str
    dni_owner: str

class ParkingLot(BaseModel):
    id: int
    registration_vehicle: Optional[str]
    period: Optional[float]

class Incidence(BaseModel):
    id: int
    registration_vehicle: str
    text: str

class Reservation(BaseModel):
    registration_plate: str
    id_parkingLot: int
    start_reservation: int
    end_reservation: int