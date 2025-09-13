
from pydantic import BaseModel
from typing import Optional, List

# ---------- Driver ----------
class DriverBase(BaseModel):
    name: str

class DriverCreate(DriverBase):
    pass

class Driver(DriverBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Earnings ----------
class EarningsBase(BaseModel):
    amount: float
    driver_id: int

class EarningsCreate(EarningsBase):
    pass

class Earnings(EarningsBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Trip ----------
class TripBase(BaseModel):
    destination: str
    driver_id: int

class TripCreate(TripBase):
    pass

class Trip(TripBase):
    id: int

    class Config:
        from_attributes = True
