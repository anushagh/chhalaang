# app/db/seed.py
from .database import SessionLocal, Base, engine
from . import models
from sqlalchemy.orm import Session
from datetime import date, datetime


# Create tables (if not exists)
Base.metadata.create_all(bind=engine)

# Start a DB session
db: Session = SessionLocal()

try:
    # --- Seed Drivers ---
    drivers_data = [
        {"name": "Jamie User"},
        {"name": "John Doe"},
        {"name": "Jane Smith"},
    ]

    for d in drivers_data:
        existing = db.query(models.Driver).filter_by(name=d["name"]).first()
        if not existing:
            driver = models.Driver(name=d["name"])
            db.add(driver)
    db.commit()
    print("✅ Drivers seeded")

    # Fetch drivers for Earnings/Trips
    drivers = db.query(models.Driver).all()

    # --- Seed Earnings ---
    for driver in drivers:
        existing = db.query(models.Earnings).filter_by(driver_id=driver.id, date=date.today()).first()
        if not existing:
            earning = models.Earnings(
                driver_id=driver.id,
                amount=1000.0,
                expenses=200.0,
                date=date.today()
            )
            db.add(earning)
    db.commit()
    print("✅ Earnings seeded")

    # --- Seed Trips ---
    for driver in drivers:
        existing = db.query(models.Trip).filter_by(driver_id=driver.id, status="completed").first()
        if not existing:
            trip = models.Trip(
                driver_id=driver.id,
                status="completed",
                start_time=datetime.now(),
                end_time=datetime.now()
            )
            db.add(trip)
    db.commit()
    print("✅ Trips seeded")

finally:
    db.close()