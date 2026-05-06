import os
import json
import httpx

MODEL = os.getenv("LLM_MODEL", "google/gemini-2.0-flash-001")
API_KEY = os.getenv("OPENROUTER_API_KEY")

async def chat(messages: list, system: str = None) -> str:
    if system:
        messages = [{"role": "system", "content": system}] + messages
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": messages
            },
            timeout=60.0
        )
    
    data = response.json()
    return data["choices"][0]["message"]["content"]

async def extract_json(prompt: str, system: str = None) -> dict:
    messages = [{"role": "user", "content": prompt + "\n\nRespond with valid JSON only."}]
    response = await chat(messages, system)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            return json.loads(response[start:end])
        except:
            return {"error": "Failed to parse JSON", "raw": response}

async def extract_json_list(prompt: str, system: str = None) -> list:
    messages = [{"role": "user", "content": prompt + "\n\nRespond with valid JSON array only."}]
    response = await chat(messages, system)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        try:
            start = response.find('[')
            end = response.rfind(']') + 1
            return json.loads(response[start:end])
        except:
            return []