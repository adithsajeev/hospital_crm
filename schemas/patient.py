from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: str
    gender: str
    date_of_birth: date
    address: Optional[str] = None

class PatientResponse(PatientCreate):
    id: int

    class Config:
        from_attributes = True