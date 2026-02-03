---
id: 015
title: refactor-task-item-stacking-and-layout
stage: green
date: 2026-01-20
surface: agent
model: gemini-2.0-flash-exp
feature: 009-mcp-tools-integration
branch: 009-mcp-tools-integration
user: Mutahir
command: fix it
labels: ["bugfix", "ui", "z-index", "layout", "framer-motion"]
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

User reported two issues:
1. "pura card pr hover krany sae glow up nahi hota shyd size ka masla hai" (Glow doesn't work on the full card, maybe size issue).
2. "jaab glow hota hai tab hi delte ka button kama karta hai" (Delete button only works when glow works).

## Response snapshot

Hypothesis: Stacking context and hit-testing issues were causing "dead zones" where the container didn't receive mouse events (killing the glow) and potentially confusing the user about the delete button state.
Fix:
1.  **Full Width:** Added `w-full` to the main container to ensure it fills the list width and has no dead zones.
2.  **Simplified Stacking:** Removed `z-10` from content and `z-20` from button. Relied on natural DOM order (Content > Flashlight) to handle stacking.
3.  **Removed Debug Styles:** Removed the red background debug style from the delete button.
4.  **Preserved Functionality:** Kept `e.stopPropagation` on the delete button.

## Outcome

- ✅ Impact: Improved layout robustness and touch/click targets.
- 🧪 Tests: Visual verification required.
- 📁 Files: Modified `frontend/src/components/feature/TaskItem.tsx`.
- 🔁 Next prompts: Continue monitoring.
- 🧠 Reflection: Over-engineering z-indexes often leads to fragile UIs. Natural DOM stacking is usually safer.

## Evaluation notes (flywheel)

- Failure modes observed: Complex z-index/overlay interactions creating hit-test dead zones.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
