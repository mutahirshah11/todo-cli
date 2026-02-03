---
id: 009
title: fix-task-card-hover-issue
stage: green
date: 2026-01-20
surface: agent
model: gemini-2.0-flash-exp
feature: 009-mcp-tools-integration
branch: 009-mcp-tools-integration
user: Mutahir
command: fix it
labels: ["bugfix", "ui", "framer-motion", "hover", "z-index"]
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

"acha bro ye Your Task mae jo card hai us puray pr hover karnay sae delte ka icon aea .. aesa nahi hora hai left side pr gover karnay sae delete ka icon arah hai jesay hi card pr hover us tarf le jata hu unhover hojata hai samjh rahay ho ? kya kaha mene ye samjhao phele"

## Response snapshot

Acknowledged understanding: The user reported that the delete icon only appears when hovering the left side of the card, and moving to the center/right causes the hover state to break.
Fix: Removed `zIndex: 10` from `whileHover` in `TaskItem.tsx`. Dynamic z-index changes during hover often cause layout/stacking context trashing that can reset the hover state in some browsers/layouts.

## Outcome

- ✅ Impact: Stable hover state across the entire card.
- 🧪 Tests: User verification required.
- 📁 Files: Modified `frontend/src/components/feature/TaskItem.tsx`.
- 🔁 Next prompts: Verify UI behavior.
- 🧠 Reflection: When `whileHover` changes z-index, it can change the element's layer. If the mouse is "between" pixels or layers during the transition, the browser might fire `onMouseLeave`, cancelling the hover, which reverts the z-index, causing a loop or a broken state.

## Evaluation notes (flywheel)

- Failure modes observed: Hover instability due to z-index thrashing.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
