# Feature Specification: Chatbot User Interface (ChatKit)

**Feature Branch**: `007-chatkit-ui`
**Created**: 2026-01-18
**Status**: Draft
**Input**: Phase 3.2 Chatbot User Interface using OpenAI ChatKit (Strict)

## Clarifications

### Session 2026-01-18
- Q: How should the assistant response be rendered (streaming vs atomic)? → A: Streaming (SSE)
- Q: What should the UI display when no conversation_id is provided? → A: Show Empty State (welcome prompt/tips)
- Q: How should non-critical errors (e.g., transient network failure) be communicated? → A: Toast Notification
- Q: What should happen to the input field immediately after the user sends a message? → A: Clear Input
- Q: How is a new `conversation_id` established? → A: Assigned by Backend (returned in first response)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Floating Chat Initialization (Priority: P1)

Users see a floating circular action button at the bottom-right of the dashboard. Clicking this button toggles the ChatKit interface in a persistent floating window.

**Why this priority**: Fundamental entry point; integrated into the dashboard layout.

**Independent Test**: Verify that the floating bot icon is visible on all dashboard pages and expands into a chat window upon click.

**Acceptance Scenarios**:

1. **Given** the user is on the dashboard, **When** they look at the bottom-right, **Then** a circular bot icon is visible.
2. **Given** the chat window is closed, **When** the user clicks the icon, **Then** the ChatKit UI expands upward from the button.
3. **Given** the chat window is open, **When** the user clicks the 'X' or the floating button, **Then** the window collapses.

---

### User Story 2 - Sending and Receiving Messages (Priority: P1)

Users must be able to type natural language input and receive AI assistant responses within the standard ChatKit interaction pattern.

**Why this priority**: Core interaction loop of the chatbot.

**Independent Test**: Send a message and verify the input clears, user message appears, typing indicator shows, and assistant response renders.

**Acceptance Scenarios**:

1. **Given** the input field is focused, **When** the user types and presses Enter (or clicks Send), **Then** the message is added to the ChatKit message list and the input field is cleared immediately.
2. **Given** a message has been sent, **When** waiting for a response, **Then** the ChatKit typing/loading indicator is visible.
3. **Given** the backend returns a response, **When** received, **Then** the assistant's message is rendered distinctly from the user's message using ChatKit styles.

---

### User Story 3 - UX & Accessibility (Priority: P2)

The interface must be responsive, keyboard accessible, and screen-reader friendly, leveraging ChatKit's built-in accessibility features.

**Why this priority**: Ensures usability for all users and professional polish.

**Independent Test**: Navigate the entire UI using only a keyboard and verify screen reader announcements for incoming messages.

**Acceptance Scenarios**:

1. **Given** the user is on a mobile device, **When** the keyboard opens, **Then** the message list adjusts to keep the latest content visible.
2. **Given** a screen reader is active, **When** a new assistant message arrives, **Then** it is announced/readable without losing focus on the input.
3. **Given** the user presses Tab, **When** navigating, **Then** focus moves logically between the message list and input controls.

---

### Edge Cases

- **Network Failure**: What happens if the message fails to send?
    - *Behavior*: ChatKit UI must display a retry option or clear error indicator.
- **Empty/Malformed Response**: What happens if the backend returns nothing?
    - *Behavior*: UI should show a generic error message rather than crashing or showing blank bubbles.
- **Long History**: What happens with a very long conversation?
    - *Behavior*: ChatKit message list handles scrolling performance and initial scroll-to-bottom behavior.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST render the conversational interface using strictly OpenAI ChatKit components (Container, MessageList, Input).
- **FR-002**: The UI MUST derive all state (history, current context) from the backend; it MUST NOT persist conversation content locally between sessions.
- **FR-003**: The system MUST support markdown rendering for assistant responses if supported by ChatKit default components.
- **FR-004**: The UI MUST handle the "loading" state during backend processing and MUST render assistant responses progressively (streaming) as tokens arrive using ChatKit's supported patterns.
- **FR-005**: The system MUST display clear visual separation between "User" and "Assistant" messages.
- **FR-006**: The UI MUST handle errors (network, 500s) by displaying user-friendly error messages using toast notifications, avoiding raw system dumps.
- **FR-007**: The UI MUST initialize new conversations by sending messages without a conversation ID and subsequently adopting the ID returned by the backend.

### Key Entities

- **Message**: A unit of communication (Role: User/Assistant, Content, Timestamp).
- **Conversation**: An ordered collection of Messages associated with a unique ID.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **Deterministic Rendering**: The UI renders identically for the same sequence of message inputs/history 100% of the time.
- **SC-002**: **Zero Custom Abstractions**: 100% of chat UI components are derived from OpenAI ChatKit library; no custom-built message bubbles or input bars.
- **SC-003**: **Statelessness**: A hard refresh of the browser page restores the exact same visual state (via backend fetch) with no data loss.
- **SC-004**: **Accessibility**: The chat interface passes WCAG 2.1 AA standards for keyboard navigation and contrast (as supported by ChatKit).