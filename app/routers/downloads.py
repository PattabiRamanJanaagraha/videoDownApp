from fastapi import APIRouter
from pydantic import BaseModel

from app.services.video_downloader import FACEBOOK_HOSTS, YOUTUBE_HOSTS, download_video

router = APIRouter(prefix="/download", tags=["download"])


class DownloadRequest(BaseModel):
    url: str


@router.post("/facebook")
def download_facebook_video(request: DownloadRequest):
    return download_video(request.url, FACEBOOK_HOSTS, "facebook.com or fb.watch")


@router.post("/youtube")
def download_youtube_video(request: DownloadRequest):
    return download_video(request.url, YOUTUBE_HOSTS, "youtube.com or youtu.be")
