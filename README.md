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

## Running

```powershell
venv\Scripts\python.exe -m uvicorn main:app --reload
```

Or, with the virtual environment activated:

```powershell
uvicorn main:app --reload
```

The app will be available at http://127.0.0.1:8000.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Returns a hello world message |
| GET | `/health` | Returns the app's health status |
| POST | `/download/facebook` | Downloads a public Facebook video given `{"url": "..."}` and returns the MP4 file |
| POST | `/download/youtube` | Downloads a public YouTube video given `{"url": "..."}` and returns the MP4 file |
| GET | `/ui` | Serves the browser/desktop frontend for pasting a link and downloading |

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
   venv\Scripts\python.exe -m PyInstaller --noconfirm --onedir --name VideoDownloader --add-data "static;static" desktop.py
   ```

3. The packaged app is at `dist\VideoDownloader\VideoDownloader.exe` — it can be copied/shared and run without Python installed on the target machine.
