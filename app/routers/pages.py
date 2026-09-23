from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

router = APIRouter()


@router.get("/")
def root():
    return FileResponse(STATIC_DIR / "index.html")


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/ui")
def ui():
    return FileResponse(STATIC_DIR / "index.html")


@router.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse(STATIC_DIR / "favicon.ico")
