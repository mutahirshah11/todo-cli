---
name: openai-agents-sdk
description: |
  Build multi-agent conversational systems using OpenAI Agents SDK (production-ready successor to Swarm).
  This skill should be used when building agent orchestration, implementing handoffs between specialized agents,
  defining function tools, managing context variables across agents, or optimizing token usage in agent conversations.
---

# OpenAI Agents SDK

Build multi-agent systems with handoffs, tool calling, and context management.

## Before Implementation

| Source | Gather |
|--------|--------|
| **Codebase** | Existing agent patterns, API structure, error handling conventions |
| **Conversation** | User's specific use case, agent specializations needed, integration requirements |
| **Skill References** | SDK patterns from `references/` (agent definition, handoffs, tools, streaming) |

## Quick Start

```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant"
)

result = Runner.run_sync(agent, "Hello!")
print(result.final_output)
```

## Core Concepts

### Agent Definition

```python
from agents import Agent

agent = Agent(
    name="Sales Agent",           # Identifier
    instructions="Help customers with purchases",  # System prompt
    tools=[check_inventory, process_order],        # Function tools
    handoffs=[support_agent, billing_agent],       # Agents to transfer to
    model="gpt-4o"                # Optional model override
)
```

**Dynamic Instructions** (with context variables):
```python
def get_instructions(context_variables):
    user = context_variables.get("user_name", "customer")
    return f"Help {user} with their purchase. Be friendly."

agent = Agent(
    name="Sales Agent",
    instructions=get_instructions
)
```

### Runner (Orchestration)

Three execution methods:

| Method | Use Case |
|--------|----------|
| `Runner.run()` | Async - FastAPI, event loops |
| `Runner.run_sync()` | Sync - scripts, CLI |
| `Runner.run_streamed()` | Real-time token streaming |

```python
from agents import Runner

# Synchronous
result = Runner.run_sync(agent, "Book appointment for tomorrow")
print(result.final_output)

# Async
result = await Runner.run(agent, input="Book appointment")

# With context variables
result = Runner.run_sync(
    agent,
    input="Check my orders",
    context_variables={"user_id": "123", "org_id": "456"}
)
```

### Handoffs

Transfer conversation between specialized agents:

```python
# Define specialized agents
refund_agent = Agent(
    name="Refund Agent",
    instructions="Process refund requests. Verify order, check policy, initiate refund."
)

support_agent = Agent(
    name="Support Agent",
    instructions="Handle technical issues and troubleshooting."
)

# Triage agent routes to specialists
triage_agent = Agent(
    name="Triage Agent",
    instructions="Route customer to appropriate specialist based on their request.",
    handoffs=[refund_agent, support_agent]
)

# Run - model automatically calls transfer_to_refund_agent or transfer_to_support_agent
result = Runner.run_sync(triage_agent, "I want a refund for order #123")
```

**Handoff with Context**:
```python
from agents import Agent, handoff

# Custom handoff with input filter
billing_handoff = handoff(
    agent=billing_agent,
    tool_name_override="escalate_to_billing",
    tool_description_override="Transfer to billing for payment issues",
    on_handoff=lambda ctx: print(f"Handing off with context: {ctx.context_variables}")
)

agent = Agent(
    name="Support",
    handoffs=[billing_handoff]
)
```

### Function Tools

```python
from agents import Agent, function_tool

@function_tool
def check_calendar(date: str, user_id: str) -> str:
    """Check calendar availability for a user.

    Args:
        date: Date to check (YYYY-MM-DD format)
        user_id: The user's ID
    """
    # Implementation
    return f"Available slots on {date}: 9am, 2pm, 4pm"

@function_tool
def book_appointment(date: str, time: str, user_id: str) -> str:
    """Book an appointment for the user.

    Args:
        date: Date for appointment (YYYY-MM-DD)
        time: Time slot (e.g., "9am")
        user_id: The user's ID
    """
    return f"Booked appointment on {date} at {time}"

agent = Agent(
    name="Scheduler",
    instructions="Help users schedule appointments",
    tools=[check_calendar, book_appointment]
)
```

**Tool with Context Access**:
```python
from agents import function_tool, RunContextWrapper

@function_tool
def get_user_orders(ctx: RunContextWrapper) -> str:
    """Get orders for current user."""
    user_id = ctx.context_variables.get("user_id")
    # Fetch orders for user_id
    return f"Orders for {user_id}: [order1, order2]"
```

