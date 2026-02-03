# Implementation Plan: MCP Tools Integration

**Branch**: `009-mcp-tools-integration` | **Date**: 2026-01-20 | **Spec**: `specs/009-mcp-tools-integration/spec.md`
**Input**: Feature specification from `/specs/009-mcp-tools-integration/spec.md`

## Summary

Implement an MCP (Model Context Protocol) Server to expose task management operations (`add_task`, `list_tasks`, `update_task`, `complete_task`, `delete_task`) to AI agents. The server will be stateless, built with the official `mcp` Python SDK, and integrated with the existing FastAPI/SQLModel backend for data persistence and validation.

## Technical Context

**Language/Version**: Python 3.12 (matches existing backend)
**Primary Dependencies**: 
- `mcp` (Official SDK)
- `fastapi` (Existing)
- `sqlmodel` (Existing)
- `pydantic` (Existing)
**Storage**: Neon PostgreSQL (Existing, via SQLModel)
**Testing**: `pytest` (Existing)
**Target Platform**: Backend Service (Containerized)
**Project Type**: Web Application Backend
**Performance Goals**: <50ms tool execution latency (excluding DB)
**Constraints**: 
- Stateless MCP Server
- No UI changes
- Must use official MCP SDK
- Must reuse existing Service/Repository layer

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Strict TDD**: Checked. All tools will be TDD'd.
- **User-Centric Privacy**: Checked. Tools require `user_id` and must enforce ownership.
- **Future-Proof Extensibility**: Checked. MCP is an open standard for agent integration.
- **Data Integrity**: Checked. Reusing existing repositories ensures consistent validation and ACID properties.
- **Simplicity**: Checked. Using official SDK and stateless design.

## Project Structure

### Documentation (this feature)

```text
specs/009-mcp-tools-integration/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (Entity mapping)
├── quickstart.md        # Phase 1 output (How to run MCP server)
├── contracts/           # Phase 1 output (Tool JSON Schemas)
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
backend/
├── mcp_server.py           # New: MCP Server entry point
├── api/
│   ├── mcp/                # New: MCP specific logic
│   │   ├── __init__.py
│   │   ├── tools.py        # Tool definitions and registration
│   │   └── utils.py        # Helper functions (e.g., error formatting)
│   ├── services/           # Existing: Business logic reuse
│   └── repositories/       # Existing: DB access reuse
└── tests/
    └── mcp/                # New: Tests for MCP tools
        ├── unit/
        └── integration/
```

**Structure Decision**: Added `backend/mcp_server.py` as the entry point and `backend/api/mcp/` for modular tool definitions. This keeps the MCP logic distinct but allows easy import of existing services.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None      | N/A        | N/A                                 |