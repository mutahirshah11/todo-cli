---
id: 2
title: update-project-constitution
stage: constitution
date: 2026-01-06
surface: agent
model: gemini-2.0-flash-exp
feature: none
branch: main
user: Mutahir
command: /sp.constitution
labels: ["governance", "tdd", "refactor"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
tests:
  - null
---

## Prompt

/sp.constitution 

ask: Draft a formal Constitution for a full-stack software project.

Project context (for understanding, do not include in output):
This Constitution is for a multi-user Todo web application with authentication and planned Chatbot integration in the future (Phase III). The project will follow Test-Driven Development (TDD) principles to ensure reliability, correctness, and maintainable growth.

The Constitution should include:

Preamble: Purpose and guiding principles of the project.

Objectives: Goals regarding user experience, task management, security, and integrity.

Core Principles: Ethical rules, user-centric behavior, privacy, security, fairness, and adherence to TDD.

Governance: Rules for enforcing ownership, compliance, operational behavior, handling changes, and preparing for future integrations.

Data and User Interaction: Guidelines to ensure each user’s data is private, correct, and secure.

Compliance and Enforcement: How the Constitution is enforced and what constitutes violations.

Strict rules for you:

Do not mention technology, frameworks, libraries, databases, APIs, specs, plans, or tasks.

Do not include implementation details.

Output must be formal, precise, and authoritative.

Organize using articles, clauses, and principles like a legal or governance document.

Ensure the Constitution reflects multi-user fairness, security, future extensibility, TDD adherence, and data integrity.


Strict Test Driven Developemnt Should be done in the project

## Response snapshot

Updated constitution to v2.0.0 reflecting full-stack/TDD shift. Updated dependent templates (.specify/templates/spec-template.md and .specify/templates/tasks-template.md) to enforce mandatory testing.

## Outcome

- ✅ Impact: Constitution aligned with new project scope.
- 🧪 Tests: N/A
- 📁 Files: Updated constitution and 2 templates.
- 🔁 Next prompts: /sp.specify
- 🧠 Reflection: Manual template updates were required due to "OPTIONAL" keyword changes in the original templates which conflicted with the new "Strict TDD" principle.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
