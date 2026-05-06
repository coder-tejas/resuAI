from fastapi import APIRouter
from pydantic import BaseModel
from api.services.llm import extract_json
from api.services.jd_parser import parse_jd

router = APIRouter()

class JDPayload(BaseModel):
    jd_text: str
    company: str | None = None

@router.post("/parse-jd")
async def parse_jd_endpoint(payload: JDPayload):
    return await parse_jd(payload.jd_text, payload.company)