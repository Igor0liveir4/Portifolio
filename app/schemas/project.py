from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, HttpUrl

# Schema base com campos comuns
class ProjectBase(BaseModel):
    title: str
    description: str
    tech_stack: str  # Ex: "FastAPI, SQLAlchemy, SQLite"
    image_url: Optional[str] = None
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    is_featured: bool = False

# Usado na requisição POST /api/admin/projects
class ProjectCreate(ProjectBase):
    pass

# Usado na requisição PUT /api/admin/projects/{id} (todos os campos tornam-se opcionais)
class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tech_stack: Optional[str] = None
    image_url: Optional[str] = None
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    is_featured: Optional[bool] = None

# Usado para retornar os projetos na API (JSON)
class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)