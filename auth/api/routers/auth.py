from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import Response

from ..models.user import UserCreate, UserPublic, Token, LoginRequest
from ..services.auth_service import AuthService
from ..middleware.auth_middleware import security
from ..exceptions.auth_exceptions import InvalidCredentialsException

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
        print(f"Register request received: {user_create.email}")  # Debug logging
        user_public, access_token = auth_service.register_user(user_create)

        return {
            "user": user_public.model_dump(),
            "access_token": access_token,
            "token_type": "bearer"
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Handle other exceptions
        print(f"Registration error: {str(e)}")  # Debug logging
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=dict)
async def login(login_request: LoginRequest):
    """
    Authenticate user with email and password.
    Returns user information and access token.
    """
    try:
        user_public, access_token = auth_service.authenticate_user(
            login_request.email.strip(),
            login_request.password
        )

        return {
            "user": user_public.model_dump(),
            "access_token": access_token,
            "token_type": "bearer"
        }
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log the actual error for debugging
        print(f"Login error: {str(e)}")
        # Return a generic server error instead of 401 for non-auth failures
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed due to server error: {str(e)}"
        )


@router.get("/me", response_model=UserPublic)
async def get_current_user(token_credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get current authenticated user information.
    Requires valid JWT token in Authorization header.
    """
    token = token_credentials.credentials
    return auth_service.get_current_user(token)