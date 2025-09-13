from sqlalchemy.orm import Session
from . import models, schemas

# --- Drivers ---
def create_driver(db: Session, driver: schemas.DriverCreate):
    db_driver = models.Driver(name=driver.name)
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver

def get_driver(db: Session, driver_id: int):
    return db.query(models.Driver).filter(models.Driver.id == driver_id).first()

# --- Earnings ---
def create_earnings(db: Session, earnings: schemas.EarningsCreate):
    db_earnings = models.Earnings(**earnings.dict())
    db.add(db_earnings)
    db.commit()
    db.refresh(db_earnings)
    return db_earnings

def get_earnings_by_driver(db: Session, driver_id: int):
    return db.query(models.Earnings).filter(models.Earnings.driver_id == driver_id).all()

# --- Trips ---
def create_trip(db: Session, trip: schemas.TripCreate):
    db_trip = models.Trip(**trip.dict())
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip

def get_trips_by_driver(db: Session, driver_id: int):
    return db.query(models.Trip).filter(models.Trip.driver_id == driver_id).all()
