from pydantic import BaseModel, Field, field_validator, ConfigDict
from app.schemas.common import ORMBase

class PatientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    age: int = Field(gt=0)
    phone: str = Field(min_length=10, max_length=15)

    @field_validator("phone")
    @classmethod
    def phone_digits_only(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Phone number must contain digits only")
        return v

class PatientOut(ORMBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    age: int
    phone: str
