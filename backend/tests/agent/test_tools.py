import pytest
from backend.api.agent.tools import add_task_impl, AddTaskArgs, list_tasks_impl, ListTasksArgs

@pytest.mark.asyncio
async def test_add_task_tool():
    args = AddTaskArgs(title="Buy milk")
    result = await add_task_impl(args)
    assert "Task 'Buy milk' added" in result

@pytest.mark.asyncio
async def test_list_tasks_tool():
    args = ListTasksArgs(status="pending")
    result = await list_tasks_impl(args)
    assert "Listing pending tasks" in result