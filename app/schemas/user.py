from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

# Schema base com campos comuns
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str

# Usado na resposta da API (oculta o campo de senha por segurança)
class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Schema específico para autenticação (login)
class UserLogin(BaseModel):
    email: EmailStr
    password: str