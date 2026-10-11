from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from models.patient import Patient
from schemas.patient import PatientCreate, PatientResponse
from services.auth_utils import RequireRole, get_current_active_user
from models.user import User

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(RequireRole(["admin", "receptionist"]))
):
    patient_data = patient.model_dump() if hasattr(patient, "model_dump") else patient.dict()
    db_patient = Patient(**patient_data)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.get("/", response_model=List[PatientResponse])
def list_patients(
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(10, ge=1, le=100, description="Page size limit"),
    search: Optional[str] = Query(None, description="Search by name or phone number"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    query = db.query(Patient)
    
    if search:
        search_pattern = f"%{search.strip()}%"
        
        # Check which phone attribute exists on Patient model
        phone_attr = getattr(Patient, "phone_number", None) or getattr(Patient, "phone", None)
        first_name_attr = getattr(Patient, "first_name", None)
        last_name_attr = getattr(Patient, "last_name", None)
        
        filters = []
        if first_name_attr is not None:
            filters.append(first_name_attr.ilike(search_pattern))
        if last_name_attr is not None:
            filters.append(last_name_attr.ilike(search_pattern))
        if phone_attr is not None:
            filters.append(phone_attr.ilike(search_pattern))
            
        if filters:
            query = query.filter(or_(*filters))
        
    return query.offset(skip).limit(limit).all()

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient