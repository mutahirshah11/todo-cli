# OpenAI Agents SDK Reference

## Installation

```bash
pip install openai-agents
```

Requires Python 3.10+

## Agent Class

```python
from agents import Agent

agent = Agent(
    name: str,                    # Required: Agent identifier
    instructions: str | Callable, # Required: System prompt or function returning prompt
    tools: list = [],             # Function tools available to agent
    handoffs: list = [],          # Agents this agent can transfer to
    model: str = "gpt-4o",        # Model to use
    model_settings: ModelSettings = None,  # Temperature, top_p, etc.
)
```

### ModelSettings

```python
from agents import ModelSettings

settings = ModelSettings(
    temperature=0.7,
    top_p=1.0,
    max_tokens=4096,
    presence_penalty=0.0,
    frequency_penalty=0.0,
)

agent = Agent(
    name="Creative",
    instructions="Be creative",
    model_settings=settings
)
```

## Runner Class

### run_sync (Synchronous)

```python
from agents import Runner

result = Runner.run_sync(
    agent: Agent,                 # Starting agent
    input: str | list,            # User message or message list
    context_variables: dict = {}, # Shared state across agents
    max_turns: int = None,        # Limit conversation turns
)
```

**Returns `RunResult`:**
```python
result.final_output    # str: Last assistant message
result.last_agent      # Agent: Final active agent
result.new_items       # list: All generated items
result.context_variables  # dict: Updated context
```

### run (Async)

```python
result = await Runner.run(
    agent=agent,
    input="Hello",
    context_variables={"user_id": "123"}
)
```

### run_streamed (Streaming)

```python
result = Runner.run_streamed(
    agent=agent,
    input="Tell me a story"
)

async for event in result.stream_events():
    if event.type == "raw_response_event":
        # Token-by-token output
        pass
    elif event.type == "agent_updated_stream_event":
        # Handoff occurred
        pass
    elif event.type == "run_item_stream_event":
        # Tool call or result
        pass
```

## Function Tools

### @function_tool Decorator

```python
from agents import function_tool

@function_tool
def my_tool(arg1: str, arg2: int = 10) -> str:
    """Tool description used by the model.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2 (optional)
    """
    return "result"
```

**Decorator Options:**
```python
@function_tool(
    name_override="custom_name",           # Override function name
    description_override="Custom desc",    # Override docstring
    use_docstring_info=True,               # Parse docstring (default True)
    failure_error_function=error_handler,  # Custom error handler
    strict_json_schema=True,               # Strict schema validation
)
```

### Supported Docstring Formats

- Google style (default)
- Sphinx style
- NumPy style

### Context Access in Tools

```python
from agents import function_tool, RunContextWrapper

@function_tool
def tool_with_context(ctx: RunContextWrapper, query: str) -> str:
    """Tool that accesses context."""
    user_id = ctx.context_variables.get("user_id")
    return f"Result for {user_id}: {query}"
```

### Manual FunctionTool

```python
from agents import FunctionTool
from pydantic import BaseModel

class MyArgs(BaseModel):
    query: str
    limit: int = 10

async def run_tool(ctx, args_json: str) -> str:
    args = MyArgs.model_validate_json(args_json)
    return f"Query: {args.query}, Limit: {args.limit}"

tool = FunctionTool(
    name="my_tool",
    description="Search for items",
    params_json_schema=MyArgs.model_json_schema(),
    on_invoke_tool=run_tool,
)
```

## Handoffs

### Basic Handoff

```python
agent_a = Agent(name="A", instructions="...", handoffs=[agent_b])
# Model can call transfer_to_b to switch
```

### Custom Handoff

```python
from agents import handoff

custom_handoff = handoff(
    agent=target_agent,
    tool_name_override="escalate_to_specialist",
    tool_description_override="Transfer for complex issues",
    on_handoff=lambda ctx: log_handoff(ctx),
    input_filter=lambda input: filter_sensitive(input),
)

agent = Agent(name="Support", handoffs=[custom_handoff])
```

### Nested Handoffs (Beta)

```python
from agents import RunConfig

config = RunConfig(
    nest_handoff_history=True,  # Summarize prior conversation
    handoff_input_filter=my_filter,  # Global input filter
)

result = Runner.run_sync(agent, "Hello", run_config=config)
```

## Guardrails

### Input Guardrail

```python
from agents import Agent, input_guardrail, GuardrailFunctionOutput

@input_guardrail
async def check_input(ctx, agent, input):
    if "forbidden" in input.lower():
        return GuardrailFunctionOutput(
            output_info={"reason": "Forbidden content"},
            tripwire_triggered=True
        )
    return GuardrailFunctionOutput(
        output_info={"status": "ok"},
        tripwire_triggered=False
    )

agent = Agent(
    name="Safe Agent",
    instructions="...",
    input_guardrails=[check_input]
)
```

### Output Guardrail

```python
from agents import output_guardrail

@output_guardrail
async def check_output(ctx, agent, output):
    # Validate agent output
    return GuardrailFunctionOutput(
        output_info={"validated": True},
        tripwire_triggered=False
    )

agent = Agent(
    name="Validated Agent",
    output_guardrails=[check_output]
)
```

## Built-in Tools

```python
from agents.tools import WebSearchTool, FileSearchTool, CodeInterpreterTool

agent = Agent(
    name="Research Agent",
    instructions="Search and analyze",
    tools=[
        WebSearchTool(),           # Web search
        FileSearchTool(vector_store_ids=["vs_123"]),  # Vector search
        CodeInterpreterTool(),     # Execute code
    ]
)
```

## Tracing

```python
from agents import trace

with trace("my-workflow"):
    result = Runner.run_sync(agent, "Do task")
    # All events logged under this trace
```

## Error Handling

```python
from agents import AgentsException, InputGuardrailTripwireTriggered

try:
    result = Runner.run_sync(agent, input)
except InputGuardrailTripwireTriggered as e:
    print(f"Input blocked: {e.guardrail_result.output_info}")
except AgentsException as e:
    print(f"Agent error: {e}")
```

## Official Resources

- Documentation: https://openai.github.io/openai-agents-python/
- Platform Guide: https://platform.openai.com/docs/guides/agents-sdk
- GitHub: https://github.com/openai/openai-agents-python
- Original Swarm (educational): https://github.com/openai/swarm
