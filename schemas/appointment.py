from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from schemas.patient import PatientResponse
from schemas.doctor import DoctorResponse

class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    reason: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    appointment_date: Optional[datetime] = None
    reason: Optional[str] = None
    status: Optional[str] = None  

class AppointmentResponse(AppointmentBase):
    id: int
    status: str
    created_at: datetime
    patient: Optional[PatientResponse] = None
    doctor: Optional[DoctorResponse] = None

    model_config = ConfigDict(from_attributes=True)