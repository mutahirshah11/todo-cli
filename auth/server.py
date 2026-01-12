"""
Standalone Authentication Service using Better Auth
This service handles all authentication-related functionality separately
"""

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

# Initialize auth service
auth_service = AuthService()

@app.post("/auth/register", response_model=dict)
async def register(user_create: UserCreate):
    """
    Register a new user account.
    Creates a new user with the provided email and password.
    Returns user information and access token.
    """
    try:
        user_public, access_token = auth_service.register_user(user_create)

        return {
            "user": user_public.dict(),
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@app.post("/auth/login", response_model=dict)
async def login(login_request: LoginRequest):
    """
    Authenticate user with email and password.
    Returns user information and access token.
    """
    try:
        user_public, access_token = auth_service.authenticate_user(
            login_request.email,
            login_request.password
        )

        return {
            "user": user_public.dict(),
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/auth/me", response_model=UserPublic)
async def get_current_user(token_credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get current authenticated user information.
    Requires valid JWT token in Authorization header.
    """
    token = token_credentials.credentials
    return auth_service.get_current_user(token)


@app.get("/health")
async def health_check():
    """Health check endpoint for the auth service."""
    return {"status": "auth service healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)