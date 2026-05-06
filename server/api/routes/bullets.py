from fastapi import APIRouter
from pydantic import BaseModel
from api.services.bullet_optimizer import optimize_bullets

router = APIRouter()

class BulletInput(BaseModel):
    projects: list[dict]
    jd_info: dict

@router.post("/optimize-bullets")
async def optimize_bullets_endpoint(input: BulletInput):
    return await optimize_bullets(input.projects, input.jd_info)