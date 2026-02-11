#!/usr/bin/env python3
"""
Start the Todo API server
"""
import subprocess
import sys
import os

def start_server():
    """Start the FastAPI server using uvicorn."""
    print("Starting Todo API server...")

    # Check if uvicorn is installed
    try:
        import uvicorn
    except ImportError:
        print("uvicorn is not installed. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "uvicorn[standard]"])

    # Start the server
    sys.path.insert(0, os.getcwd())
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=True)

if __name__ == "__main__":
    start_server()