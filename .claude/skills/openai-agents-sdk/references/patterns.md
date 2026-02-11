# Advanced Patterns

## Customer Support System

Complete multi-agent support system with triage, specialists, and escalation.

```python
from agents import Agent, Runner, function_tool, RunContextWrapper

# Tools
@function_tool
def lookup_order(ctx: RunContextWrapper, order_id: str) -> str:
    """Look up order details by order ID."""
    # Database lookup
    return f"Order {order_id}: Status=Shipped, Total=$99.99"

@function_tool
def process_refund(ctx: RunContextWrapper, order_id: str, reason: str) -> str:
    """Process a refund for an order."""
    user_id = ctx.context_variables.get("user_id")
    return f"Refund initiated for order {order_id}. User {user_id} will receive credit in 3-5 days."

@function_tool
def create_ticket(ctx: RunContextWrapper, issue: str, priority: str) -> str:
    """Create a support ticket for escalation."""
    return f"Ticket created: {issue} (Priority: {priority})"

# Specialists
refund_agent = Agent(
    name="Refund Specialist",
    instructions="""You handle refund requests. Process:
    1. Look up the order
    2. Verify refund eligibility (within 30 days, unused)
    3. Process refund if eligible
    4. Explain next steps to customer""",
    tools=[lookup_order, process_refund]
)

tech_support_agent = Agent(
    name="Tech Support",
    instructions="""You handle technical issues. Process:
    1. Gather issue details
    2. Try common solutions
    3. Escalate if unresolved""",
    tools=[create_ticket]
)

billing_agent = Agent(
    name="Billing",
    instructions="Handle payment issues, invoice questions, subscription changes.",
    tools=[lookup_order]
)

# Triage routes to specialists
triage_agent = Agent(
    name="Customer Support",
    instructions="""You are the first point of contact. Classify and route:
    - Refund/return requests → Refund Specialist
    - Technical problems/bugs → Tech Support
    - Payment/billing/invoices → Billing

    Ask 1-2 clarifying questions if intent is unclear before routing.""",
    handoffs=[refund_agent, tech_support_agent, billing_agent]
)

# Run
result = Runner.run_sync(
    triage_agent,
    input="I want to return my order #12345",
    context_variables={"user_id": "user_789", "org_id": "acme_corp"}
)
```

## Voice Agent (Vapi Integration)

Agent designed for voice conversations with short responses.

```python
from agents import Agent, function_tool

@function_tool
def check_availability(date: str) -> str:
    """Check appointment availability for a date."""
    return "Available: 9am, 11am, 2pm, 4pm"

@function_tool
def book_appointment(date: str, time: str, service: str) -> str:
    """Book an appointment."""
    return f"Booked {service} on {date} at {time}"

voice_agent = Agent(
    name="Appointment Scheduler",
    instructions="""You are a voice assistant for scheduling appointments.

VOICE GUIDELINES:
- Keep responses under 2 sentences
- Use natural, conversational language
- Confirm details by repeating them back
- Don't use markdown or special formatting

FLOW:
1. Greet and ask what service they need
2. Ask preferred date/time
3. Check availability and offer options
4. Confirm booking details
5. Say goodbye""",
    tools=[check_availability, book_appointment]
)
```

## E-commerce Purchase Flow

Multi-step workflow: browse → recommend → purchase.

```python
from agents import Agent, function_tool, RunContextWrapper

@function_tool
def search_products(query: str, category: str = None) -> str:
    """Search product catalog."""
    return """Found 3 products:
    1. Blue Widget ($29.99) - 4.5 stars
    2. Red Widget ($24.99) - 4.2 stars
    3. Green Widget ($34.99) - 4.8 stars"""

@function_tool
def get_product_details(product_id: str) -> str:
    """Get detailed product information."""
    return "Blue Widget: High quality, 1-year warranty, free shipping"

@function_tool
def add_to_cart(ctx: RunContextWrapper, product_id: str, quantity: int) -> str:
    """Add product to cart."""
    user_id = ctx.context_variables.get("user_id")
    return f"Added {quantity}x {product_id} to cart for {user_id}"

@function_tool
def checkout(ctx: RunContextWrapper) -> str:
    """Process checkout."""
    return "Order placed! Confirmation #ORD-12345"

# Agents for each step
browse_agent = Agent(
    name="Product Browser",
    instructions="Help customers find products. Search catalog, show options.",
    tools=[search_products, get_product_details],
    handoffs=[]  # Will add recommend_agent
)

recommend_agent = Agent(
    name="Product Advisor",
    instructions="""Recommend best products based on customer needs.
    Compare features, prices, reviews. Help them decide.""",
    tools=[get_product_details],
    handoffs=[]  # Will add purchase_agent
)

purchase_agent = Agent(
    name="Checkout Assistant",
    instructions="Help complete the purchase. Add to cart, process checkout.",
    tools=[add_to_cart, checkout]
)

# Wire up handoffs
browse_agent.handoffs = [recommend_agent]
recommend_agent.handoffs = [purchase_agent, browse_agent]  # Can go back
```

