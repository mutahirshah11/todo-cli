---
id: 1
title: backend-api-specs-for-todo-app
stage: spec
date_iso: 2026-01-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: backend-tickwen
branch: 003-backend-tickwen
user: DELL
command: /sp.specify
labels:
  - specification
  - api
  - backend
  - todo
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/003-backend-tickwen/spec.md
  - specs/003-backend-tickwen/checklists/requirements.md
tests_yaml:
  - spec validation checklist
prompt_text: "Create specs for the Backend API of the Todo Full-Stack Web Application.\n\nScope:\n- Backend responsibility only: expose REST API endpoints for task operations.\n- The **Python CLI Todo app logic already exists** in the project. Use it as the definitive reference for all task rules, validation, and behavior.\n- Backend must enforce **user ownership** for all tasks.\n- Inputs must be validated exactly as in the CLI app.\n- Backend returns consistent JSON responses for all API calls.\n- Backend must handle errors: 401 Unauthorized, 403 Forbidden, 404 Not Found, 400 Bad Request.\n- Do **not** include frontend, UI, authentication issuing, tech stack explanation, or planning steps.\n\nDeliverables in spec.md:\n1. **API Endpoints**\n   - GET /api/{user_id}/tasks → list all tasks for a user\n   - GET /api/{user_id}/tasks/{id} → get details of a single task\n   - POST /api/{user_id}/tasks → create a new task\n   - PUT /api/{user_id}/tasks/{id} → update an existing task\n   - DELETE /api/{user_id}/tasks/{id} → delete a task\n   - PATCH /api/{user_id}/tasks/{id}/complete → toggle completion\n\n2. **Endpoint Details**\n   For each endpoint:\n   - Input: path params, query params, body\n   - Output: JSON response (success, error)\n   - Error codes and conditions\n   - Validation rules (from CLI app)\n   - Follow CLI app logic exactly for all CRUD and completion behavior\n\n3. **Ownership Enforcement**\n   - Every request must include a valid user ID (from decoded JWT, handled later)\n   - Backend must ensure tasks returned/modified belong to the authenticated user\n   - Any violation returns 403 Forbidden\n\n4. **Data Validation**\n   - Task title: required, max 100 characters\n   - Task description: optional, max 500 characters\n   - Completion status: boolean for PATCH and PUT\n   - Invalid inputs return 400 Bad Request with details\n   - All validations must follow the Python CLI Todo logic exactly\n\n5. **Error Handling**\n   - 401 Unauthorized if user ID is missing/invalid (token verification later)\n   - 403 Forbidden if task does not belong to user\n   - 404 Not Found if task ID does not exist\n   - 400 Bad Request for invalid payloads\n   - All error responses must include JSON with `{ \"error\": \"<message>\" }`\n\n6. **Output Requirements**\n   - spec.md must have structured sections:\n     1. API Endpoints\n     2. Endpoint Details\n     3. Ownership Enforcement\n     4. Data Validation\n     5. Error Handling\n   - Include **sample JSON request and response** for each endpoint\n   - Python CLI logic is the source of truth for task behavior, validations, and rules\n   - Do not include frontend logic, JWT issuance, or deployment details"
response_text: "Created comprehensive API specification for the Backend Todo application with 6 REST endpoints, detailed input/output specifications, ownership enforcement, data validation rules, and error handling procedures. The spec includes sample requests/responses for each endpoint and follows the requirements from the Python CLI Todo app logic."
outcome: "Successfully created backend API specification in specs/003-backend-tickwen/spec.md with all required sections: API Endpoints, Endpoint Details, Ownership Enforcement, Data Validation, and Error Handling. Created validation checklist in specs/003-backend-tickwen/checklists/requirements.md."
evaluation: "Specification meets all requirements with clear API contracts, validation rules, and error handling procedures. Ready for planning phase (/sp.plan)."
---

# Prompt History Record

## Summary
Created comprehensive backend API specification for Todo application with complete endpoint definitions, validation rules, and error handling.

## Details
- **Stage**: spec
- **Feature**: Backend API for Todo Full-Stack Web Application
- **Files Created**: specs/003-backend-tickwen/spec.md, specs/003-backend-tickwen/checklists/requirements.md

## Validation
- All required sections completed
- Sample requests/responses provided for each endpoint
- Ownership enforcement and validation rules clearly defined
- Error handling procedures specified