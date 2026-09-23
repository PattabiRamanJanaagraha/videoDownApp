# videoDownApp

A FastAPI application with a hello world endpoint and a health check endpoint.

## Setup

1. Create the virtual environment (skip if `venv/` already exists):

   ```powershell
   python -m venv venv
   ```

2. Activate it:

   ```powershell
   venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

## Project structure

```text
app/
  main.py             FastAPI app factory: mounts static files, includes routers
  routers/
    pages.py          /, /health, /ui, /favicon.ico
    downloads.py      /download/facebook, /download/youtube
  services/
    video_downloader.py   yt-dlp download logic shared by the download routes
  static/             Frontend served at /ui (index.html, style.css, app.js)
desktop.py            Desktop entry point (pywebview window + background server)
```

## Running

```powershell
venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Or, with the virtual environment activated:

```powershell
uvicorn app.main:app --reload
```

The app will be available at http://127.0.0.1:8000.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Serves the frontend for pasting a link and downloading |
| GET | `/health` | Returns the app's health status |
| POST | `/download/facebook` | Downloads a public Facebook video given `{"url": "..."}` and returns the MP4 file |
| POST | `/download/youtube` | Downloads a public YouTube video given `{"url": "..."}` and returns the MP4 file |
| GET | `/ui` | Same frontend as `/`, kept for the desktop app entrypoint |
| GET | `/favicon.ico` | Serves the app's favicon |

## Troubleshooting YouTube "Sign in to confirm you're not a bot"

YouTube's bot-check triggers far more often from datacenter IPs (like Vercel's) than from a home IP. `app/services/video_downloader.py` already asks yt-dlp to try the `android`/`ios` clients first, which avoids the check for many videos with no setup needed.

If a video still fails with that error, supply your own YouTube cookies (this is yt-dlp's own documented fix, see the [FAQ](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp)):

1. While signed in to YouTube in your browser, export cookies in Netscape format (e.g. with the "Get cookies.txt LOCALLY" browser extension).
2. **Local/desktop use:** save the file somewhere on disk and set `YTDLP_COOKIES_FILE` to its path before running. Never commit this file — it's equivalent to a login session (`cookies.txt` is already in `.gitignore`).
3. **Vercel/serverless use:** since there's no persistent filesystem to point a path at, instead set an environment variable `YTDLP_COOKIES` in the Vercel project's settings containing the full contents of the cookies file. It's written to the function's temp dir on first use each cold start. Paste the file's contents as-is — real newlines or literal `\n` sequences (common when a dashboard's input mangles multi-line paste) are both normalized before writing.
4. Redeploy after adding the env var — existing deployments/cold starts won't pick it up otherwise.

Treat both values as secrets — anyone with them can act as your signed-in YouTube session. If a download still fails after this, the app's error message will now say explicitly whether cookies were even configured for that attempt.

## Desktop app

The same FastAPI app can run inside a native desktop window via [pywebview](https://pywebview.flowrl.com/), with the API server running in a background thread.

### Run without packaging

```powershell
venv\Scripts\python.exe desktop.py
```

This opens a window loading the local UI. A free port is picked automatically each run.

### Build a standalone .exe

1. Install the build-only dependency:

   ```powershell
   venv\Scripts\python.exe -m pip install -r requirements-build.txt
   ```

2. Build:

   ```powershell
   venv\Scripts\python.exe -m PyInstaller --noconfirm --onedir --name VideoDownloader --add-data "app/static;app/static" desktop.py
   ```

3. The packaged app is at `dist\VideoDownloader\VideoDownloader.exe` — it can be copied/shared and run without Python installed on the target machine.
