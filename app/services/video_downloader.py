import os
import tempfile
import uuid
from pathlib import Path
from urllib.parse import urlparse

import yt_dlp
from fastapi import HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

DOWNLOAD_DIR = Path(tempfile.gettempdir()) / "any-video-downloader"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

FACEBOOK_HOSTS = {"facebook.com", "www.facebook.com", "m.facebook.com", "fb.watch"}
YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}

# YouTube's "Sign in to confirm you're not a bot" check triggers far more often
# from datacenter IPs (e.g. Vercel) than from a home IP. YTDLP_COOKIES_FILE
# points at a cookies.txt already on disk (local/desktop use). YTDLP_COOKIES
# holds the same file's contents as a string (for serverless, where secrets
# are set as env vars rather than files) and gets materialized into the
# read/write temp dir on first use.
_cookies_file_cache: Path | None = None


def _cookies_file() -> str | None:
    global _cookies_file_cache

    local_path = os.environ.get("YTDLP_COOKIES_FILE")
    if local_path:
        return local_path

    cookies_content = os.environ.get("YTDLP_COOKIES")
    if not cookies_content:
        return None

    if _cookies_file_cache is None:
        _cookies_file_cache = DOWNLOAD_DIR / "cookies.txt"
        _cookies_file_cache.write_text(cookies_content, encoding="utf-8")

    return str(_cookies_file_cache)


def download_video(url: str, allowed_hosts: set[str], site_name: str) -> FileResponse:
    host = urlparse(url).hostname or ""
    if host not in allowed_hosts:
        raise HTTPException(status_code=400, detail=f"URL must be a {site_name} link")

    output_template = str(DOWNLOAD_DIR / f"{uuid.uuid4()}.%(ext)s")
    ydl_opts = {
        "outtmpl": output_template,
        "format": "mp4/best",
        "quiet": True,
        "noplaylist": True,
        # The android/ios clients skip the web bot-check that triggers
        # "Sign in to confirm you're not a bot" on datacenter IPs, so try
        # them before falling back to the regular web client.
        "extractor_args": {"youtube": {"player_client": ["android", "ios", "web"]}},
    }

    cookies_file = _cookies_file()
    if cookies_file:
        ydl_opts["cookiefile"] = cookies_file

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = Path(ydl.prepare_filename(info))
    except yt_dlp.utils.DownloadError as exc:
        raise HTTPException(status_code=422, detail=f"Failed to download video: {exc}") from exc

    if not file_path.exists():
        raise HTTPException(status_code=500, detail="Download completed but file was not found")

    filename = f"{info.get('title', 'video')}{file_path.suffix}"
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="video/mp4",
        background=BackgroundTask(file_path.unlink, missing_ok=True),
    )
