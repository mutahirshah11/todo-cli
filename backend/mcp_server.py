from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import logging
from api.mcp.tools import add_task_tool, list_tasks_tool, update_task_tool, complete_task_tool, delete_task_tool

# Load environment variables
load_dotenv()

# Configure logging to stderr to avoid interfering with Stdio transport
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_server")

# Initialize FastMCP server
mcp = FastMCP("TodoMCP", dependencies=["mcp"])

@mcp.tool()
async def health_check() -> str:
    """Returns the health status of the MCP server."""
    return "OK"

# Register tools
mcp.tool(add_task_tool, name="add_task", description="Create a new task for a user")
mcp.tool(list_tasks_tool, name="list_tasks", description="List tasks for a user with optional filtering")
mcp.tool(update_task_tool, name="update_task", description="Update an existing task")
mcp.tool(complete_task_tool, name="complete_task", description="Mark a task as completed")
mcp.tool(delete_task_tool, name="delete_task", description="Delete (soft-delete) a task")

if __name__ == "__main__":
    logger.info("Starting TodoMCP Server...")
    # FastMCP.run() automatically handles Stdio transport
    mcp.run()
