from db import db
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, DECIMAL, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

class Room(db.Model):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    room_number = Column(String(50), unique=True, nullable=False)
    type = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False)
    price_per_night = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(50), nullable=False)
    amenities = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reservations = relationship('Reservation', backref='room')

class Customer(db.Model):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reservations = relationship('Reservation', backref='customer')

class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    check_in_date = Column(Date, nullable=False)
    check_out_date = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)
    total_cost = Column(DECIMAL(10, 2), nullable=False)
    special_requests = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Employee(db.Model):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    role = Column(String(50), nullable=False)
    department = Column(String(50), nullable=False)
    salary = Column(DECIMAL(10, 2), nullable=False)
    hire_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True)
    reservation_id = Column(Integer, ForeignKey('reservations.id'), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_status = Column(String(50), nullable=False)
    payment_date = Column(Date, nullable=True)
    payment_method = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reservation = relationship('Reservation', backref='invoices')