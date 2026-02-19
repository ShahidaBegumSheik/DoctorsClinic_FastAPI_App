from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.association import doctor_patients

class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    specialization: Mapped[str] = mapped_column(String(200), nullable=False)
    emailid: Mapped[str] = mapped_column(String(320),unique=True, index=True,nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True,nullable=False)

    user = relationship("User", back_populates="doctor_profile")
    patients = relationship(
        "Patient",secondary=doctor_patients,back_populates="doctors",lazy="selectin",)
    