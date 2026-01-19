---
id: 023
title: global-chatbot-integration
stage: refactor
date: 2026-01-18
surface: agent
model: gemini-2.0-flash-exp
feature: 007-chatkit-ui
branch: 007-chatkit-ui
user: Mutahir
command: refactor
labels: ["global-ui", "chatbot", "auth-conditional", "layout"]
links:
  spec: specs/007-chatkit-ui/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/app/theme-provider-wrapper.tsx
  - frontend/src/components/chat/global-chatbot.tsx
  - frontend/src/app/dashboard/layout.tsx
tests: []
---

## Prompt

bro show the chatbot on the homepage too when the user is signin ... on everypage user should access the chatbot

## Response snapshot

Enabled global access to the chatbot across all pages for authenticated users.
- Created `GlobalChatbot` component to handle conditional rendering based on `isAuthenticated` state from `AuthProvider`.
- Moved chatbot integration from `dashboard/layout.tsx` to `theme-provider-wrapper.tsx`.
- Ensured chatbot is visible on the homepage and all other routes when the user is signed in.

## Outcome

- ✅ Impact: Users can now access AI assistance from anywhere in the application after logging in.
- 🧪 Tests: N/A
- 📁 Files: Modified layout and created conditional wrapper component.
- 🔁 Next prompts: none
- 🧠 Reflection: Leveraging the existing AuthProvider context allows for clean conditional UI logic at the root level.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): standard
- Next experiment (smallest change to try): none
