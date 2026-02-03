import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4
from datetime import datetime
from api.mcp.tools import update_task_tool, complete_task_tool, delete_task_tool
from api.models.task import TaskResponse

@pytest.mark.asyncio
async def test_update_task_tool_success():
    user_id = str(uuid4())
    task_id = str(uuid4())
    title = "Updated Task"
    
    mock_task_response = TaskResponse(
        id=task_id,
        title=title,
        description="Desc",
        completed=False,
        user_id=user_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    mock_session = AsyncMock()
    
    with patch("api.mcp.tools.get_mcp_session") as mock_get_session, \
         patch("api.mcp.tools.TaskAdapter") as mock_adapter_cls:
        
        mock_get_session.return_value.__aenter__.return_value = mock_session
        
        mock_adapter_instance = mock_adapter_cls.return_value
        mock_adapter_instance.update_task = AsyncMock(return_value=mock_task_response)

        result = await update_task_tool(user_id=user_id, task_id=task_id, title=title)
        
        assert title in result
        assert "success" in result.lower() or "id" in result

@pytest.mark.asyncio
async def test_complete_task_tool_success():
    user_id = str(uuid4())
    task_id = str(uuid4())
    
    mock_task_response = TaskResponse(
        id=task_id,
        title="Task",
        description="Desc",
        completed=True,
        user_id=user_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    mock_session = AsyncMock()
    
    with patch("api.mcp.tools.get_mcp_session") as mock_get_session, \
         patch("api.mcp.tools.TaskAdapter") as mock_adapter_cls:
        
        mock_get_session.return_value.__aenter__.return_value = mock_session
        
        mock_adapter_instance = mock_adapter_cls.return_value
        mock_adapter_instance.toggle_completion = AsyncMock(return_value=mock_task_response)

        result = await complete_task_tool(user_id=user_id, task_id=task_id)
        
        assert "completed" in result.lower() or "true" in result.lower()

@pytest.mark.asyncio
async def test_delete_task_tool_success():
    user_id = str(uuid4())
    task_id = str(uuid4())
    
    mock_session = AsyncMock()
    
    with patch("api.mcp.tools.get_mcp_session") as mock_get_session, \
         patch("api.mcp.tools.TaskAdapter") as mock_adapter_cls:
        
        mock_get_session.return_value.__aenter__.return_value = mock_session
        
        mock_adapter_instance = mock_adapter_cls.return_value
        mock_adapter_instance.delete_task = AsyncMock(return_value=True)

        result = await delete_task_tool(user_id=user_id, task_id=task_id)
        
        assert "deleted" in result.lower() or "success" in result.lower()

@pytest.mark.asyncio
async def test_update_task_unauthorized():
    """Test updating a task that doesn't exist or isn't owned by user returns error."""
    user_id = str(uuid4())
    task_id = str(uuid4())
    
    mock_session = AsyncMock()
    
    with patch("api.mcp.tools.get_mcp_session") as mock_get_session, \
         patch("api.mcp.tools.TaskAdapter") as mock_adapter_cls:
        
        mock_get_session.return_value.__aenter__.return_value = mock_session
        
        mock_adapter_instance = mock_adapter_cls.return_value
        mock_adapter_instance.update_task = AsyncMock(return_value=None) # None indicates not found/auth error

        result = await update_task_tool(user_id=user_id, task_id=task_id, title="New")
        
        assert "Error" in result
        assert "not found" in result.lower() or "unauthorized" in result.lower()
