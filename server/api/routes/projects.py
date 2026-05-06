from fastapi import APIRouter
from pydantic import BaseModel
from api.services.project_selector import select_projects

router = APIRouter()

class ProjectInput(BaseModel):
    projects: list[dict]
    jd_info: dict
    company_info: dict | None = None

@router.post("/select-projects")
async def select_projects_endpoint(input: ProjectInput):
    return await select_projects(input.projects, input.jd_info, input.company_info)