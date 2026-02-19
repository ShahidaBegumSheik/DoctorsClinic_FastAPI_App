from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from app.utils.pagination import paginate

from app.models.patient import Patient

def create_patient(db: Session, name: str, age: int, phone: str) -> Patient:
    patient = Patient(name=name, age=age, phone=phone)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

def list_patients(db: Session, q: str | None, page: int, size: int):
    stmt = select(Patient)
    if q:
        like = f"%{q.strip()}%"
        stmt = stmt.where(Patient.name.ilike(like) | Patient.phone.ilike(like))

    total, items = paginate(db,stmt,page=page,size=size)
    return total, items

def get_patient(db: Session, patient_id: int) -> Patient:
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
