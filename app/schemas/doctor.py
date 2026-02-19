from pydantic import BaseModel, EmailStr, Field
from app.schemas.common import ORMBase
from pydantic import BaseModel, ConfigDict, EmailStr

class DoctorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    specialization: str = Field(min_length=1, max_length=200)
    emailid: EmailStr
    # password used to create the doctor user
    password: str = Field(min_length=8, max_length=128)

class DoctorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    specialization: str | None = Field(default=None, min_length=1, max_length=200)
    is_active: bool | None = None

class DoctorOut(ORMBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    specialization: str
    emailid: EmailStr
    is_active: bool
