
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from models.appointment import Appointment
from models.patient import Patient
from models.doctor import Doctor
from models.user import User
from schemas.appointment import (AppointmentCreate,AppointmentResponse,AppointmentUpdate,)
from services.auth_utils import get_current_active_user, RequireRole


router = APIRouter(prefix="/appointments",tags=["Appointments"],)


@router.post("/",response_model=AppointmentResponse,status_code=status.HTTP_201_CREATED,)

def create_appointment(appointment: AppointmentCreate,db: Session = Depends(get_db),current_user: User = Depends(get_current_active_user),):

    patient = (db.query(Patient).filter(Patient.id == appointment.patient_id).first())

    if not patient:raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Patient not found",)

    doctor = (db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first())

    if not doctor:raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Doctor not found",)

    if not doctor.is_available:raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Doctor is currently not available for appointments",)

    db_appointment = Appointment(**appointment.model_dump())

    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)

    return db_appointment


@router.get("/",response_model=List[AppointmentResponse],)
def get_appointments(
    doctor_id: Optional[int] = Query(None,ge=1,description="Filter by doctor ID",),
    patient_id: Optional[int] = Query(None,ge=1,description="Filter by patient ID",),
    status: Optional[str] = Query(None,pattern="^(scheduled|confirmed|completed|cancelled)$",description="Filter by appointment status",),
    skip: int = Query(0,ge=0,description="Number of appointments to skip",),
    limit: int = Query(100,ge=1,le=100,description="Maximum number of appointments to return",),
    db: Session = Depends(get_db),current_user: User = Depends(get_current_active_user),):
    query = db.query(Appointment)

    if doctor_id is not None:query = query.filter(Appointment.doctor_id == doctor_id)

    if patient_id is not None:query = query.filter(Appointment.patient_id == patient_id)

    if status is not None:query = query.filter(Appointment.status == status)

    appointments = (query.offset(skip).limit(limit).all())

    return appointments


@router.get("/{appointment_id}",response_model=AppointmentResponse,)
def get_appointment(appointment_id: int,db: Session = Depends(get_db),current_user: User = Depends(get_current_active_user),):
    appointment = (db.query(Appointment).filter(Appointment.id == appointment_id).first())

    if not appointment:raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Appointment not found",)

    return appointment


@router.put("/{appointment_id}",response_model=AppointmentResponse,)
def update_appointment(appointment_id: int,appointment_update: AppointmentUpdate,db: Session = Depends(get_db),current_user: User = Depends(get_current_active_user),):
    appointment = (db.query(Appointment).filter(Appointment.id == appointment_id).first())

    if not appointment:raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Appointment not found",)

    update_data = appointment_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():setattr(appointment, key, value)

    db.commit()
    db.refresh(appointment)

    return appointment

@router.delete("/{appointment_id}",status_code=status.HTTP_204_NO_CONTENT,)

def cancel_appointment(appointment_id: int,db: Session = Depends(get_db),current_user: User = Depends(RequireRole(["admin", "receptionist"])),):
    appointment = (db.query(Appointment).filter(Appointment.id == appointment_id).first())

    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Appointment not found",)

    appointment.status = "cancelled"

    db.commit()

    return None