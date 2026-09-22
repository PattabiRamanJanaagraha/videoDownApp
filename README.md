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
