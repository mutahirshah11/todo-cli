#!/usr/bin/env python3
"""
Start the standalone Authentication Service
"""

import uvicorn
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description='Start the Authentication Service')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8001, help='Port to bind to (default: 8001)')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload (development)')

    args = parser.parse_args()

    # Start the Uvicorn server
    uvicorn.run(
        "app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )


if __name__ == "__main__":
    main()