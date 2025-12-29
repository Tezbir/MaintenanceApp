from sqlalchemy import (
    Column, BigInteger, String, DateTime, ForeignKey, Integer, SmallInteger,
    Text, Date, DECIMAL, UniqueConstraint, func
)
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_name = Column(String (100), nullable=True)
    user_email = Column(String(100), nullable=False, unique=True, index=True)
    user_password = Column(String(255), nullable=False)
    user_creation_date = Column(DateTime, server_default=func.current_timestamp())

    vees = relationship("Vee", back_populates="user", cascade="all, delete-orphan")


class Vee(Base):
    __tablename__ = "vee"
    __table_args__ = (
        UniqueConstraint("user_id", "vee_vin", name="uq_user_vin"),
    )

    vee_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)

    vee_name = Column(String(100), nullable=True)
    vee_year = Column(SmallInteger, nullable=True)
    vee_make = Column(String(100), nullable=True)
    vee_model = Column(String(100), nullable=True)
    vee_vin = Column(String(17), nullable=True)
    vee_mileage = Column(Integer, nullable=False, server_default="0")
    vee_stamped = Column(DateTime, server_default=func.current_timestamp())

    user = relationship("User", back_populates="vees")
    service_records = relationship("ServiceRecord", back_populates="vee", cascade="all, delete-orphan")


class ServiceType(Base):
    __tablename__ = "service_type"

    service_type_id = Column(BigInteger, primary_key=True, autoincrement=True)
    service_type_name = Column(String(100), unique=True, nullable=True)
    service_type_default_interval_miles = Column(Integer, nullable=True)
    service_type_default_interval_days = Column(Integer, nullable=True)
    service_type_created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())


class ServiceRecord(Base):
    __tablename__ = "service_record"

    service_record_id = Column(BigInteger, primary_key=True, autoincrement=True)

    vee_id = Column(BigInteger, ForeignKey("vee.vee_id", ondelete="CASCADE"), nullable=False, index=True)
    service_type_id = Column(BigInteger, ForeignKey("service_type.service_type_id", ondelete="RESTRICT"), nullable=False, index=True)

    service_record_date = Column(Date, nullable=False)
    service_record_mileage = Column(Integer, nullable=False)
    service_record_cost = Column(DECIMAL(10, 2), nullable=True)
    service_record_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    vee = relationship("Vee", back_populates="service_records")
