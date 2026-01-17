#!/usr/bin/env python3
"""
Start the Backend Service
"""

import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

import uvicorn
import argparse


def main():
    parser = argparse.ArgumentParser(description='Start the Backend Service')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to (default: 8000)')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload (development)')

    args = parser.parse_args()

    print("Starting Backend Service on port 8000...")

    # Start the Uvicorn server
    uvicorn.run(
        "main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )


if __name__ == "__main__":
    main()