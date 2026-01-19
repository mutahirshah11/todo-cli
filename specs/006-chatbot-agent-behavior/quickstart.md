# Quickstart - AI Agent Behavior (Phase 3.1)

## Prerequisites

- Python 3.10+
- Gemini API Key

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install openai pytest pydantic python-dotenv
    ```

2.  **Environment Variables**:
    Create a `.env` file in the root:
    ```env
    GEMINI_API_KEY=your_gemini_key_here
    ```

## Running Tests

Execute the strict TDD test suite:

```bash
pytest tests/agent/test_agent_behavior.py
```

## Running the Agent Locally

(After implementation)

```python
import asyncio
from src.agent.core import Agent

async def main():
    agent = Agent()
    response = await agent.process_request(
        user_id="test_user",
        message="Add a task to buy milk",
        history=[]
    )
    print(response.content)

if __name__ == "__main__":
    asyncio.run(main())
```
