
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False,
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id"),
        nullable=False,
    )

    appointment_date = Column(DateTime, nullable=False, index=True)
    reason = Column(Text, nullable=True)
    status = Column(String, default="scheduled", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship(
        "Patient",
        back_populates="appointments",
    )

    doctor = relationship(
        "Doctor",
        back_populates="appointments",
    )

    medical_records = relationship(
        "MedicalRecord",
        back_populates="appointment",
    )