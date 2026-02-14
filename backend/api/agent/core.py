import os
import logging
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from agents import Agent, Runner, set_tracing_disabled
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from api.agent.tools import add_task, list_tasks, update_task, delete_task, complete_task

# Configure logging
logger = logging.getLogger("agent_core")
logger.setLevel(logging.INFO)

# DEBUG LOGGING FUNCTION
def log_debug(message: str):
    try:
        with open("agent_debug.log", "a", encoding="utf-8") as f:
            f.write(f"{message}\n")
    except Exception:
        pass

# Disable tracing to prevent 401 errors with non-OpenAI keys
set_tracing_disabled(True)

# Initialize the AsyncOpenAI client for Gemini
gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY") or "MISSING_KEY"
gemini_key = gemini_key.strip().replace('"', '').replace("'", "")

client = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)

# Base instructions
BASE_INSTRUCTIONS = """You are a helpful task management assistant. 
Use the available tools to help the user manage their tasks. 
Always be polite and concise."""

async def process_request(message: str, history: List[Dict[str, Any]], user_id: str = "guest") -> str:
    """
    Process a request using the OpenAI Agents SDK Runner.
    """
    logger.info(f"Processing request for user: {user_id}")
    log_debug(f"CORE: process_request called for user_id={user_id}")
    
    try:
        # Construct input list from history + new message
        input_list = history + [{"role": "user", "content": message}]
        
        # We inject the user_id context directly into the agent's instructions
        # This is the most stable way to pass state to tools in the current SDK version
        # We use a very explicit marker
        current_instructions = f"{BASE_INSTRUCTIONS}\n\nCURRENT_USER_CONTEXT: {str(user_id)}\n\nEnd of Context"
        
        log_debug(f"CORE: Instructions prepared with user_id={user_id}")

        # Create a transient agent for this specific request
        # This ensures the context is perfectly isolated and stateless
        dynamic_agent = Agent(
            name="Task Assistant",
            instructions=current_instructions,
            tools=[add_task, list_tasks, update_task, delete_task, complete_task],
            model=model
        )
        
        logger.info("Starting Runner.run...")
        # Run the dynamic agent
        result = await Runner.run(dynamic_agent, input_list)
        logger.info("Runner.run completed successfully.")
        
        return result.final_output
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error in process_request: {error_msg}", exc_info=True)
        log_debug(f"CORE ERROR: {error_msg}")
        
        # Friendly handling for Rate Limits (Quota)
        if "429" in error_msg or "quota" in error_msg.lower():
            return "⚠️ System Busy: My AI brain (Gemini) has reached its free usage limit for today. Please try again in a few minutes or check your API quota."
            
        return f"Error: {error_msg}"