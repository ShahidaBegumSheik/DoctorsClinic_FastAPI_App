from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_role
from app.models.user import UserRole
from app.schemas.patient import PatientCreate, PatientOut
from app.schemas.common import Paginated
from app.services.patient_service import create_patient, list_patients, get_patient

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("", response_model=PatientOut, dependencies=[Depends(require_role(UserRole.ADMIN))])
def create(payload: PatientCreate, db: Session = Depends(get_db)):
    return create_patient(db, payload.name, payload.age, payload.phone)

@router.get("", response_model=dict, dependencies=[Depends(require_role(UserRole.ADMIN))])
def list_(
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    q: str | None = Query(default=None, description="Search by name/phone"),
):
    total, items = list_patients(db, q=q, page=page, size=size)

    items_out = [PatientOut.model_validate(p) for p in items]
    return {"meta": Paginated(total=total, page=page, size=size).model_dump(), "items": items_out}

@router.get("/{patient_id}", response_model=PatientOut, dependencies=[Depends(require_role(UserRole.ADMIN))])
def get_(patient_id: int, db: Session = Depends(get_db)):
    return get_patient(db, patient_id)
