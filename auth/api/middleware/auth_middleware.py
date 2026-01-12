from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any

from ..utils.jwt import verify_token, get_current_user_id
from ..models.user import UserPublic

security = HTTPBearer()


async def get_current_user_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Dependency to get current user from JWT token.
    Verifies the token and returns the user payload.
    """
    token = credentials.credentials
    try:
        payload = verify_token(token)
        return payload
    except HTTPException:
        raise


async def get_current_user_id_from_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to get current user ID from JWT token.
    Verifies the token and returns the user ID.
    """
    token = credentials.credentials
    try:
        user_id = get_current_user_id(token)
        return user_id
    except HTTPException:
        raise


def verify_user_owns_resource(user_id: str, resource_owner_id: str):
    """
    Verify that the authenticated user owns the resource.
    Raises 403 Forbidden if the user doesn't own the resource.
    """
    if user_id != resource_owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )