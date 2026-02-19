from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.services.doctor_service import get_doctor
from app.services.patient_service import get_patient

def assign_patient_to_doctor(db: Session, doctor_id: int, patient_id: int):
    doctor = get_doctor(db, doctor_id)
    patient = get_patient(db, patient_id)

    if not doctor.is_active:
        raise HTTPException(status_code=400, detail="Doctor is inactive")

    if patient in doctor.patients:
        return doctor  # idempotent

    doctor.patients.append(patient)
    db.commit()
    db.refresh(doctor)
    return doctor

def get_doctor_patients(db: Session, doctor_id: int):
    doctor = get_doctor(db, doctor_id)
    return doctor.patients
