from pydantic import EmailStr
from app.schemas.common import ORMBase

class UserOut(ORMBase):
    id: int
    email: EmailStr
    role: str
