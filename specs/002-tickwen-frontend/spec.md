# Feature Specification: Tickwen Frontend

**Feature Branch**: `002-tickwen-frontend`
**Created**: 2026-01-07
**Status**: Draft
**Input**: User description: "Generate spec.md for Frontend of the Full-Stack Todo Web Applicatio , named as Tickwen..."

## Clarifications

### Session 2026-01-07
- Q: How should authentication interfaces be presented? → A: Dedicated Pages (/login, /register).
- Q: How should task deletions be confirmed? → A: Custom Modal.
- Q: How should success feedback for actions (CRUD) be displayed? → A: Toast Notifications.
- Q: Should theme preference be persisted? → A: Yes, via localStorage.
- Q: How should task searching/filtering be implemented? → A: Client-side filtering.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Dashboard & Task Management (Priority: P1)

As an authenticated user, I want to view, complete, and delete my tasks so that I can stay organized.

**Why this priority**: Core value proposition of a Todo app.

**Independent Test**: Can be tested by mocking the API and verifying the UI updates for CRUD operations.

**Acceptance Scenarios**:

1. **Given** an authenticated user with existing tasks, **When** they visit the dashboard, **Then** they see a list of their tasks with clear status indicators.
2. **Given** a task in the list, **When** the user clicks the "Complete" toggle, **Then** the task visual style updates to "completed", a toast notification confirms the change, and a request is sent to the backend.
3. **Given** a task, **When** the user clicks "Delete", **Then** a custom confirmation modal is displayed.
4. **Given** the delete confirmation modal, **When** the user confirms, **Then** the task is removed from the list and a success toast is shown.
5. **Given** an empty task list, **When** the user visits the dashboard, **Then** they see a friendly "No tasks yet" message.

---

### User Story 2 - Task Creation & Editing (Priority: P1)

As a user, I want to create new tasks and edit existing ones to keep my list accurate.

**Why this priority**: Essential for data entry and maintenance.

**Independent Test**: Can be tested by simulating form submissions and API responses.

**Acceptance Scenarios**:

1. **Given** the "Create Task" form, **When** the user enters a Title and submits, **Then** the task is added to the list, a success toast is shown, and the form resets.
2. **Given** the form, **When** the user tries to submit without a Title, **Then** an inline validation error is displayed.
3. **Given** an existing task, **When** the user clicks "Edit", **Then** the form opens pre-filled with task details.
4. **Given** the edit form, **When** the user saves changes, **Then** the task list reflects the updated information and a success toast confirms the update.

---

### User Story 3 - Landing Page & Authentication Flow (Priority: P2)

As a visitor, I want to understand what the app does and log in so I can access my data.

**Why this priority**: Entry point for the application.

**Independent Test**: Verify landing page elements and redirection logic upon auth events.

**Acceptance Scenarios**:

1. **Given** a visitor, **When** they access the root URL, **Then** they see the Hero section with app name "Tickwen" and a "Get Started/Login" CTA.
2. **Given** an unauthenticated user, **When** they try to access `/dashboard`, **Then** they are redirected to the `/login` page.
3. **Given** an authenticated user, **When** the API returns a 401 (Unauthorized) error, **Then** the user is redirected to the login flow.
4. **Given** an authenticated user, **When** they click "Logout", **Then** their session is cleared and they are sent to the landing page.

---

### User Story 4 - Error Handling & Feedback (Priority: P3)

As a user, I want to see clear feedback when things load or fail so I know the system status.

**Why this priority**: Good UX prevents frustration during network issues.

**Independent Test**: Simulate network latency and error responses.

**Acceptance Scenarios**:

1. **Given** any async operation (load/save), **When** the request is in progress, **Then** a loading spinner is visible and buttons are disabled.
2. **Given** an API failure (e.g., 500 or network error), **When** a request fails, **Then** a user-friendly error message is displayed (toast or inline).

---

### User Story 5 - Theme Management (Priority: P3)

As a user, I want my theme preference (Dark/Light) to be remembered so the app matches my preference every time I visit.

