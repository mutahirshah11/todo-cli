#!/bin/bash
# Start the FastAPI server

echo "Starting Todo API server..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000