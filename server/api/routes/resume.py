from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.services.resume_generator import generate_resume

router = APIRouter()

class ResumeInput(BaseModel):
    personal_info: dict
    education: list[dict]
    projects: list[dict]
    skills: dict
    jd_info: dict

@router.post("/generate-resume")
async def generate_resume_endpoint(input: ResumeInput):
    try:
        pdf_path = await generate_resume(
            input.personal_info,
            input.education,
            input.projects,
            input.skills,
            input.jd_info
        )
        return {"pdf_path": pdf_path, "status": "generated"}
    except Exception as e:
        raise HTTPException(500, str(e))