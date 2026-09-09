from fastapi import APIRouter
from app.api.endpoints import auth, projects, contact

api_router = APIRouter(prefix="/api")

# Registra os grupos de endpoints com suas respectivas tags para o Swagger
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projetos"])
api_router.include_router(contact.router, prefix="/contact", tags=["Contato"])