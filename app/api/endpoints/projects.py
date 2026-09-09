from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.api.deps import get_current_user

router = APIRouter()

# --- Rotas Públicas ---
@router.get("/", response_model=List[ProjectResponse])
def read_projects(
    skip: int = 0, 
    limit: int = 100, 
    featured_only: bool = False,
    db: Session = Depends(get_db)
):
    """
    Retorna a lista de projetos do portfólio.
    """
    query = db.query(Project)
    if featured_only:
        query = query.filter(Project.is_featured == True)
    
    projects = query.offset(skip).limit(limit).all()
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
def read_project_by_id(project_id: int, db: Session = Depends(get_db)):
    """
    Retorna os detalhes de um projeto específico.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Projeto não encontrado."
        )
    return project

# --- Rotas Protegidas (Apenas Admin autenticado) ---
@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cadastra um novo projeto no portfólio.
    """
    project = Project(**project_in.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza as informações de um projeto existente.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Projeto não encontrado."
        )

    # Atualiza dinamicamente apenas os campos enviados no JSON
    update_data = project_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove um projeto do portfólio.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Projeto não encontrado."
        )
    
    db.delete(project)
    db.commit()
    return None