## Context Preservation Across Handoffs

Maintaining state through the conversation.

```python
from agents import Agent, Runner, function_tool, RunContextWrapper

@function_tool
def authenticate_user(ctx: RunContextWrapper, email: str) -> str:
    """Authenticate user and store in context."""
    # In real app, verify credentials
    user_data = {"user_id": "u_123", "name": "John", "tier": "premium"}

    # Update context for all subsequent agents
    ctx.context_variables.update(user_data)
    return f"Welcome back, {user_data['name']}!"

@function_tool
def get_account_info(ctx: RunContextWrapper) -> str:
    """Get account info using context."""
    name = ctx.context_variables.get("name", "Unknown")
    tier = ctx.context_variables.get("tier", "free")
    return f"Account: {name}, Tier: {tier}"

auth_agent = Agent(
    name="Auth Agent",
    instructions="Authenticate users before proceeding.",
    tools=[authenticate_user],
    handoffs=[]  # Will add account_agent
)

account_agent = Agent(
    name="Account Agent",
    instructions="""Help with account management.
    User is already authenticated - their info is in context.""",
    tools=[get_account_info]
)

auth_agent.handoffs = [account_agent]

# Context flows through handoffs
result = Runner.run_sync(
    auth_agent,
    input="Log me in with john@example.com, then show my account",
    context_variables={}  # Starts empty, populated by authenticate_user
)

print(result.context_variables)  # Contains user_id, name, tier
```

## Parallel Tool Execution

When tools are independent, they can run in parallel.

```python
from agents import Agent, function_tool
import asyncio

@function_tool
async def fetch_weather(city: str) -> str:
    """Fetch weather for a city."""
    await asyncio.sleep(1)  # Simulate API call
    return f"{city}: 72°F, Sunny"

@function_tool
async def fetch_news(topic: str) -> str:
    """Fetch news headlines."""
    await asyncio.sleep(1)  # Simulate API call
    return f"Top news about {topic}: [Headlines...]"

@function_tool
async def fetch_stocks(symbol: str) -> str:
    """Fetch stock price."""
    await asyncio.sleep(1)  # Simulate API call
    return f"{symbol}: $150.25 (+2.3%)"

# Agent can call multiple tools - SDK handles parallelization
dashboard_agent = Agent(
    name="Dashboard",
    instructions="""Provide daily briefing with weather, news, and stocks.
    Gather all information, then present a summary.""",
    tools=[fetch_weather, fetch_news, fetch_stocks]
)
```

## Conversation History Pruning

Manage token limits in long conversations.

```python
from agents import Agent, Runner

def prune_conversation(messages: list, max_messages: int = 20) -> list:
    """Keep recent messages while preserving system context."""
    system_messages = [m for m in messages if m.get("role") == "system"]
    other_messages = [m for m in messages if m.get("role") != "system"]

    # Keep last N non-system messages
    pruned = other_messages[-max_messages:] if len(other_messages) > max_messages else other_messages

    return system_messages + pruned

# Long-running conversation
messages = []
agent = Agent(name="Assistant", instructions="Be helpful")

for user_input in conversation_inputs:
    messages.append({"role": "user", "content": user_input})

    # Prune before each run to stay under token limits
    messages = prune_conversation(messages, max_messages=20)

    result = Runner.run_sync(agent, messages)
    messages.append({"role": "assistant", "content": result.final_output})
```

## Retry with Exponential Backoff

Handle rate limits and transient errors.

```python
import time
from agents import Agent, Runner, AgentsException

def run_with_retry(agent, input, max_retries=3, base_delay=1):
    """Run agent with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            return Runner.run_sync(agent, input)
        except AgentsException as e:
            if "rate_limit" in str(e).lower() and attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"Rate limited, retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise

    raise Exception("Max retries exceeded")
```

## Multi-Tenant Context

Isolate data between organizations.

```python
from agents import Agent, function_tool, RunContextWrapper

@function_tool
def get_org_data(ctx: RunContextWrapper, query: str) -> str:
    """Get organization-specific data."""
    org_id = ctx.context_variables.get("org_id")
    if not org_id:
        return "Error: No organization context"

    # Query only this org's data
    return f"Data for org {org_id}: [results for '{query}']"

@function_tool
def update_org_settings(ctx: RunContextWrapper, setting: str, value: str) -> str:
    """Update organization settings."""
    org_id = ctx.context_variables.get("org_id")
    user_role = ctx.context_variables.get("user_role")

    if user_role != "admin":
        return "Error: Admin access required"

    return f"Updated {setting}={value} for org {org_id}"

tenant_agent = Agent(
    name="Org Assistant",
    instructions="""Help users with their organization's data.
    Always operate within the user's org context.
    Respect role-based permissions.""",
    tools=[get_org_data, update_org_settings]
)

# Each request includes tenant context
result = Runner.run_sync(
    tenant_agent,
    input="Show me our sales data",
    context_variables={
        "org_id": "org_456",
        "user_id": "user_123",
        "user_role": "admin"
    }
)
```
