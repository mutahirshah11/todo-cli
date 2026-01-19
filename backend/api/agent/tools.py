from typing import Optional, Literal
from pydantic import BaseModel, Field
from agents import function_tool

# --- Add Task ---
class AddTaskArgs(BaseModel):
    title: str = Field(..., description="The title of the task")
    description: Optional[str] = Field(None, description="Additional details about the task")
    due_date: Optional[str] = Field(None, description="ISO-8601 date string for the deadline")

async def add_task_impl(args: AddTaskArgs) -> str:
    """Create a new task with the given details."""
    return f"Task '{args.title}' added."

@function_tool
async def add_task(args: AddTaskArgs) -> str:
    return await add_task_impl(args)

# --- List Tasks ---
class ListTasksArgs(BaseModel):
    status: Optional[Literal["pending", "completed"]] = Field(None, description="Filter tasks by status. If omitted, returns all tasks.")

async def list_tasks_impl(args: ListTasksArgs) -> str:
    """List tasks, optionally filtered by status."""
    if args.status:
        return f"Listing {args.status} tasks: 1. Mock Task"
    return "Listing all tasks: 1. Mock Task"

@function_tool
async def list_tasks(args: ListTasksArgs) -> str:
    return await list_tasks_impl(args)

# --- Update Task ---
class UpdateTaskArgs(BaseModel):
    task_id: int = Field(..., description="The ID of the task to update")
    title: Optional[str] = Field(None, description="New title")
    description: Optional[str] = Field(None, description="New description")
    status: Optional[Literal["pending", "completed"]] = Field(None, description="New status")
    due_date: Optional[str] = Field(None, description="New due date")

async def update_task_impl(args: UpdateTaskArgs) -> str:
    """Update an existing task."""
    return f"Task {args.task_id} updated."

@function_tool
async def update_task(args: UpdateTaskArgs) -> str:
    return await update_task_impl(args)

# --- Delete Task ---
class DeleteTaskArgs(BaseModel):
    task_id: int = Field(..., description="The ID of the task to delete")

async def delete_task_impl(args: DeleteTaskArgs) -> str:
    """Delete a task by ID."""
    return f"Task {args.task_id} deleted."

@function_tool
async def delete_task(args: DeleteTaskArgs) -> str:
    return await delete_task_impl(args)

# --- Complete Task ---
class CompleteTaskArgs(BaseModel):
    task_id: int = Field(..., description="The ID of the task to complete")

async def complete_task_impl(args: CompleteTaskArgs) -> str:
    """Mark a task as completed."""
    return f"Task {args.task_id} marked as completed."

@function_tool
async def complete_task(args: CompleteTaskArgs) -> str:
    return await complete_task_impl(args)