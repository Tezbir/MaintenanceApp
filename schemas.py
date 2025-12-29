from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

class UserCreate(BaseModel):
    user_name: Optional[str] = None
    user_email: EmailStr
    user_password: str  # plaintext coming in (we hash it)

class UserOut(BaseModel):
    user_id: int
    user_name: Optional[str]
    user_email: EmailStr
    user_creation_date: datetime

    class Config:
        from_attributes = True

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class VeeCreate(BaseModel):
    vee_name: Optional[str] = None
    vee_year: Optional[int] = None
    vee_make: Optional[str] = None
    vee_model: Optional[str] = None
    vee_vin: Optional[str] = None
    vee_mileage: int = 0

class VeeOut(BaseModel):
    vee_id: int
    user_id: int
    vee_name: Optional[str]
    vee_year: Optional[int]
    vee_make: Optional[str]
    vee_model: Optional[str]
    vee_vin: Optional[str]
    vee_mileage: int
    vee_stamped: datetime

    class Config:
        from_attributes = True


class ServiceTypeOut(BaseModel):
    service_type_id: int
    service_type_name: Optional[str]
    service_type_default_interval_miles: Optional[int]
    service_type_default_interval_days: Optional[int]

    class Config:
        from_attributes = True


class ServiceRecordCreate(BaseModel):
    vee_id: int
    service_type_id: int
    service_record_date: date
    service_record_mileage: int
    service_record_cost: Optional[Decimal] = None
    service_record_notes: Optional[str] = None

class ServiceRecordOut(BaseModel):
    service_record_id: int
    vee_id: int
    service_type_id: int
    service_record_date: date
    service_record_mileage: int
    service_record_cost: Optional[Decimal]
    service_record_notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
