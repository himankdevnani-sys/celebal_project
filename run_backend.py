"""
PatchContext Backend Launcher Script
Runs the FastAPI Uvicorn server on http://localhost:8000
"""
import uvicorn

if __name__ == "__main__":
    print("Starting PatchContext FastAPI Backend Server on http://localhost:8000...")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
