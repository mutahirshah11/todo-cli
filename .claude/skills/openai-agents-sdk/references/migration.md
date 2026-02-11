# Swarm to Agents SDK Migration

The OpenAI Agents SDK is the production-ready successor to Swarm (experimental).

## Key Differences

| Aspect | Swarm (Legacy) | Agents SDK |
|--------|----------------|------------|
| Status | Experimental/Educational | Production-ready |
| Package | `git+https://github.com/openai/swarm.git` | `openai-agents` |
| Import | `from swarm import Swarm, Agent` | `from agents import Agent, Runner` |
| Orchestrator | `Swarm()` client | `Runner` class |
| Run method | `client.run()` | `Runner.run_sync()` / `Runner.run()` |
| Guardrails | Not included | Built-in input/output validation |
| Tracing | Not included | Built-in tracing |
| Tools | Functions list | `@function_tool` decorator + built-ins |

## Migration Steps

### 1. Update Imports

```python
# Before (Swarm)
from swarm import Swarm, Agent

# After (Agents SDK)
from agents import Agent, Runner, function_tool
```

### 2. Agent Definition

```python
# Before (Swarm)
agent = Agent(
    name="Helper",
    instructions="Be helpful",
    functions=[my_function]
)

# After (Agents SDK)
@function_tool
def my_function(arg: str) -> str:
    """Description."""
    return "result"

agent = Agent(
    name="Helper",
    instructions="Be helpful",
    tools=[my_function]
)
```

### 3. Running Agents

```python
# Before (Swarm)
client = Swarm()
response = client.run(
    agent=agent,
    messages=[{"role": "user", "content": "Hello"}],
    context_variables={"user_id": "123"}
)
print(response.messages[-1]["content"])

# After (Agents SDK)
result = Runner.run_sync(
    agent,
    input="Hello",
    context_variables={"user_id": "123"}
)
print(result.final_output)
```

### 4. Function Definitions

```python
# Before (Swarm) - Plain functions
def get_weather(location, context_variables):
    """Get weather for a location."""
    user = context_variables.get("user_id")
    return f"Weather for {location}"

# After (Agents SDK) - Decorated with context wrapper
from agents import function_tool, RunContextWrapper

@function_tool
def get_weather(ctx: RunContextWrapper, location: str) -> str:
    """Get weather for a location.

    Args:
        location: City name to check weather
    """
    user = ctx.context_variables.get("user_id")
    return f"Weather for {location}"
```

### 5. Handoffs

```python
# Before (Swarm) - Return agent from function
def transfer_to_sales():
    return sales_agent

agent = Agent(
    name="Triage",
    functions=[transfer_to_sales]
)

# After (Agents SDK) - Use handoffs parameter
agent = Agent(
    name="Triage",
    instructions="Route to sales for purchase questions",
    handoffs=[sales_agent]
)
# SDK auto-generates transfer_to_sales_agent tool
```

### 6. Streaming

```python
# Before (Swarm)
response = client.run(agent=agent, messages=messages, stream=True)
for chunk in response:
    if "content" in chunk:
        print(chunk["content"], end="")

# After (Agents SDK)
from openai.types.responses import ResponseTextDeltaEvent

result = Runner.run_streamed(agent, input="Hello")
async for event in result.stream_events():
    if event.type == "raw_response_event":
        if isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
```

### 7. Context Variable Updates

```python
# Before (Swarm) - Return Result object
from swarm import Result

def update_context(context_variables):
    return Result(
        value="Updated",
        context_variables={"key": "new_value"}
    )

# After (Agents SDK) - Modify via context wrapper
@function_tool
def update_context(ctx: RunContextWrapper) -> str:
    ctx.context_variables["key"] = "new_value"
    return "Updated"
```

## New Features in Agents SDK

### Guardrails

```python
from agents import Agent, input_guardrail, GuardrailFunctionOutput

@input_guardrail
async def block_pii(ctx, agent, input):
    has_pii = detect_pii(input)
    return GuardrailFunctionOutput(
        output_info={"has_pii": has_pii},
        tripwire_triggered=has_pii
    )

agent = Agent(
    name="Safe Agent",
    input_guardrails=[block_pii]
)
```

### Built-in Tools

```python
from agents.tools import WebSearchTool, CodeInterpreterTool

agent = Agent(
    name="Research Agent",
    tools=[WebSearchTool(), CodeInterpreterTool()]
)
```

### Tracing

```python
from agents import trace

with trace("customer-support-flow"):
    result = Runner.run_sync(agent, "Help me")
    # All events captured for debugging
```

## Common Migration Issues

### Issue: Functions not being called

**Cause**: Missing or unclear docstrings
**Fix**: Add detailed docstrings - the SDK extracts descriptions from them

```python
@function_tool
def book_meeting(date: str, time: str) -> str:
    """Book a meeting at the specified date and time.

    Args:
        date: Meeting date in YYYY-MM-DD format
        time: Meeting time in HH:MM format (24-hour)
    """
    return "Meeting booked"
```

### Issue: Context not persisting

**Cause**: Not using `RunContextWrapper`
**Fix**: Add context parameter to functions that need it

```python
@function_tool
def my_tool(ctx: RunContextWrapper, arg: str) -> str:
    # Access context
    user = ctx.context_variables.get("user_id")
    # Update context
    ctx.context_variables["last_action"] = "my_tool"
    return f"Done for {user}"
```

### Issue: Handoffs not working

**Cause**: Using functions instead of handoffs parameter
**Fix**: Use the `handoffs` parameter

```python
# Wrong
def transfer():
    return other_agent

agent = Agent(tools=[transfer])

# Correct
agent = Agent(handoffs=[other_agent])
```

## Resources

- [Agents SDK Docs](https://openai.github.io/openai-agents-python/)
- [Platform Guide](https://platform.openai.com/docs/guides/agents-sdk)
- [Original Swarm](https://github.com/openai/swarm) (for reference only)
