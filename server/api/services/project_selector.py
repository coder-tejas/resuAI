from api.services.llm import extract_json

SYSTEM_PROMPT = """You are a project matching engine. Score projects based on relevance to a job description.

Scoring criteria:
- Keyword overlap (0-40): how many JD keywords appear in the project
- Domain relevance (0-30): industry alignment
- Tech stack match (0-30): technology alignment

Return JSON with selected projects (top 3), each including:
- name, original description, score, selected (boolean), matched_keywords"""

async def select_projects(projects: list[dict], jd_info: dict, company_info: dict = None) -> dict:
    jd_keywords = jd_info.get("keywords", []) + jd_info.get("required_skills", [])
    domain = jd_info.get("domain", "")
    
    prompt = f"""Score and select the best projects for this job:

JD Role: {jd_info.get('role', '')}
JD Keywords: {jd_keywords}
JD Domain: {domain}

Projects:
{chr(10).join([f"- {p.get('name', 'Unnamed')}: {p.get('description', p.get('tech', ''))}" for p in projects])}

Select top 3 projects that best match the JD. Include a score (0-100) and list matched keywords."""
    
    result = await extract_json(prompt, SYSTEM_PROMPT)
    
    selected = result.get("selected_projects", result.get("projects", []))[:3]
    for p in selected:
        p["selected"] = True
    
    return {
        "selected_projects": selected,
        "unselected_projects": [p for p in projects if p.get("name") not in [s.get("name") for s in selected]]
    }