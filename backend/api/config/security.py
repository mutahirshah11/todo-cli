"""
Security configuration for the Todo API.
Includes secure headers, CORS settings, and other security measures.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ..config.settings import settings


def configure_cors(app: FastAPI):
    """
    Configure CORS middleware with security in mind.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.get_allowed_origins(),
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
        # Prevent wildcard for credentials
        allow_origin_regex=None,  # Only allow explicit origins when credentials are allowed
    )


def add_security_middleware(app: FastAPI):
    """
    Add all security-related middleware to the application.
    """
    configure_cors(app)