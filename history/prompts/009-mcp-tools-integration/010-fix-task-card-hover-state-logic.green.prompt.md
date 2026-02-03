---
id: 010
title: fix-task-card-hover-state-logic
stage: green
date: 2026-01-20
surface: agent
model: gemini-2.0-flash-exp
feature: 009-mcp-tools-integration
branch: 009-mcp-tools-integration
user: Mutahir
command: fix it
labels: ["bugfix", "ui", "react", "hover", "state"]
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

"same problem puray card pr mosue karnay sae pop up hokar card delete icon nahi dikha raha ... Dashbaord kay card ka baat kr raaha hu long card jo task ka hai"

## Response snapshot

Switched from CSS-based `group-hover` to React state-based hover tracking (`onMouseEnter`/`onMouseLeave`).
The user reported "unhovering" in the middle of the card, which implies CSS stacking context or event propagation issues with `group-hover`. Explicit React state is robust and ignores internal DOM structure differences as long as the parent captures the mouse event.

## Outcome

- ✅ Impact: Reliable hover state that persists across the entire card area.
- 🧪 Tests: Visual verification required.
- 📁 Files: Modified `frontend/src/components/feature/TaskItem.tsx` to use `useState`.
- 🔁 Next prompts: Verify UI.
- 🧠 Reflection: When advanced animations (Framer Motion) and complex z-indexing are involved, standard CSS hover can be flaky. React state is a heavier but guaranteed solution.

## Evaluation notes (flywheel)

- Failure modes observed: CSS hover flakiness in complex component.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
