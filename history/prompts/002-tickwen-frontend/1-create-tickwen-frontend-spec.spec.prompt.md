---
id: 1
title: create-tickwen-frontend-spec
stage: spec
date: 2026-01-07
surface: agent
model: gemini
feature: 002-tickwen-frontend
branch: 002-tickwen-frontend
user: Mutahir
command: /sp.specify
labels: ["spec", "frontend", "tickwen"]
links:
  spec: specs/002-tickwen-frontend/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-tickwen-frontend/spec.md
  - specs/002-tickwen-frontend/checklists/requirements.md
tests: []
---

## Prompt

Generate spec.md for Frontend of the Full-Stack Todo Web Applicatio , named as Tickwen

Scope:
- Frontend responsibility only: user interface, API consumption, state management.
- Frontend **must not** include any backend, database, authentication logic, tech stack explanation, or development plan.
- Backend provides REST API endpoints with JWT security.
- Python CLI Todo app exists in the project and should be used **only as reference** for:
  - Task CRUD rules
  - Completion toggle behavior
  - Validation logic (title required, description optional, etc.)
- Frontend UI should be **fully customized and visually premium**, inspired by **Vercel.com and Neon.com**, not generic.

Deliverables in spec.md:
1. **Pages**
   - Landing Page
     - Hero section with app name, tagline, CTA (Get Started/Login)
     - Feature highlights or workflow explanation
     - Modern, clean layout with premium UI
   - Dashboard / Task List Page
     - Shows all tasks of authenticated user
     - Includes Edit, Delete, Toggle Complete buttons
     - Visual emphasis on clarity, spacing, colors inspired by Vercel/Neon
   - Task Detail Page
     - Shows single task with all details (title, description, completed status, timestamps)
     - Buttons for Edit, Delete, Toggle Complete
     - Layout visually clean, interactive
   - Create / Edit Task Page
     - Form with Title (required, max 100), Description (optional, max 500), Completed checkbox
     - Submit button disabled while loading
     - Validation feedback inline
   - Loading / Error Page
     - Generic component for async calls
     - Shows spinner during API requests
     - Displays clear error messages

2. **Components**
   - TaskItem Component
     - Receives task object
     - Displays task info with clear visual distinction for completed tasks
     - Buttons: Edit, Delete, Toggle Complete
   - TaskList Component
     - Receives array of tasks
     - Renders TaskItem components
     - Handles empty state: “No tasks yet”
   - TaskForm Component
     - Used on Create/Edit pages
     - Handles input fields and validation
     - Submits API request via API client
   - Navbar / Header Component
     - Shows user info and Logout button
     - Optional: navigation links

3. **API Client**
   - Base URL: /api/
   - Attaches JWT token from frontend storage (localStorage/cookie) in `Authorization: Bearer <token>` header
   - Handles HTTP errors:
     - 401 → redirect to login
     - 403/404 → display message
   - Returns JSON responses

4. **State Management**
   - React Context or Zustand
   - Stores: current user info, tasks array, loading state, error state
   - Updates tasks automatically after create/update/delete

5. **UI/UX Requirements**
   - Fully customized, premium design inspired by Vercel.com and Neon.com
   - Fully responsive (mobile & desktop)
   - Clear loading indicators
   - Inline error messages for forms
   - Buttons, inputs, and task items should have interactive hover/focus states
   - Smooth transitions and spacing for clean modern look
   - Landing page hero section with CTA, animated or interactive elements optional
   - Color palette, typography, and spacing consistent across all pages

6. **Validation Rules (based on Python CLI logic)**
   - Task title: required, max 100 characters
   - Task description: optional, max 500 characters
   - Completion status: boolean checkbox on edit form

7. **API Endpoints Reference**
   - GET /api/{user_id}/tasks → fetch all tasks
   - GET /api/{user_id}/tasks/{id} → fetch single task
   - POST /api/{user_id}/tasks → create task
   - PUT /api/{user_id}/tasks/{id} → update task
   - DELETE /api/{user_id}/tasks/{id} → delete task
   - PATCH /api/{user_id}/tasks/{id}/complete → toggle completion
   - Frontend **must attach JWT token** in all requests

8. **Rules / Constraints**
   - Frontend never interacts with database directly
   - Frontend never issues or verifies JWT
   - All displayed data must belong to authenticated user (backend-enforced)
   - Task CRUD must follow backend API contract exactly
   - Show meaningful messages for loading, success, and error states

9. **Output Requirements**
   - spec.md must include structured sections:
     1. Pages (behavior, inputs, outputs, interaction flow, UI inspiration)
     2. Components (props, events, expected behavior, UI guidelines)
     3. API Client (request format, response format, error handling)
     4. State Management (what is stored, how it updates)
     5. UI/UX Requirements (fully customized, interactive, premium)
     6. Validation Rules
     7. Rules / Constraints
   - Include sample API request/response examples wherever relevant
   - Include expected behavior for loading, success, and error states
   - Python CLI Todo app **only as reference for logic**, not implementation

## Response snapshot

Created spec.md for Tickwen Frontend. Validated against requirements checklist.

## Outcome

- ✅ Impact: Created new feature spec
- 🧪 Tests: N/A
- 📁 Files: Created spec.md and requirements.md
- 🔁 Next prompts: sp.plan
- 🧠 Reflection: User input was detailed, minimal clarification needed.

## Evaluation notes (flywheel)

- Failure modes observed: Shell script argument parsing failed, fell back to manual file creation.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Fix shell script to handle long JSON arguments.
