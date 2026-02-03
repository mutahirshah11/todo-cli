import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from datetime import datetime
from api.mcp.tools import add_task_tool
from api.models.task import TaskResponse

@pytest.mark.asyncio
async def test_add_task_tool_success():
    """Test add_task tool successfully creates a task."""
    user_id = str(uuid4())
    title = "Test Task"
    description = "Test Description"
    
    mock_task_response = TaskResponse(
        id=uuid4(),
        title=title,
        description=description,
        completed=False,
        user_id=user_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    # Mock the session context manager
    mock_session = AsyncMock()
    
    # Mock the TaskAdapter
    with patch("api.mcp.tools.get_mcp_session") as mock_get_session, \
         patch("api.mcp.tools.TaskAdapter") as mock_adapter_cls:
        
        # Setup session mock
        mock_get_session.return_value.__aenter__.return_value = mock_session
        
        # Setup adapter mock
        mock_adapter_instance = mock_adapter_cls.return_value
        # Configure create_task to be an async method returning the response
        mock_adapter_instance.create_task = AsyncMock(return_value=mock_task_response)

        # Call the tool
        result = await add_task_tool(user_id=user_id, title=title, description=description)
        
        # Verify JSON response contains expected fields
        assert str(mock_task_response.id) in result
        assert title in result
        assert "created" in result.lower() or "success" in result.lower() or "id" in result

@pytest.mark.asyncio
async def test_add_task_tool_validation_error():
    """Test add_task tool handles empty title."""
    user_id = str(uuid4())
    title = ""  # Invalid
    
    # We expect the tool to return a formatted error string
    result = await add_task_tool(user_id=user_id, title=title)
    assert "Error" in result
    assert "required" in result.lower()

@pytest.mark.asyncio
async def test_add_task_tool_missing_user_id():
    """Test add_task tool handles missing user_id."""
    user_id = ""  # Invalid
    title = "Valid Title"
    
    result = await add_task_tool(user_id=user_id, title=title)
    assert "Error" in result
    assert "required" in result.lower()