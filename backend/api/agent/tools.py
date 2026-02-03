from typing import Optional, Literal, List, Dict, Any
from pydantic import BaseModel, Field
from agents import function_tool, TContext
from api.database.session import AsyncSessionLocal
from api.services.task_adapter import TaskAdapter
from api.models.task import TaskCreate, TaskUpdate, TaskToggle
import logging
import re
import os

logger = logging.getLogger(__name__)

# ... (imports)

# DEBUG LOGGING FUNCTION
def log_debug(message: str):
    try:
        with open("agent_debug.log", "a", encoding="utf-8") as f:
            f.write(f"{message}\n")
    except Exception:
        pass

# --- SYNC FIX: Extract user_id from Agent Context ---
def get_user_id_from_context(context: Any) -> str:
    """
    Extracts the User ID from the context.
    Handles both TContext object and direct string (if passed that way).
    """
    try:
        log_debug(f"DEBUG: context type: {type(context)}")
        
        instructions = ""
        
        # Case 1: context is TContext object (has .agent)
        if hasattr(context, "agent") and hasattr(context.agent, "instructions"):
            instructions = context.agent.instructions
            log_debug("DEBUG: Extracted instructions from context.agent")
            
        # Case 2: context is the Agent object directly (has .instructions)
        elif hasattr(context, "instructions"):
            instructions = context.instructions
            log_debug("DEBUG: Extracted instructions from context directly")
            
        # Case 3: context is a string (maybe the instructions themselves?)
        elif isinstance(context, str):
            instructions = context
            log_debug("DEBUG: Context is a string")
            
        # Case 4: Context is a dict (maybe serialized state?)
        elif isinstance(context, dict):
            log_debug(f"DEBUG: Context is a dict: {context.keys()}")
            # Check if instructions are in the dict
            if "agent" in context and "instructions" in context["agent"]:
                 instructions = context["agent"]["instructions"]
            elif "instructions" in context:
                 instructions = context["instructions"]

        log_debug(f"DEBUG: Content length: {len(instructions)}")
        if len(instructions) < 100:
             log_debug(f"DEBUG: Content preview: {instructions}")

        # CHECK 1: Is the content ITSELF a UUID? (Length 36 is standard UUID)
        clean_content = instructions.strip().replace('"', '').replace("'", "")
        if len(clean_content) == 36 and "-" in clean_content:
             log_debug(f"DEBUG: Content looks like a UUID. Returning directly: {clean_content}")
             return clean_content

        # CHECK 2: Look for the marker
        marker = "CURRENT_USER_CONTEXT:"
        if marker in instructions:
            parts = instructions.split(marker)
            if len(parts) > 1:
                after_marker = parts[1].strip()
                uid = after_marker.split('\n')[0].strip()
                # Clean up any trailing punctuation if extraction is messy
                uid = uid.strip('.,;:"\'')
                log_debug(f"DEBUG: Found User ID via marker: {uid}")
                return uid
        
        log_debug("DEBUG: Marker not found in instructions and content is not a UUID.")
        
    except Exception as e:
        logger.error(f"Failed to extract user_id from context: {e}")
        log_debug(f"DEBUG: Error extracting User ID: {e}")
    
    # Fallback
    log_debug("DEBUG: Using Fallback User ID.")
    return "00000000-0000-0000-0000-000000000000"
# ... (rest of file)

async def get_adapter(user_id: str):
    session = AsyncSessionLocal()
    return TaskAdapter(session, user_id), session

# --- Add Task ---
class AddTaskArgs(BaseModel):
    title: str = Field(..., description="The title of the task")
    description: Optional[str] = Field("", description="Details")

@function_tool
async def add_task(args: AddTaskArgs, context: TContext) -> str:
    """Create a new task on the dashboard."""
    user_id = get_user_id_from_context(context)
    log_debug(f"TOOL: add_task called for user {user_id} with title '{args.title}'")
    
    adapter, session = await get_adapter(user_id)
    try:
        task_create = TaskCreate(title=args.title, description=args.description or "")
        result = await adapter.create_task(task_create)
        await session.commit()
        return f"SUCCESS: Added '{result.title}' to your dashboard."
    except Exception as e:
        await session.rollback()
        log_debug(f"TOOL ERROR: add_task failed: {e}")
        return f"ERROR: {str(e)}"
    finally:
        await session.close()

# --- List Tasks ---
class ListTasksArgs(BaseModel):
    status: Optional[Literal["pending", "completed"]] = Field(None, description="Filter")

