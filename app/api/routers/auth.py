from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.schemas.user import UserOut
from app.services.user_service import create_user, authenticate_user
from app.models.user import UserRole
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut, summary="Register an admin user")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    user = create_user(db, email=payload.email, password=payload.password, role=UserRole.ADMIN)
    return user

@router.post("/login", response_model=TokenResponse, summary="Login and get JWT access token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=user.email, role=user.role.value)
    return {"access_token": token, "token_type": "bearer"}
