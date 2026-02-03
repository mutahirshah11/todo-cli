from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from api.agent.core import process_request
from api.utils.jwt_validator import get_current_user_id_from_token_dep
import logging

logger = logging.getLogger("uvicorn")
router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, Any]]
    user_id: Optional[str] = None # Optional now, we prefer token

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user_id_from_token_dep)
):
    """
    Endpoint for the AI Chatbot to process messages.
    Requires Authentication.
    """
    logger.info(f"--- Chat Request Start ---")
    logger.info(f"Authenticated User ID (from Token): {current_user_id}")
    
    # Log mismatch for debugging
    if request.user_id and request.user_id != current_user_id:
        logger.warning(f"Frontend sent user_id {request.user_id} which differs from Token ID {current_user_id}. Using Token ID.")
    
    logger.info(f"Message: {request.message}")
    
    try:
        # process_request handles the logic using OpenAI Agents SDK
        logger.info("Calling process_request...")
        # ALWAYS use the trusted ID from token
        response_text = await process_request(request.message, request.history, current_user_id)
        logger.info(f"Response received: {response_text[:50]}...")
        return ChatResponse(response=response_text)
    except Exception as e:
        logger.error(f"FATAL Agent error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        logger.info(f"--- Chat Request End ---")
