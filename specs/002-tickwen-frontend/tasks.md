# Tasks: Tickwen Frontend

**Input**: Design documents from `/specs/002-tickwen-frontend/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are MANDATORY per Constitution Article I. Using Jest + RTL.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/src/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create dedicated frontend directory `frontend/` and initialize Next.js project
- [X] T002 Install dependencies (Tailwind, Zustand, Lucide, React Hook Form, Zod, Sonner, clsx) in `frontend/package.json`
- [X] T003 [P] Configure Tailwind CSS and `frontend/tailwind.config.ts` for "Premium" styling
- [X] T004 [P] Configure Jest and React Testing Library in `frontend/jest.config.ts` and `frontend/package.json`
- [X] T005 [P] Setup `frontend/src/lib/utils.ts` (cn helper) and `frontend/src/lib/api.ts` (fetch wrapper)
- [X] T006 [P] Setup global styles and font (Inter) in `frontend/src/app/globals.css` and `frontend/src/app/layout.tsx`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Define TypeScript interfaces from data-model.md in `frontend/src/lib/types.ts`
- [X] T008 Setup Zustand store for Auth and Tasks in `frontend/src/lib/store.ts`
- [X] T009 Implement Theme Provider (next-themes) in `frontend/src/app/providers.tsx`
- [X] T010 Create shared UI components (Button, Input, Card, Modal, Spinner) in `frontend/src/components/ui/`
- [X] T011 Setup Toaster component (Sonner) in `frontend/src/app/layout.tsx`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Dashboard & Task Management (Priority: P1) 🎯 MVP

**Goal**: Authenticated user can view, complete, and delete tasks.

**Independent Test**: Mock API, render Dashboard, verify list renders, complete toggle updates state, delete removes item.

### Tests for User Story 1 (MANDATORY) ⚠️

- [X] T012 [P] [US1] Create test for TaskList rendering in `frontend/src/__tests__/dashboard/TaskList.test.tsx`
- [X] T013 [P] [US1] Create test for TaskItem actions (toggle, delete) in `frontend/src/__tests__/dashboard/TaskItem.test.tsx`

### Implementation for User Story 1

- [X] T014 [US1] Create `TaskItem` component with actions in `frontend/src/components/feature/TaskItem.tsx`
- [X] T015 [US1] Create `TaskList` component (handles empty state) in `frontend/src/components/feature/TaskList.tsx`
- [X] T016 [US1] Implement `DeleteConfirmationModal` in `frontend/src/components/feature/DeleteConfirmationModal.tsx`
- [X] T017 [US1] Implement Dashboard page fetching logic in `frontend/src/app/dashboard/page.tsx`
- [X] T018 [US1] Integrate store actions (fetch, toggle, delete) in `frontend/src/lib/store.ts` (update stub)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Creation & Editing (Priority: P1)

**Goal**: User can create and edit tasks.

**Independent Test**: Render forms, submit valid/invalid data, verify store updates.

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T019 [P] [US2] Create test for TaskForm validation in `frontend/src/__tests__/forms/TaskForm.test.tsx`

### Implementation for User Story 2

- [X] T020 [US2] Create Zod schema for tasks in `frontend/src/lib/schemas.ts`
- [X] T021 [US2] Implement `TaskForm` component with RHF+Zod in `frontend/src/components/feature/TaskForm.tsx`
- [X] T022 [US2] Create Create Task page in `frontend/src/app/create/page.tsx`
- [X] T023 [US2] Create Edit Task page (with ID fetching) in `frontend/src/app/edit/[id]/page.tsx`
- [X] T024 [US2] Integrate store actions (create, update) in `frontend/src/lib/store.ts`

**Checkpoint**: Create/Edit flows functional.

---

## Phase 5: User Story 3 - Landing Page & Authentication Flow (Priority: P2)

**Goal**: Visitor can see landing page and log in/register.

**Independent Test**: Verify protected routes redirect, login form submits correctly.

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T025 [P] [US3] Create test for Auth Flow (Login/Register) in `frontend/src/__tests__/auth/Auth.test.tsx`

### Implementation for User Story 3

- [X] T026 [US3] Implement Landing Page Hero section in `frontend/src/app/page.tsx`
- [X] T027 [US3] Implement Login Page in `frontend/src/app/(auth)/login/page.tsx`
- [X] T028 [US3] Implement Register Page in `frontend/src/app/(auth)/register/page.tsx`
- [X] T029 [US3] Implement Auth Guard/Middleware for protected routes in `frontend/src/middleware.ts`
- [X] T030 [US3] Integrate store actions (login, logout) in `frontend/src/lib/store.ts`

**Checkpoint**: Auth flow complete.

---

## Phase 6: User Story 4 - Error Handling & Feedback (Priority: P3)

**Goal**: Clear feedback for loading/errors.

**Independent Test**: Mock API errors, verify toast appearance.

### Tests for User Story 4 (MANDATORY) ⚠️

- [X] T031 [P] [US4] Create test for Error Toast trigger in `frontend/src/__tests__/ui/Feedback.test.tsx`

### Implementation for User Story 4

- [X] T032 [US4] Update `frontend/src/lib/api.ts` interceptors to trigger global error toasts
- [X] T033 [US4] Ensure loading spinners in buttons/pages in `frontend/src/components/ui/`

---

## Phase 7: User Story 5 - Theme Management (Priority: P3)

**Goal**: Persist Dark/Light mode.

**Independent Test**: Toggle theme, reload, verify persistence.

### Implementation for User Story 5

- [X] T034 [US5] Implement Theme Toggle component in `frontend/src/components/ui/ThemeToggle.tsx`
- [X] T035 [US5] Add Theme Toggle to Navbar in `frontend/src/components/feature/Navbar.tsx`

---

## Phase 8: User Story 6 - Task Filtering (Priority: P2)

**Goal**: Client-side filtering.

**Independent Test**: Filter list, verify results.

### Tests for User Story 6 (MANDATORY) ⚠️

- [X] T036 [P] [US6] Create test for Filter logic in `frontend/src/__tests__/dashboard/Filter.test.tsx`

### Implementation for User Story 6

- [X] T037 [US6] Add Search Input to Dashboard in `frontend/src/app/dashboard/page.tsx`
- [X] T038 [US6] Update `frontend/src/lib/store.ts` with filtering logic (selectors)

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T039 [P] Update README.md with run instructions
- [X] T040 Run full linting and fix issues
- [X] T041 Verify responsiveness on mobile/desktop views

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup
- **User Stories (Phase 3+)**: All depend on Foundational
- **Polish (Phase 9)**: Depends on all stories

### Implementation Strategy

1. **Setup & Foundation**: T001-T011
2. **MVP (US1)**: T012-T018 (View/Delete Tasks)
3. **Core Features**: US2 (Create/Edit) -> US3 (Auth)
4. **Enhancements**: US6 (Filter) -> US4 (Feedback) -> US5 (Theme)
