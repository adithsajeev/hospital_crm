
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=True,
        index=True
    )

    full_name = Column(String, nullable=False, index=True)
    specialization = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="doctor")

    appointments = relationship(
        "Appointment",
        back_populates="doctor"
    )

    medical_records = relationship(
        "MedicalRecord",
        back_populates="doctor"
    )