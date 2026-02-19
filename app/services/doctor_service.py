from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from app.models.doctor import Doctor
from app.models.user import UserRole
from app.services.user_service import create_user
from app.utils.pagination import paginate

def create_doctor(db: Session, name: str, specialization: str, emailid: str, password: str) -> Doctor:
    # Create doctor user account (email == emailid)
    user = create_user(db, email=emailid, password=password, role=UserRole.DOCTOR)

    doctor = Doctor(user_id=user.id, name=name, specialization=specialization, emailid=emailid, is_active=True)
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor

def list_doctors(db: Session, is_active: bool | None, q: str | None, page: int, size: int):
    stmt = select(Doctor)
    if is_active is not None:
        stmt = stmt.where(Doctor.is_active == is_active)
    if q:
        like = f"%{q.strip()}%"
        stmt = stmt.where((Doctor.name.ilike(like)) | (Doctor.specialization.ilike(like)) | (Doctor.emailid.ilike(like)))

    total, items = paginate(db,stmt,page=page,size=size)
    return total, items

def get_doctor(db: Session, doctor_id: int) -> Doctor:
    doctor = db.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

def update_doctor(db: Session, doctor_id: int, name: str | None, specialization: str | None, is_active: bool | None) -> Doctor:
    doctor = get_doctor(db, doctor_id)
    if name is not None:
        doctor.name = name
    if specialization is not None:
        doctor.specialization = specialization
    if is_active is not None:
        doctor.is_active = is_active
    db.commit()
    db.refresh(doctor)
    return doctor

def soft_delete_doctor(db: Session, doctor_id: int) -> Doctor:
    doctor = get_doctor(db, doctor_id)
    doctor.is_active = False
    db.commit()
    db.refresh(doctor)
    return doctor

def get_doctor_by_user_id(db: Session, user_id: int) -> Doctor | None:
    return db.scalar(select(Doctor).where(Doctor.user_id == user_id))
