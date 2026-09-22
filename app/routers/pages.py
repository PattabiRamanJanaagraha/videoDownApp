from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

router = APIRouter()


@router.get("/")
def hello_world():
    return {"message": "Hello, World!"}


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/ui")
def ui():
    return FileResponse(STATIC_DIR / "index.html")
