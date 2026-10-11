Hospital CRM System API

A robust, enterprise-grade RESTful API backend built with FastAPI, SQLAlchemy, and Pydantic designed for efficient hospital management, clinical operations, and administrative workflows.

Key Features

Role-Based Access Control (RBAC): Strict security boundaries and permission enforcement for Admins, Doctors, Receptionists, and Patients using JWT authentication.
Unified Staff & Doctor Onboarding: Secure administrative controls separating generic staff management (`/users/`) from specialized clinical profiles (`/doctors/`) via atomic transactions.
Patient & Appointment Management: Streamlined scheduling system allowing receptionists and staff to book, track, and manage patient appointments.
Electronic Medical Records (EMR): Secure clinical record management enforcing strict data ownership (doctors can only edit their own clinical entries, while admins retain oversight).
Automated Data Validation: Pydantic `Enum` validation ensuring clean role definitions and preventing invalid data entries.



Tech Stack

* Framework: FastAPI (Python)
* Database ORM: SQLAlchemy
* Data Validation: Pydantic v2
* Authentication: OAuth2 with Password Bearer & JWT Tokens (`python-jose`, `passlib`)
* Database: SQLite (Easily configurable to PostgreSQL/MySQL via environment variables)
* Server:Uvicorn



Project Directory Structure


hospital_crm/
│
├── app/
│   ├── __init__.py
│   ├── config.py         # Application configuration & settings
│   └── database.py       # Database engine & session dependency
│
├── models/               # SQLAlchemy Database Models
│   ├── user.py
│   ├── doctor.py
│   ├── patient.py
│   ├── appointment.py
│   └── medical_record.py
│
├── schemas/              # Pydantic Validation Schemas
│   ├── user.py
│   ├── doctor.py
│   ├── patient.py
│   ├── appointment.py
│   └── medical_record.py
│
├── routers/              # API Route Handlers
│   ├── auth.py
│   ├── user.py
│   ├── doctor.py
│   ├── patient.py
│   ├── appointment.py
│   ├── medical_record.py
│   └── dashboard.py
│
├── services/             # Business Logic & Auth Utilities
│   └── auth_utils.py
│
├── main.py               # Application Entrypoint & Middleware Setup
├── requirements.txt      # Project Dependencies
└── README.md
