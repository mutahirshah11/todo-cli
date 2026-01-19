from typing import List, Optional, Any, Dict
from pydantic import BaseModel

class AgentRequest(BaseModel):
    user_id: str
    message: str
    history: List[Dict[str, Any]] = []

class AgentResponse(BaseModel):
    content: str
