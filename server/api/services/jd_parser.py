from api.services.llm import extract_json
from sklearn.feature_extraction.text import TfidfVectorizer
import re

def rank_keywords_tfidf(texts: list) -> list[str]:
    if not texts:
        return []
    vectorizer = TfidfVectorizer(stop_words='english', max_features=20)
    try:
        tfidf_matrix = vectorizer.fit_transform(texts)
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.sum(axis=0).A1
        ranked = sorted(zip(feature_names, scores), key=lambda x: x[1], reverse=True)
        return [word for word, _ in ranked[:15]]
    except:
        return []

SYSTEM_PROMPT = """You are an expert ATS resume optimizer. Parse job descriptions to extract structured data.
Return ONLY valid JSON with these fields:
- role: job title
- required_skills: array of must-have skills
- preferred_skills: array of nice-to-have skills  
- keywords: important terms (tools, frameworks, concepts)
- responsibilities: key duties
- domain: industry (fintech, saas, ai, etc.)
- experience_level: junior, mid, senior, lead"""

async def parse_jd(jd_text: str, company: str = None) -> dict:
    tfidf_keywords = rank_keywords_tfidf([jd_text])
    
    prompt = f"""Parse this job description:

{jd_text[:3000]}

{f'Company: {company}' if company else ''}

Also consider these TF-IDF ranked keywords: {tfidf_keywords}

Extract the structured information."""
    
    parsed = await extract_json(prompt, SYSTEM_PROMPT)
    
    return {
        "role": parsed.get("role", ""),
        "required_skills": parsed.get("required_skills", []),
        "preferred_skills": parsed.get("preferred_skills", []),
        "keywords": parsed.get("keywords", tfidf_keywords),
        "responsibilities": parsed.get("responsibilities", []),
        "domain": parsed.get("domain", ""),
        "experience_level": parsed.get("experience_level", "mid"),
        "tfidf_keywords": tfidf_keywords
    }