
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


class DoctorBase(BaseModel):
    full_name: str
    specialization: str
    phone: str
    email: EmailStr
    is_available: bool = True


class DoctorCreate(DoctorBase):
    pass


class DoctorCreateWithUser(DoctorBase):
    username: str
    password: str


class DoctorUpdate(BaseModel):
    full_name: Optional[str] = None
    specialization: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_available: Optional[bool] = None


class DoctorResponse(DoctorBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)