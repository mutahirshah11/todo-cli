from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import Response

from ..models.user import UserCreate, UserPublic, Token, LoginRequest
from ..services.auth_service import AuthService
from ..middleware.auth_middleware import security

router = APIRouter(prefix="/auth", tags=["Authentication"])

auth_service = AuthService()




@router.post("/register", response_model=dict)
async def register(user_create: UserCreate):
    """
    Register a new user account.
    Creates a new user with the provided email and password.
    Returns user information and access token.
    """
    try:
        user_public, access_token = auth_service.register_user(user_create)

        return {
            "user": user_public.model_dump(),
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/login", response_model=dict)
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
            "user": user_public.model_dump(),
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserPublic)
async def get_current_user(token_credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get current authenticated user information.
    Requires valid JWT token in Authorization header.
    """
    token = token_credentials.credentials
    return auth_service.get_current_user(token)