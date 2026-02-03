from mcp.server.fastmcp import FastMCP
import pytest

def test_mcp_server_initialization():
    """Test that the MCP server initializes correctly."""
    mcp = FastMCP("TodoMCP")
    assert mcp.name == "TodoMCP"
