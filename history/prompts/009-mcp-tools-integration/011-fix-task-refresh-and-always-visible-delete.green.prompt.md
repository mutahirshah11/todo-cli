---
id: 011
title: fix-task-refresh-and-always-visible-delete
stage: green
date: 2026-01-20
surface: agent
model: gemini-2.0-flash-exp
feature: 009-mcp-tools-integration
branch: 009-mcp-tools-integration
user: Mutahir
command: fix it
labels: ["bugfix", "ui", "react", "useEffect", "fetch-logic"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend/src/app/dashboard/page.tsx
 - frontend/src/components/feature/TaskItem.tsx
tests: []
---

## Prompt

1. Tasks disappear on refresh (only show when creating new ones).
2. "Secondly car pr hover kiye bagair bhi delete ka icon show ho... do these"

## Response snapshot

1. **Fixed Refresh Bug:** Updated `DashboardPage`'s `useEffect` to depend on `[user]`. Previously it only ran on mount (`[]`). On refresh, `user` is initially null, so the fetch failed. Now, when `AuthProvider` restores the user, the effect re-runs and fetches tasks.
2. **Fixed Delete Icon:** Made the delete icon **always visible** (`opacity-100`), removing the hover dependency entirely. This fulfills the user's request for "hover kiye bagair bhi show ho".

## Outcome

- ✅ Impact: Tasks persist after refresh; Delete icon is easier to access.
- 🧪 Tests: Visual verification required.
- 📁 Files: Modified `frontend/src/app/dashboard/page.tsx`, `frontend/src/components/feature/TaskItem.tsx`.
- 🔁 Next prompts: Continue monitoring.
- 🧠 Reflection: Race conditions between Auth rehydration and Data fetching are common in SPA. Always ensure data fetching waits for a valid User/Auth state.

## Evaluation notes (flywheel)

- Failure modes observed: `useEffect` with empty dependency array missing updates from async Auth provider.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
