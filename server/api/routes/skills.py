from fastapi import APIRouter
from pydantic import BaseModel
from api.services.skills_optimizer import optimize_skills

router = APIRouter()

class SkillsInput(BaseModel):
    skills: dict
    jd_info: dict

@router.post("/optimize-skills")
async def optimize_skills_endpoint(input: SkillsInput):
    return await optimize_skills(input.skills, input.jd_info)