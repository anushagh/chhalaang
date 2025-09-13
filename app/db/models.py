from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from .database import Base
from datetime import datetime
from .mixins import TimestampMixin

class Driver(Base, TimestampMixin):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Earnings(Base, TimestampMixin):
    __tablename__ = "earnings"
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, index=True)
    amount = Column(Float)
    expenses = Column(Float)
    date = Column(Date)

class Trip(Base, TimestampMixin):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, index=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    status = Column(String)
