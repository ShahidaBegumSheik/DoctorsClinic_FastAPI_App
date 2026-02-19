from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from app.models.user import User, UserRole
from app.core.security import hash_password, verify_password

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))

def create_user(db: Session, email: str, password: str, role: UserRole) -> User:
    if get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=email, password_hash=hash_password(password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> User:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
