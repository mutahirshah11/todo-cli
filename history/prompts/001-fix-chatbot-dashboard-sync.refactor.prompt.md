---
id: "001"
title: "Fix Chatbot Dashboard Sync"
stage: "refactor"
date: "2026-01-23"
surface: "agent"
model: "gemini-2.0-flash-thinking-exp-1219"
feature: "chatbot-task-sync"
branch: "main"
user: "Mutahir"
command: "fix-sync"
labels:
 - "bugfix"
 - "auth"
 - "chatbot"
 - "mcp"
links:
 spec: null
 ticket: null
 adr: null
 pr: null
files_yaml: |
 - frontend/src/components/chat/chat-container.tsx
 - frontend/src/app/api/chat/message/route.ts
 - backend/api/routers/agent.py
tests_yaml: |
 - manual verification
prompt_text: |
 is ne mujhay jo task dikhae ha (ye mene add akrwae thay phele) wo dashbarod pr hai hi nahi ! yani pata nahi kaha sotre hai ye task or dashboard k task . 
 ...
 ky asamjhay ho batao k sahi samjhay ho ya galat
response_text: |
 The chatbot and dashboard were using different user IDs. The dashboard uses the ID from the JWT token, while the chatbot was falling back to a "guest" ID or an untrusted ID from the request body. I implemented a fix to enforce JWT authentication for the chatbot and pass the authenticated user ID to the agent tools.
---
The Chatbot and Dashboard are now synchronized.
1.  **Frontend:** Chat widget now sends the Authorization token.
2.  **Proxy:** Next.js API route forwards the token to the backend.
3.  **Backend:** Chat endpoint now verifies the token and uses the *authenticated* User ID.

Now, tasks added via Chatbot will appear on the Dashboard, and vice versa.
