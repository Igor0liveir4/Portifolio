from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api.router import api_router
from app.db.session import get_db, engine, Base
from app.models.project import Project

# 1. Cria as tabelas automaticamente no banco caso ainda não existam
Base.metadata.create_all(bind=engine)

# 2. Instancia a aplicação FastAPI
app = FastAPI(
    title="Portfólio API",
    description="API e Website do meu Portfólio Profissional",
    version="1.0.0"
)

# 3. Inclui as rotas da API JSON (/api/projects, /api/auth, /api/contact)
app.include_router(api_router)

# 4. Configura pastas estáticas e templates HTML
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Rotas Web (Frontend Jinja2)

@app.get("/", summary="Página Inicial do Portfólio")
def home(request: Request, db: Session = Depends(get_db)):
    """
    Renderiza a página principal do portfólio (index.html)
    injetando os projetos cadastrados no banco de dados.
    """
    # Busca os projetos ordenados do mais recente para o mais antigo
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request, 
            "projects": projects
        }
    )

@app.get("/admin/login", summary="Página de Login do Admin")
def admin_login(request: Request):
    """
    Renderiza a tela de login do painel administrativo.
    """
    return templates.TemplateResponse(request, "admin/login.html", {"request": request})

@app.get("/admin/dashboard", summary="Painel de Controle")
def admin_dashboard(request: Request):
    """
    Renderiza a interface do painel administrativo.
    (O controle de acesso JWT é feito no frontend via JavaScript/Local Storage).
    """
    return templates.TemplateResponse(request, "admin/dashboard.html", {"request": request})