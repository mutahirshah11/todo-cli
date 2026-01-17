"""
Standalone Authentication Service using Better Auth
This service handles all authentication-related functionality separately
"""

import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.utils.jwt import verify_token, get_current_user_id, create_access_token, get_password_hash, verify_password
from api.models.user import UserCreate, UserPublic, UserInDB, LoginRequest
from api.services.auth_service import AuthService

app = FastAPI(title="Authentication Service", version="1.0.0")

# Include auth router
from api.routers import auth
app.include_router(auth.router)

# Security scheme
security = HTTPBearer()

# Initialize auth service (no demo user creation)
auth_service = AuthService()



@app.get("/health")
async def health_check():
    """Health check endpoint for the auth service."""
    return {"status": "auth service healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)