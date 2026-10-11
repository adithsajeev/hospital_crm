from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from services.auth_utils import RequireRole
from models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard & Analytics"])

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(RequireRole(["admin", "doctor"]))
):
    total_patients = db.query(func.count(Patient.id)).scalar()
    total_doctors = db.query(func.count(Doctor.id)).scalar()
    total_appointments = db.query(func.count(Appointment.id)).scalar()

    scheduled_count = db.query(func.count(Appointment.id)).filter(Appointment.status == "scheduled").scalar()
    completed_count = db.query(func.count(Appointment.id)).filter(Appointment.status == "completed").scalar()
    cancelled_count = db.query(func.count(Appointment.id)).filter(Appointment.status == "cancelled").scalar()

    return {
        "overview": {
            "total_patients": total_patients,
            "total_doctors": total_doctors,
            "total_appointments": total_appointments,
        },
        "appointments_by_status": {
            "scheduled": scheduled_count,
            "completed": completed_count,
            "cancelled": cancelled_count,
        }
    }