from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint
from app.db.base import Base

doctor_patients = Table(
    "doctor_patients", 
    Base.metadata,
    Column("doctor_id",ForeignKey("doctors.id", ondelete="CASCADE"), primary_key=True),
    Column("patient_id",ForeignKey("patients.id", ondelete="CASCADE"), primary_key=True),
    UniqueConstraint("doctor_id", "patient_id", name="uq_doctor_patient"),
)