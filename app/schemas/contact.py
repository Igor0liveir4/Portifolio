from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

# Schema base
class ContactMessageBase(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

# Usado quando o visitante envia o formulário de contato (POST /api/contact)
class ContactMessageCreate(ContactMessageBase):
    pass

# Usado no painel admin para atualizar status de leitura
class ContactMessageUpdate(BaseModel):
    is_read: Optional[bool] = True

# Usado para retornar as mensagens para o painel de admin
class ContactMessageResponse(ContactMessageBase):
    id: int
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)