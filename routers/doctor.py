
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from models.doctor import Doctor
from models.user import User
from schemas.doctor import (
    DoctorCreateWithUser,
    DoctorResponse,
    DoctorUpdate,
)
from services.auth_utils import (
    RequireRole,
    get_current_active_user,
    hash_password,
)

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post(
    "/",
    response_model=DoctorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_doctor(
    doctor_data: DoctorCreateWithUser,
    db: Session = Depends(get_db),
    current_user: User = Depends(RequireRole(["admin"])),
):
    existing_user = (
        db.query(User)
        .filter(User.username == doctor_data.username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    existing_email = (
        db.query(User)
        .filter(User.email == doctor_data.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered to a user",
        )

    existing_doctor = (
        db.query(Doctor)
        .filter(Doctor.email == doctor_data.email)
        .first()
    )

    if existing_doctor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor with this email already exists",
        )

    try:
        new_user = User(
            username=doctor_data.username,
            email=doctor_data.email,
            hashed_password=hash_password(doctor_data.password),
            full_name=doctor_data.full_name,
            role="doctor",
            is_active=True,
        )

        db.add(new_user)

        db.flush()

        doctor_fields = doctor_data.model_dump(
            exclude={"username", "password"}
        )

        new_doctor = Doctor(
            **doctor_fields,
            user_id=new_user.id,
        )

        db.add(new_doctor)

        db.commit()
        db.refresh(new_doctor)

        return new_doctor

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Could not create doctor. Username or email may already exist.",
        )


@router.get("/", response_model=List[DoctorResponse])
def get_doctors(
    specialization: Optional[str] = Query(
        None, description="Filter by specialization"
    ),
    is_available: Optional[bool] = Query(
        None, description="Filter by availability status"
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    query = db.query(Doctor)

    if specialization:
        query = query.filter(
            Doctor.specialization.ilike(f"%{specialization}%")
        )

    if is_available is not None:
        query = query.filter(Doctor.is_available == is_available)

    return query.offset(skip).limit(limit).all()


@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )

    return doctor


@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(
    doctor_id: int,
    doctor_update: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RequireRole(["admin"])),
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )

    update_data = doctor_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(doctor, key, value)

    db.commit()
    db.refresh(doctor)

    return doctor