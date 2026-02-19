from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.association import doctor_patients

class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False, index=True)

    doctors = relationship(
        "Doctor", secondary=doctor_patients,back_populates="patients",lazy="selectin",
    )
    