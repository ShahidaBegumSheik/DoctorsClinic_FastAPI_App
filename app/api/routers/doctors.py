from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_role
from app.models.user import UserRole
from app.schemas.doctor import DoctorCreate, DoctorUpdate, DoctorOut
from app.schemas.common import Paginated
from app.services.doctor_service import (
    create_doctor, list_doctors, get_doctor, update_doctor, soft_delete_doctor
)

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.post("", response_model=DoctorOut, dependencies=[Depends(require_role(UserRole.ADMIN))])
def create(payload: DoctorCreate, db: Session = Depends(get_db)):
    return create_doctor(db, payload.name, payload.specialization, payload.emailid, payload.password)

@router.get("", response_model=dict, dependencies=[Depends(require_role(UserRole.ADMIN))])
def list_(
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    is_active: bool | None = Query(default=None),
    q: str | None = Query(default=None, description="Search by name/specialization/email"),
):
    total, items = list_doctors(db, is_active=is_active, q=q, page=page, size=size)
    items_out = [DoctorOut.model_validate(d) for d in items]
    return {"meta": Paginated(total=total, page=page, size=size).model_dump(), "items": items_out}

@router.get("/{doctor_id}", response_model=DoctorOut, dependencies=[Depends(require_role(UserRole.ADMIN))])
def get_(doctor_id: int, db: Session = Depends(get_db)):
    return get_doctor(db, doctor_id)

@router.put("/{doctor_id}", response_model=DoctorOut, dependencies=[Depends(require_role(UserRole.ADMIN))])
def update_(doctor_id: int, payload: DoctorUpdate, db: Session = Depends(get_db)):
    return update_doctor(db, doctor_id, payload.name, payload.specialization, payload.is_active)

@router.delete("/{doctor_id}", response_model=DoctorOut, dependencies=[Depends(require_role(UserRole.ADMIN))])
def delete_(doctor_id: int, db: Session = Depends(get_db)):
    return soft_delete_doctor(db, doctor_id)
