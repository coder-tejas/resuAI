import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

load_dotenv()

app = FastAPI(title="resoAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
db = client[os.getenv("DB_NAME", "resoAI")]

from api.routes import jd, company, projects, bullets, resume, skills, download

app.include_router(jd.router, prefix="/api", tags=["JD"])
app.include_router(company.router, prefix="/api", tags=["Company"])
app.include_router(projects.router, prefix="/api", tags=["Projects"])
app.include_router(bullets.router, prefix="/api", tags=["Bullets"])
app.include_router(resume.router, prefix="/api", tags=["Resume"])
app.include_router(skills.router, prefix="/api", tags=["Skills"])
app.include_router(download.router, prefix="/api", tags=["Download"])

@app.get("/health")
def health():
    return {"status": "ok"}