from api.services.llm import extract_json_list

SYSTEM_PROMPT = """You are an ATS resume bullet point optimizer. Rewrite project descriptions into powerful, quantified bullet points.

Requirements:
- Start with strong action verbs (Designed, Built, Implemented, Optimized, Developed, Created, Refactored)
- Include metrics where possible (% improvement, users, requests, scale)
- Use ATS keywords from the job description
- Keep concise (1-2 lines each)
- Avoid generic statements
- Show impact

Return array of bullet points (3-5 per project)."""

async def optimize_bullets(projects: list[dict], jd_info: dict) -> dict:
    jd_keywords = jd_info.get("keywords", []) + jd_info.get("required_skills", [])
    domain = jd_info.get("domain", "")
    
    optimized = []
    
    for project in projects:
        name = project.get("name", "Project")
        description = project.get("description", "")
        tech = project.get("tech", "")
        
        prompt = f"""Rewrite these bullets for project '{name}' (tech: {tech})

Original: {description}

JD Keywords: {jd_keywords}
Domain: {domain}

Create 3-5 optimized bullet points that:
1. Use strong action verbs
2. Include quantified impact
3. Include relevant keywords
4. Are ATS-friendly
5. Show what you achieved"""
        
        bullets = await extract_json_list(prompt, SYSTEM_PROMPT)
        
        optimized.append({
            "name": name,
            "tech": tech,
            "bullets": bullets if bullets else [description]
        })
    
    return {"optimized_projects": optimized}