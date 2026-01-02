# Tasks: Todo CLI Application

**Feature**: Todo CLI Application
**Branch**: 001-todo-cli-specs
**Generated**: 2025-12-31
**Based on**: specs/001-todo-cli-specs/spec.md, specs/001-todo-cli-specs/plan.md

## Implementation Strategy

Implement the Todo CLI Application following a test-driven development approach. Start with the foundational components (Task model, TaskService with temporary file persistence) and then implement each user story in priority order. Each user story should be independently testable and deliver value. State will be maintained between CLI commands using a temporary file.

**MVP Scope**: User Story 1 (Add tasks) and User Story 2 (View tasks) with basic functionality.

## Dependencies

- User Story 1 (Add tasks) must be completed before User Story 3 (Mark Complete), User Story 4 (Update tasks), and User Story 5 (Delete tasks) as they depend on having tasks in the system
- Foundational components (Task model, TaskService) must be completed before CLI commands can be implemented

## Parallel Execution Examples

- Task model and initial tests can be developed in parallel
- CLI commands for different operations can be developed in parallel after foundational components are complete
- Unit tests can be written in parallel with implementation

## Phase 1: Setup

- [x] T001 Create project directory structure per implementation plan
- [x] T002 Initialize Python project with uv and create pyproject.toml
- [x] T003 Add dependencies (click, pytest) using uv
- [x] T004 Create source directory structure (src/todo_cli/, src/todo_cli/models/, src/todo_cli/services/, src/todo_cli/cli/)
- [x] T005 Create tests directory structure (tests/unit/, tests/integration/, tests/contract/)

## Phase 2: Foundational Components

- [ ] T006 [P] Create Task model in src/todo_cli/models/task.py with id, content, and completed fields
- [ ] T007 [P] Create TaskService in src/todo_cli/services/task_service.py with in-memory storage and temporary file persistence
- [ ] T008 [P] Implement TaskService.add_task() method with sequential ID generation and file persistence
- [ ] T009 [P] Implement TaskService.get_all_tasks() method with file loading
- [ ] T010 [P] Implement TaskService.get_task_by_id() method with file loading
- [ ] T011 [P] Implement TaskService.update_task() method with file persistence
- [ ] T012 [P] Implement TaskService.delete_task() method with file persistence
- [ ] T013 [P] Implement TaskService.mark_complete() method with file persistence
- [ ] T013A [P] Implement TaskService.save_to_file() method for state persistence
- [ ] T013B [P] Implement TaskService.load_from_file() method for state loading
- [ ] T013C [P] Implement TaskService._get_next_id() method for sequential ID generation
- [ ] T014 [P] Create main CLI entry point in src/todo_cli/main.py with click decorators
- [ ] T015 [P] Create __init__.py files in all directories

## Phase 3: User Story 1 - Add New Tasks (Priority: P1)

**Goal**: Implement the ability to add new tasks to the todo list using the command line

**Independent Test Criteria**: Can be fully tested by running the add command with various inputs and verifying the task appears in the list with appropriate confirmation message.

**Acceptance Scenarios**:
1. Given user wants to add a task, When user runs `todo add "Buy groceries"`, Then the task is added to the list and a success message is displayed
2. Given user wants to add a task with special characters, When user runs `todo add "Call John's store (555) 123-4567"`, Then the task is added with all characters preserved

- [ ] T016 [P] [US1] Create unit tests for Task model in tests/unit/test_task.py
- [ ] T017 [P] [US1] Create unit tests for TaskService.add_task() in tests/unit/test_task_service.py
- [ ] T018 [US1] Create CLI add command in src/todo_cli/cli/commands.py
- [ ] T019 [US1] Implement add command with proper error handling, exit codes, and temporary file persistence
- [ ] T020 [US1] Add support for both human-readable and JSON output formats to add command
- [ ] T021 [US1] Test add command with various inputs including special characters
- [ ] T022 [US1] Verify sequential ID assignment for new tasks

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Implement the ability to see all current tasks with their completion status and IDs

**Independent Test Criteria**: Can be fully tested by adding tasks and then viewing them to ensure they display correctly with appropriate formatting.

**Acceptance Scenarios**:
1. Given user has added multiple tasks, When user runs `todo list`, Then all tasks are displayed with their ID, status, and content
2. Given user has no tasks, When user runs `todo list`, Then an appropriate message is displayed indicating no tasks exist

