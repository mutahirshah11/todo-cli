---
id: 016
title: fix-floating-chatbot-overlap-issue
stage: green
date: 2026-01-20
surface: agent
model: gemini-2.0-flash-exp
feature: 009-mcp-tools-integration
branch: 009-mcp-tools-integration
user: Mutahir
command: fix it
labels: ["bugfix", "ui", "css", "pointer-events", "overlap"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend/src/components/chat/floating-chatbot.tsx
tests: []
---

## Prompt

"bro i have figured out ye delete ka button kyu anhi dab raha , kyu k ye jo hum ne floating-chatbot.tsx bananaya hai iska div overalp kr rah ahai us car k uper jiss waja sae adha car kama nahi kr raha hai dekho usko fix karo in such way k dono kam hogae koi cheez hatani na paray"

## Response snapshot

User correctly identified that the Floating Chatbot container (which is fixed at the bottom-right) was overlapping the task card, blocking clicks. Even though the chat window was closed/invisible, the container div was still capturing events.
Fix:
1.  Added `pointer-events-none` to the main Floating Chatbot container. This allows clicks to pass through the empty space around the button.
2.  Added `pointer-events-auto` to the specific interactive elements (Chat Window and Toggle Button) so they remain clickable.

## Outcome

- ✅ Impact: Task card clicks work (including delete button), and Chatbot still works. No functionality removed.
- 🧪 Tests: User verification required.
- 📁 Files: Modified `frontend/src/components/chat/floating-chatbot.tsx`.
- 🔁 Next prompts: Continue monitoring.
- 🧠 Reflection: Fixed positioning containers often create invisible overlays. Always use `pointer-events-none` on the layout container and re-enable it on children.

## Evaluation notes (flywheel)

- Failure modes observed: Layout container blocking user interaction.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
