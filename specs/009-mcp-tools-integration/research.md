# Research: MCP Tools Integration

**Branch**: `009-mcp-tools-integration`
**Date**: 2026-01-20

## Unknowns Resolved

### 1. MCP Server Implementation & Transport
**Question**: How should the MCP server be exposed to be callable by OpenAI Agents SDK?
**Findings**: 
- The OpenAI Agents SDK typically interacts with MCP servers via a client that connects to a running process (Stdio) or a network address (SSE). 
- **Decision**: Use **Stdio** transport for the primary implementation. This allows the server to be run as a subprocess (standard MCP pattern) and is easiest to secure (no open ports). If network access is required later, the SDK supports switching to SSE easily.
- **Reference**: Official MCP Python SDK documentation recommends Stdio for local/subprocess integration.

### 2. Database Integration in MCP Tools
**Question**: How to access the database within stateless tool calls?
**Findings**:
- The project uses `sqlmodel` with `AsyncSession`.
- `mcp` SDK tools are async functions.
- **Decision**: Use `async with AsyncSessionLocal() as session:` within each tool function. This ensures a fresh session for every tool call, maintaining statelessness and reusing the existing connection pool.
- **Dependency**: `backend.api.database.session.AsyncSessionLocal`.

### 3. Dependency Injection
**Question**: Can we reuse existing Services/Repositories?
**Findings**:
- Existing services likely depend on `Depends(get_db_session)`.
- **Decision**: Since MCP tools don't use FastAPI's `Depends`, we will instantiate the Repository/Service directly, passing the session created in the `with` block.
- **Pattern**: 
  ```python
  async with AsyncSessionLocal() as session:
      repo = TaskRepository(session)
      service = TaskService(repo)
      return await service.create_task(...)
  ```

## Best Practices Adopted

- **Statelessness**: No global state variables; DB is the single source of truth.
- **Error Handling**: Catch `pydantic.ValidationError` and `SQLAlchemyError`, returning them as structured string responses (or specific MCP error types) to the agent.
- **Security**: Strictly validate `user_id` in every tool call.

## Alternatives Considered

- **FastAPI Mount**: Running MCP as an endpoint inside FastAPI. 
  - *Rejected*: Keeps the MCP logic coupled to the HTTP server. Running as a standalone script (`backend/mcp_server.py`) allows it to be orchestrated separately (e.g., by a CLI or agent runner).
- **Global Session**: 
  - *Rejected*: Violates statelessness and risks connection issues.
