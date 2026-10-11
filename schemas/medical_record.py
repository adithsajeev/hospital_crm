from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from schemas.patient import PatientResponse
from schemas.doctor import DoctorResponse

class MedicalRecordBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int] = None
    diagnosis: str
    prescription: Optional[str] = None
    notes: Optional[str] = None

class MedicalRecordCreate(MedicalRecordBase):
    pass

class MedicalRecordUpdate(BaseModel):
    diagnosis: Optional[str] = None
    prescription: Optional[str] = None
    notes: Optional[str] = None

class MedicalRecordResponse(MedicalRecordBase):
    id: int
    created_at: datetime
    patient: Optional[PatientResponse] = None
    doctor: Optional[DoctorResponse] = None

    model_config = ConfigDict(from_attributes=True)