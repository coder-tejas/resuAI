from fastapi import APIRouter
from pydantic import BaseModel
from api.services.company_enrichment import enrich_company

router = APIRouter()

class CompanyPayload(BaseModel):
    company: str

@router.post("/enrich-company")
async def enrich_company_endpoint(payload: CompanyPayload):
    return await enrich_company(payload.company)