**Why this priority**: Standard feature for premium SaaS applications.

**Independent Test**: Set theme, refresh page, and verify theme persists.

**Acceptance Scenarios**:

1. **Given** the application, **When** a user changes the theme, **Then** the preference is saved to local storage.
2. **Given** a returning user with a saved preference, **When** they load the application, **Then** the saved theme is applied immediately.

---

### User Story 6 - Task Filtering (Priority: P2)

As a user with many tasks, I want to quickly filter my list so I can find specific items instantly.

**Why this priority**: Improves usability as the task list grows.

**Independent Test**: Type in a search box and verify the list filters in real-time.

**Acceptance Scenarios**:

1. **Given** a list of tasks, **When** the user types in the search box, **Then** the list instantly updates to show only matching tasks based on title or description.
2. **Given** a search query with no matches, **When** the user finishes typing, **Then** an "Empty search results" message is displayed.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The Landing Page MUST display a Hero section, tagline, feature highlights, and a CTA button using premium styling.
- **FR-001a**: The Application MUST provide dedicated `/login` and `/register` pages for user authentication.
- **FR-002**: The Dashboard MUST display all tasks fetched from `GET /api/{user_id}/tasks`.
- **FR-003**: The Task List MUST render `TaskItem` components with Edit, Delete, and Toggle Complete actions.
- **FR-003a**: The Application MUST display a custom confirmation modal before deleting a task.
- **FR-003b**: The Application MUST provide success feedback via toast notifications for all CRUD operations.
- **FR-004**: The `TaskForm` MUST validate that 'Title' is present (max 100 chars) and 'Description' is optional (max 500 chars).
- **FR-005**: The Frontend MUST send `POST /api/{user_id}/tasks` to create tasks and `PUT /api/{user_id}/tasks/{id}` to update them.
- **FR-006**: The Frontend MUST send `DELETE /api/{user_id}/tasks/{id}` to remove tasks.
- **FR-007**: The Frontend MUST send `PATCH /api/{user_id}/tasks/{id}/complete` to toggle completion status.
- **FR-008**: All API requests MUST include the JWT token in the `Authorization: Bearer <token>` header.
- **FR-009**: The UI MUST be fully responsive for mobile and desktop screens.
- **FR-010**: The Application MUST automatically update the displayed data after successful CRUD operations without requiring a manual page reload.
- **FR-011**: The Application MUST persist the user's theme preference in browser local storage.
- **FR-012**: The Dashboard MUST provide a search input that filters tasks client-side in real-time.

### Key Entities

- **Task**: { id, title, description, is_completed, created_at }
- **User**: { id, username } (Stored in client state/token)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a new task in under 30 seconds (measured by time on form).
- **SC-002**: Dashboard initial load time is under 1.5 seconds on 4G networks.
- **SC-003**: 100% of API errors result in a visible user-facing error message.
- **SC-004**: UI renders correctly and functionally on devices with screen widths of 375px (mobile) and 1440px (desktop).
- **SC-005**: Task filtering updates the UI in under 100ms for a list of up to 500 tasks.

## Design & Architecture (Frontend Only)

### Pages & Routing
- `/` - Landing Page
- `/login` - User Login
- `/register` - User Registration
- `/dashboard` - Task List (Protected)
- `/task/{id}` - Task Detail (Protected)
- `/create` - Create Task (Protected)
- `/edit/{id}` - Edit Task (Protected)

### UI/UX Guidelines
- **Style**: Premium, minimalist, high-contrast. Inspired by Vercel/Neon.
- **Components**:
  - `TaskItem`: Clean rows, subtle hover effects.
  - `TaskList`: Handles empty states visually.
  - `TaskForm`: Inline validation, disabled submit on loading.
  - `Navbar`: Consistent across protected pages, shows user info.
- **Feedback**:
  - Loading: Spinners for async actions.
  - Success: Toast notifications.
  - Errors: Clear text messages or toast notifications.

### API Client Strategy
- **Base URL**: `/api/`
- **Interceptors**: Attach JWT automatically; global error handler for 401 redirects.
