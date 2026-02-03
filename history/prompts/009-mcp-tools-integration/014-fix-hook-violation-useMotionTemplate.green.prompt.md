---
id: 014
title: fix-hook-violation-useMotionTemplate
stage: green
date: 2026-01-20
surface: agent
model: gemini-2.0-flash-exp
feature: 009-mcp-tools-integration
branch: 009-mcp-tools-integration
user: Mutahir
command: fix it
labels: ["bugfix", "react", "hooks", "framer-motion"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend/src/components/feature/TaskItem.tsx
tests: []
---

## Prompt

"Runtime Error: Rendered fewer hooks than expected... src/components/feature/TaskList.tsx"

## Response snapshot

The error was caused by calling `useMotionTemplate` (a hook) inside the JSX `style` prop within the `return` statement of `TaskItem`. When I commented it out for debugging, it changed the hook count, causing the error. Even when uncommented, using hooks inside return is a violation.
Fix: Moved `useMotionTemplate` to the top level of the component and assigned it to a `background` variable.

## Outcome

- ✅ Impact: Fixed Runtime Error "Rendered fewer hooks".
- 🧪 Tests: Visual verification required.
- 📁 Files: Modified `frontend/src/components/feature/TaskItem.tsx`.
- 🔁 Next prompts: Continue monitoring.
- 🧠 Reflection: Always call hooks at the top level. Never inline them in JSX props.

## Evaluation notes (flywheel)

- Failure modes observed: "Rendered fewer hooks" due to conditional/inline hook usage.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
