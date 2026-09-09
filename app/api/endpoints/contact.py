from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.contact import ContactMessage
from app.models.user import User
from app.schemas.contact import ContactMessageCreate, ContactMessageUpdate, ContactMessageResponse
from app.api.deps import get_current_user

router = APIRouter()

# --- Rota Pública ---
@router.post("/", response_model=ContactMessageResponse, status_code=status.HTTP_201_CREATED)
def send_contact_message(
    message_in: ContactMessageCreate,
    db: Session = Depends(get_db)
):
    """
    Recebe e salva as mensagens enviadas pelos visitantes no formulário de contato.
    """
    contact_msg = ContactMessage(**message_in.model_dump())
    db.add(contact_msg)
    db.commit()
    db.refresh(contact_msg)
    return contact_msg

# --- Rotas Protegidas (Visualização pelo Admin) ---
@router.get("/", response_model=List[ContactMessageResponse])
def list_messages(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista todas as mensagens recebidas (Apenas Admin).
    """
    messages = db.query(ContactMessage).order_by(ContactMessage.created_at.desc()).offset(skip).limit(limit).all()
    return messages

@router.patch("/{message_id}", response_model=ContactMessageResponse)
def toggle_message_read(
    message_id: int,
    message_in: ContactMessageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Marca/desmarca uma mensagem de contato como lida (Apenas Admin).
    """
    message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Mensagem não encontrada."
        )
    
    if message_in.is_read is not None:
        message.is_read = message_in.is_read
        
    db.add(message)
    db.commit()
    db.refresh(message)
    return message