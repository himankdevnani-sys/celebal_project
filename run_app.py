"""
PatchContext One-Click Runner
Launches both the FastAPI backend server (Port 8000) and the Streamlit web application concurrently.
"""
import subprocess
import sys
import time
import os
import signal

def run():
    print("=" * 65)
    print("⚡ Starting PatchContext AI Application...")
    print("=" * 65)

    project_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. Start FastAPI Backend Server
    print("\n🚀 [1/2] Launching FastAPI Backend Server on http://localhost:8000 ...")
    backend_process = subprocess.Popen(
        [sys.executable, "run_backend.py"],
        cwd=project_dir
    )

    # Wait for backend server startup
    time.sleep(2.5)

    # 2. Start Streamlit Frontend
    print("\n🎨 [2/2] Launching Streamlit Web App Interface ...")
    print("=" * 65)
    print("      Streamlit will open in your default browser shortly!")
    print("      Press Ctrl+C in this terminal to stop both servers.")
    print("=" * 65 + "\n")

    try:
        streamlit_process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "app.py"],
            cwd=project_dir
        )
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down PatchContext services...")
    finally:
        # Gracefully kill backend process
        if backend_process.poll() is None:
            backend_process.terminate()
            try:
                backend_process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                backend_process.kill()
        print("✅ PatchContext services stopped successfully.")

if __name__ == "__main__":
    run()
