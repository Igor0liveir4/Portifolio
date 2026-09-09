from datetime import datetime, timedelta
from typing import Any, Optional, Union
from jose import jwt, JWTError
from passlib.context import CryptContext

# Configurações de Segurança
# Em produção, esses valores devem ser carregados via variáveis de ambiente (.env)
SECRET_KEY = "SUA_CHAVE_SECRETA_SUPER_SEGURA_E_ALEATORIA_AQUI"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # O token expira em 24 horas

# Contexto de criptografia para hashing de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Funções para Gerenciamento de Senhas (Hashing & Verificação)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha em texto puro corresponde ao hash armazenado no banco.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Gera o hash Bcrypt a partir de uma senha em texto puro.
    """
    return pwd_context.hash(password)

# Funções para Gerenciamento de Tokens JWT
def create_access_token(
    subject: Union[str, Any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Cria um token JWT codificado contendo a identidade do usuário (ex: e-mail)
    e uma data de expiração.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Payload do token JWT
    to_encode = {
        "exp": expire,      # Tempo de expiração
        "sub": str(subject) # Subject (Identificador do usuário, geralmente o e-mail)
    }

    # Gera e retorna o token assinado
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[str]:
    """
    Decodifica o token JWT e retorna o 'subject' (e-mail) se for válido.
    Retorna None se o token estiver expirado ou for inválido.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Optional[str] = payload.get("sub")
        return email
    except JWTError:
        return None