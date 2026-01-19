import os
from typing import List, Dict, Any
from openai import AsyncOpenAI
from agents import Agent, Runner, set_tracing_disabled
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from backend.api.agent.tools import add_task, list_tasks, update_task, delete_task, complete_task

# Disable tracing to prevent 401 errors with non-OpenAI keys
set_tracing_disabled(True)

# Initialize the AsyncOpenAI client for Gemini
# Note: In production, ensure GEMINI_API_KEY is set in environment.
gemini_key = os.getenv("GEMINI_API_KEY") or "MISSING_KEY"
client = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Initialize the OpenAIChatCompletionsModel using the client
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)

# Initialize the agent using the official SDK syntax
agent = Agent(
    name="Task Assistant",
    instructions="You are a helpful task management assistant. Use the available tools to help the user manage their tasks. Always confirm actions.",
    tools=[add_task, list_tasks, update_task, delete_task, complete_task],
    model=model
)

async def process_request(message: str, history: List[Dict[str, Any]]) -> str:
    """
    Process a request using the OpenAI Agents SDK Runner.
    
    Args:
        message: The user's new message.
        history: List of previous messages (role, content).
    
    Returns:
        The assistant's response.
    """
    # Construct input list from history + new message
    input_list = history + [{"role": "user", "content": message}]
    
    # Run the agent using the Runner
    result = await Runner.run(agent, input_list)
    return result.final_output