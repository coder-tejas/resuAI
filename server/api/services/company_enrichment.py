from api.services.llm import extract_json

SYSTEM_PROMPT = """You are a company research assistant. For a given company name, find:
- description: what the company does
- domain: industry (fintech, saas, ai, healthcare, etc.)
- tech_stack: technologies they use (infer from job posts, engineering blogs)
- culture: work environment (optional)

Return ONLY valid JSON."""

async def enrich_company(company: str) -> dict:
    if not company:
        return {"description": "", "domain": "", "tech_stack": [], "culture": ""}
    
    prompt = f"""Research this company: {company}

Find information about what they do, their industry, and tech stack."""
    
    result = await extract_json(prompt, SYSTEM_PROMPT)
    
    return {
        "description": result.get("description", ""),
        "domain": result.get("domain", ""),
        "tech_stack": result.get("tech_stack", []),
        "culture": result.get("culture", "")
    }