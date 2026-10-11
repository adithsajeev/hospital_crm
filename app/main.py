from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from routers import auth, user, patient, doctor, appointment, medical_record, dashboard

# Database models
from models.doctor import Doctor
from models.user import User
from models.patient import Patient
from models.appointment import Appointment
from models.medical_record import MedicalRecord

# Ensure tables are created
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for local development and client apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(user.router)  # 👈 Admin User Management for staff creation
app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(appointment.router)
app.include_router(medical_record.router)
app.include_router(dashboard.router)

@app.get("/", tags=["Health Check"])
def root():
    return {
        "status": "online",
        "message": f"Welcome to {settings.APP_NAME}",
        "docs_url": "/docs",
    }