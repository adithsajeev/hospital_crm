from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from models.user import User
from schemas.user import UserCreateSchema, TokenSchema
from services.auth_utils import verify_password, hash_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/setup-admin", status_code=status.HTTP_201_CREATED)
def create_initial_admin(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    # Security Check: Block creation if an admin already exists in the system
    existing_admin = db.query(User).filter(User.role == "admin").first()
    if existing_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
            detail="Initial admin setup is disabled because an admin user already exists."
        )

    
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    new_admin = User(username=user_data.username,email=user_data.email,hashed_password=hash_password(user_data.password),full_name=user_data.full_name,role="admin",is_active=True)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return {"message": f"Admin user {new_admin.username} created successfully"}

@router.post("/login", response_model=TokenSchema)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password")
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user account")

    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "username": user.username
    }