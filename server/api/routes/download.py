from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/download/{filename}")
async def download_pdf(filename: str):
    output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    file_path = os.path.join(output_dir, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(404, "File not found")
    
    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=filename
    )