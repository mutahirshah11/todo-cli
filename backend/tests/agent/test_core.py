import pytest
from unittest.mock import AsyncMock, patch
from backend.api.agent.core import process_request
from backend.api.agent.models import AgentRequest

@pytest.mark.asyncio
async def test_process_request_delegation():
    with patch("backend.api.agent.core.Runner.run", new_callable=AsyncMock) as mock_run:
        mock_result = AsyncMock()
        mock_result.final_output = "Task added."
        mock_run.return_value = mock_result
        
        history = [{"role": "assistant", "content": "Hi"}]
        message = "Add task Buy milk"
        
        response = await process_request(message, history)
        
        assert response == "Task added."
        
        # Verify Runner was called with correct inputs
        args, _ = mock_run.call_args
        agent_arg = args[0]
        input_list = args[1]
        
        assert agent_arg.name == "Task Assistant"
        assert len(input_list) == 2
        assert input_list[0] == history[0]
        assert input_list[1] == {"role": "user", "content": "Add task Buy milk"}