@function_tool
async def list_tasks(args: ListTasksArgs, context: TContext) -> str:
    """List dashboard tasks. Use this to see current tasks."""
    user_id = get_user_id_from_context(context)
    log_debug(f"TOOL: list_tasks called for user {user_id}")
    
    adapter, session = await get_adapter(user_id)
    try:
        if args.status == "completed":
            tasks = await adapter.get_tasks_by_status(True)
        elif args.status == "pending":
            tasks = await adapter.get_tasks_by_status(False)
        else:
            tasks = await adapter.get_all_tasks()
        
        log_debug(f"TOOL: Found {len(tasks)} tasks")
        
        if not tasks:
            return "Dashboard is empty."
        
        items = []
        for i, t in enumerate(tasks, 1):
            status_icon = "✅" if t.completed else "⏳"
            items.append(f"{i}. {status_icon} {t.title}")
        
        return "Dashboard Tasks:\n" + "\n".join(items)
    except Exception as e:
        log_debug(f"TOOL ERROR: list_tasks failed: {e}")
        return f"ERROR: {str(e)}"
    finally:
        await session.close()

# --- Smart Action Args ---
class SmartActionArgs(BaseModel):
    identifier: str = Field(..., description="The Number (1, 2, 3) or Task Title")

class SmartUpdateArgs(SmartActionArgs):
    title: Optional[str] = Field(None, description="New title")
    description: Optional[str] = Field(None, description="New description")

@function_tool
async def update_task(args: SmartUpdateArgs, context: TContext) -> str:
    """Update a task's title or description on the dashboard."""
    user_id = get_user_id_from_context(context)
    log_debug(f"TOOL: update_task called for user {user_id}")
    
    adapter, session = await get_adapter(user_id)
    try:
        tasks = await adapter.get_all_tasks()
        target_task = None
        
        if args.identifier.isdigit():
            idx = int(args.identifier) - 1
            if 0 <= idx < len(tasks):
                target_task = tasks[idx]
        
        if not target_task:
            for t in tasks:
                if t.title.lower() == args.identifier.lower():
                    target_task = t
                    break
        
        if target_task:
            task_update = TaskUpdate(title=args.title, description=args.description)
            result = await adapter.update_task(str(target_task.id), task_update)
            await session.commit()
            return f"SUCCESS: Task '{result.title}' updated on dashboard."
        
        return "ERROR: Task not found on dashboard."
    except Exception as e:
        await session.rollback()
        return f"ERROR: {str(e)}"
    finally:
        await session.close()

@function_tool
async def complete_task(args: SmartActionArgs, context: TContext) -> str:
    """Mark a dashboard task as completed."""
    user_id = get_user_id_from_context(context)
    log_debug(f"TOOL: complete_task called for user {user_id}")
    
    adapter, session = await get_adapter(user_id)
    try:
        tasks = await adapter.get_all_tasks()
        target_task = None
        
        if args.identifier.isdigit():
            idx = int(args.identifier) - 1
            if 0 <= idx < len(tasks):
                target_task = tasks[idx]
        
        if not target_task:
            for t in tasks:
                if t.title.lower() == args.identifier.lower():
                    target_task = t
                    break
        
        if target_task:
            result = await adapter.toggle_completion(str(target_task.id), TaskToggle(completed=True))
            await session.commit()
            return f"SUCCESS: Task marked as completed on dashboard."
        
        return "ERROR: Task not found on dashboard."
    except Exception as e:
        await session.rollback()
        return f"ERROR: {str(e)}"
    finally:
        await session.close()

@function_tool
async def delete_task(args: SmartActionArgs, context: TContext) -> str:
    """Remove a task from the dashboard."""
    user_id = get_user_id_from_context(context)
    log_debug(f"TOOL: delete_task called for user {user_id}")
    
    adapter, session = await get_adapter(user_id)
    try:
        tasks = await adapter.get_all_tasks()
        target_id = None
        
        if args.identifier.isdigit():
            idx = int(args.identifier) - 1
            if 0 <= idx < len(tasks):
                target_id = str(tasks[idx].id)
        
        if not target_id:
            for t in tasks:
                if t.title.lower() == args.identifier.lower():
                    target_id = str(t.id)
                    break
        
        if target_id:
            success = await adapter.delete_task(target_id)
            await session.commit()
            return "SUCCESS: Removed from dashboard."
        
        return "ERROR: Task not found."
    except Exception as e:
        await session.rollback()
        return f"ERROR: {str(e)}"
    finally:
        await session.close()
