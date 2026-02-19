from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, require_role
from app.models.user import UserRole, User
from app.schemas.patient import PatientOut
from app.services.assignment_service import assign_patient_to_doctor, get_doctor_patients
from app.services.doctor_service import get_doctor_by_user_id

router = APIRouter(prefix="/doctors", tags=["Assignments"])

@router.post("/{doctor_id}/patients/{patient_id}", dependencies=[Depends(require_role(UserRole.ADMIN))])
def assign(doctor_id: int, patient_id: int, db: Session = Depends(get_db)):
    assign_patient_to_doctor(db, doctor_id, patient_id)
    return {"message": "Patient assigned"}

@router.get("/{doctor_id}/patients", response_model=list[PatientOut])
def doctor_patients(
    doctor_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # Admin can view any doctor's patients
    if user.role == UserRole.ADMIN:
        return get_doctor_patients(db, doctor_id)

    # Doctor can only view their own patients
    if user.role == UserRole.DOCTOR:
        doctor = get_doctor_by_user_id(db, user.id)
        if not doctor or doctor.id != doctor_id:
            raise HTTPException(status_code=403, detail="Doctors can only view their own patients")
        return get_doctor_patients(db, doctor_id)

    raise HTTPException(status_code=403, detail="Forbidden")
