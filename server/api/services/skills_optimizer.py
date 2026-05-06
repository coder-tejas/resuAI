from api.services.llm import extract_json

SYSTEM_PROMPT = """You are a skills section optimizer. Reorder and filter skills based on job relevance.

Group skills into:
- Languages (Python, JavaScript, Go, etc.)
- Frameworks (React, FastAPI, Django, etc.)
- Tools (Docker, Git, AWS, etc.)
- Libraries,Databases (SQL, Redis, etc.)

Prioritize JD-relevant skills. Remove low-relevance or noisy skills.

Return JSON with grouped skills."""

async def optimize_skills(skills: dict, jd_info: dict) -> dict:
    jd_required = jd_info.get("required_skills", [])
    jd_keywords = jd_info.get("keywords", [])
    all_jd_skills = jd_required + jd_keywords
    
    flat_skills = []
    for category, skill_list in skills.items():
        if isinstance(skill_list, list):
            flat_skills.extend(skill_list)
        elif isinstance(skill_list, str):
            flat_skills.extend([s.strip() for s in skill_list.split(',')])
    
    prompt = f"""Reorder and group these skills by relevance to the job:

Current skills: {flat_skills}
JD required: {jd_required}
JD keywords: {jd_keywords}

Prioritize skills that match the JD. Group them into: Languages, Frameworks, Tools, Libraries/Databases.

Remove irrelevant skills. Return grouped JSON."""
    
    result = await extract_json(prompt, SYSTEM_PROMPT)
    
    return {"optimized_skills": result}