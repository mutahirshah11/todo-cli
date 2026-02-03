import pytest
import asyncio
from typing import AsyncGenerator
from dotenv import load_dotenv
import os

# Load environment variables for tests
load_dotenv()

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()