**Error Handling in Tools**:
```python
def custom_error_handler(ctx: RunContextWrapper, error: Exception) -> str:
    return f"Tool failed: {str(error)}. Please try again."

@function_tool(failure_error_function=custom_error_handler)
def risky_operation(data: str) -> str:
    """Perform operation that might fail."""
    # Implementation
    pass
```

### Context Variables

Persist data across agents and tool calls:

```python
# Pass initial context
result = Runner.run_sync(
    agent,
    input="Help me",
    context_variables={
        "user_id": "user_123",
        "org_id": "org_456",
        "preferences": {"language": "en"}
    }
)

# Access in tools
@function_tool
def personalized_greeting(ctx: RunContextWrapper) -> str:
    user = ctx.context_variables.get("user_id")
    lang = ctx.context_variables.get("preferences", {}).get("language", "en")
    return f"Hello {user}!" if lang == "en" else f"Hola {user}!"

# Access in dynamic instructions
def get_instructions(context_variables):
    org = context_variables.get("org_id")
    return f"You work for organization {org}. Follow their policies."
```

### Streaming

```python
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner

async def stream_response():
    agent = Agent(name="Assistant", instructions="Be helpful")

    result = Runner.run_streamed(agent, input="Tell me a story")

    async for event in result.stream_events():
        # Raw token events
        if event.type == "raw_response_event":
            if isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)

        # Agent changed (handoff occurred)
        elif event.type == "agent_updated_stream_event":
            print(f"\n[Handed off to: {event.data.agent.name}]")

asyncio.run(stream_response())
```

## Patterns

### Triage → Specialist Pattern

```python
# Specialists
sales_agent = Agent(
    name="Sales",
    instructions="Handle purchases, pricing, product questions"
)

support_agent = Agent(
    name="Support",
    instructions="Handle technical issues, bugs, troubleshooting"
)

billing_agent = Agent(
    name="Billing",
    instructions="Handle payments, invoices, refunds"
)

# Triage routes based on intent
triage = Agent(
    name="Triage",
    instructions="""Classify customer intent and route:
    - Purchase/pricing/products → Sales
    - Technical issues/bugs → Support
    - Payments/invoices/refunds → Billing
    Ask clarifying questions if intent unclear.""",
    handoffs=[sales_agent, support_agent, billing_agent]
)
```

### Multi-Step Workflow

```python
# Step agents
search_agent = Agent(
    name="Search",
    instructions="Search for products matching criteria",
    tools=[search_products],
    handoffs=[recommend_agent]
)

recommend_agent = Agent(
    name="Recommend",
    instructions="Recommend best options from search results",
    handoffs=[purchase_agent]
)

purchase_agent = Agent(
    name="Purchase",
    instructions="Complete the purchase transaction",
    tools=[process_payment, send_confirmation]
)
```

### Token Optimization

```python
# Limit conversation turns
result = Runner.run_sync(
    agent,
    input="Help me",
    max_turns=10  # Prevent runaway conversations
)

# Prune history before long conversations
def prune_history(messages, keep_last=10):
    """Keep system message + last N messages."""
    system_msgs = [m for m in messages if m.get("role") == "system"]
    other_msgs = [m for m in messages if m.get("role") != "system"]
    return system_msgs + other_msgs[-keep_last:]

# Use with nested handoffs (beta)
from agents import RunConfig

config = RunConfig(nest_handoff_history=True)  # Summarizes prior context
```

## Error Handling

```python
from agents import Runner, AgentsException

try:
    result = Runner.run_sync(agent, input="Do something")
except AgentsException as e:
    if "rate_limit" in str(e).lower():
        # Handle rate limiting
        time.sleep(60)
        result = Runner.run_sync(agent, input="Do something")
    elif "context_length" in str(e).lower():
        # Handle token overflow - prune and retry
        pass
    else:
        raise
```

## Best Practices

| Practice | Rationale |
|----------|-----------|
| One agent = one job | Clearer instructions, better routing |
| Clear tool docstrings | Model uses them to decide when to call |
| Use context_variables | Persist state across handoffs |
| Limit max_turns | Prevent infinite loops |
| Stream for UX | Real-time feedback |
| Handle tool errors | Graceful degradation |

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Mega-agents with many tools | Confuses routing | Specialize agents |
| Hardcoded user data | Breaks multi-tenancy | Use context_variables |
| Unbounded conversations | Token overflow | Set max_turns |
| Silent tool failures | Bad UX | Return error messages |

## Reference

See `references/` for:
- `sdk-reference.md` - Full API reference
- `patterns.md` - Advanced patterns
- `migration.md` - Swarm to Agents SDK migration
