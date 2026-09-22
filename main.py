import uuid
from pathlib import Path
from urllib.parse import urlparse

import yt_dlp
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from starlette.background import BackgroundTask

app = FastAPI()

DOWNLOAD_DIR = Path(__file__).parent / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_HOSTS = {"facebook.com", "www.facebook.com", "m.facebook.com", "fb.watch"}


class DownloadRequest(BaseModel):
    url: str


@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/download/facebook")
def download_facebook_video(request: DownloadRequest):
    host = urlparse(request.url).hostname or ""
    if host not in ALLOWED_HOSTS:
        raise HTTPException(status_code=400, detail="URL must be a facebook.com or fb.watch link")

    output_template = str(DOWNLOAD_DIR / f"{uuid.uuid4()}.%(ext)s")
    ydl_opts = {
        "outtmpl": output_template,
        "format": "mp4/best",
        "quiet": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.url, download=True)
            file_path = Path(ydl.prepare_filename(info))
    except yt_dlp.utils.DownloadError as exc:
        raise HTTPException(status_code=422, detail=f"Failed to download video: {exc}") from exc

    if not file_path.exists():
        raise HTTPException(status_code=500, detail="Download completed but file was not found")

    filename = f"{info.get('title', 'facebook_video')}{file_path.suffix}"
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="video/mp4",
        background=BackgroundTask(file_path.unlink, missing_ok=True),
    )