- [ ] T023 [P] [US2] Create unit tests for TaskService.get_all_tasks() in tests/unit/test_task_service.py
- [ ] T024 [P] [US2] Create unit tests for TaskService.get_task_by_id() in tests/unit/test_task_service.py
- [ ] T025 [US2] Create CLI list command in src/todo_cli/cli/commands.py
- [ ] T026 [US2] Implement list command with proper formatting, temporary file persistence, and both output formats
- [ ] T027 [US2] Add support for --json flag to list command
- [ ] T028 [US2] Handle case when no tasks exist with appropriate message
- [ ] T029 [US2] Test list command with various scenarios (empty list, multiple tasks)

## Phase 5: User Story 3 - Mark Tasks Complete (Priority: P2)

**Goal**: Implement the ability to mark a specific task as complete

**Independent Test Criteria**: Can be fully tested by adding tasks, marking them as complete, and verifying the status changes when viewing the list.

**Acceptance Scenarios**:
1. Given user has tasks in their list, When user runs `todo complete 1`, Then the task with ID 1 is marked as complete and this is reflected when viewing the list

- [ ] T030 [P] [US3] Create unit tests for TaskService.mark_complete() in tests/unit/test_task_service.py
- [ ] T031 [US3] Create CLI complete command in src/todo_cli/cli/commands.py
- [ ] T032 [US3] Implement complete command with proper error handling for invalid IDs and temporary file persistence
- [ ] T033 [US3] Add support for both human-readable and JSON output formats to complete command
- [ ] T034 [US3] Test complete command with valid and invalid task IDs
- [ ] T035 [US3] Verify task status changes are reflected when viewing the list

## Phase 6: User Story 4 - Update Task Content (Priority: P3)

**Goal**: Implement the ability to modify the content of an existing task

**Independent Test Criteria**: Can be fully tested by adding a task, updating its content, and verifying the change persists.

**Acceptance Scenarios**:
1. Given user has a task in their list, When user runs `todo update 1 "Updated task content"`, Then the task content is changed and the update is reflected when viewing the list

- [ ] T036 [P] [US4] Create unit tests for TaskService.update_task() in tests/unit/test_task_service.py
- [ ] T037 [US4] Create CLI update command in src/todo_cli/cli/commands.py
- [ ] T038 [US4] Implement update command with proper error handling for invalid IDs and temporary file persistence
- [ ] T039 [US4] Add support for both human-readable and JSON output formats to update command
- [ ] T040 [US4] Test update command with valid and invalid task IDs
- [ ] T041 [US4] Verify task content changes are reflected when viewing the list

## Phase 7: User Story 5 - Delete Tasks (Priority: P3)

**Goal**: Implement the ability to remove a task from the list

**Independent Test Criteria**: Can be fully tested by adding tasks, deleting one, and verifying it no longer appears in the list.

**Acceptance Scenarios**:
1. Given user has tasks in their list, When user runs `todo delete 1`, Then the task with ID 1 is removed from the list

- [ ] T042 [P] [US5] Create unit tests for TaskService.delete_task() in tests/unit/test_task_service.py
- [ ] T043 [US5] Create CLI delete command in src/todo_cli/cli/commands.py
- [ ] T044 [US5] Implement delete command with proper error handling for invalid IDs and temporary file persistence
- [ ] T045 [US5] Add support for both human-readable and JSON output formats to delete command
- [ ] T046 [US5] Test delete command with valid and invalid task IDs
- [ ] T047 [US5] Verify task removal is reflected when viewing the list

## Phase 8: Integration & Error Handling

- [ ] T048 Create integration tests for CLI commands in tests/integration/test_cli_commands.py
- [ ] T049 Implement proper error handling with standardized error codes (1 for general error, 2 for invalid ID, 3 for missing argument)
- [ ] T050 Add exit code handling (0 for success, non-zero for errors) to all commands
- [ ] T051 Handle edge cases: non-existent task IDs, missing arguments, empty content
- [ ] T052 Test error scenarios for all commands
- [ ] T053 Create error handling utilities in src/todo_cli/utils/error_handlers.py for consistent error responses
- [ ] T054 Implement error code 1 (general error) handling across all commands
- [ ] T055 Implement error code 2 (invalid ID) handling across all commands
- [ ] T056 Implement error code 3 (missing argument) handling across all commands

## Phase 9: Polish & Cross-Cutting Concerns

- [ ] T057 Add comprehensive help text to all CLI commands
- [ ] T058 Create README.md with usage instructions
- [ ] T059 Run full test suite to ensure all functionality works together
- [ ] T060 Perform end-to-end testing of all user workflows
- [ ] T061 Optimize performance to meet sub-second response time goals
- [ ] T062 Document any remaining functionality in docstrings