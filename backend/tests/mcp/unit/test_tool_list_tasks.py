import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4
from datetime import datetime
from api.mcp.tools import list_tasks_tool
from api.models.task import TaskResponse

@pytest.mark.asyncio
async def test_list_tasks_tool_success():
    """Test list_tasks tool successfully retrieves tasks."""
    user_id = str(uuid4())
    
    mock_tasks = [
        TaskResponse(
            id=uuid4(),
            title="Task 1",
            description="Desc 1",
            completed=False,
            user_id=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        TaskResponse(
            id=uuid4(),
            title="Task 2",
            description="Desc 2",
            completed=True,
            user_id=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    ]

    mock_session = AsyncMock()
    
    with patch("api.mcp.tools.get_mcp_session") as mock_get_session, \
         patch("api.mcp.tools.TaskAdapter") as mock_adapter_cls:
        
        mock_get_session.return_value.__aenter__.return_value = mock_session
        
        mock_adapter_instance = mock_adapter_cls.return_value
        # Default behavior for get_all_tasks
        mock_adapter_instance.get_all_tasks = AsyncMock(return_value=mock_tasks)

        result = await list_tasks_tool(user_id=user_id)
        
        assert "Task 1" in result
        assert "Task 2" in result

@pytest.mark.asyncio
async def test_list_tasks_tool_with_filter():
    """Test list_tasks tool calls adapter with correct filter."""
    user_id = str(uuid4())
    status = "completed"
    
    mock_session = AsyncMock()
    
    with patch("api.mcp.tools.get_mcp_session") as mock_get_session, \
         patch("api.mcp.tools.TaskAdapter") as mock_adapter_cls:
        
        mock_get_session.return_value.__aenter__.return_value = mock_session
        
        mock_adapter_instance = mock_adapter_cls.return_value
        # We expect a new method or modified existing method
        mock_adapter_instance.get_tasks_by_status = AsyncMock(return_value=[])
        
        await list_tasks_tool(user_id=user_id, status=status)
        
        # Verify specific method was called
        mock_adapter_instance.get_tasks_by_status.assert_called_once_with(True) # completed=True