# Implementation Plan: Backend API for Todo Full-Stack Web Application

## Technical Context

- **Tech Stack**: Python + FastAPI
- **Reference Code**: Existing Python CLI Todo app logic in `src/todo_cli/`
- **Primary Entities**: Task model and TaskService from CLI app
- **API Framework**: FastAPI with Pydantic models
- **Authentication**: JWT-based (implementation deferred to later phase)
- **Data Storage**: File-based persistence (to be upgraded later)

## Constitution Check

- [ ] Verify all endpoints follow REST conventions
- [ ] Confirm data validation matches CLI app exactly
- [ ] Ensure error handling follows spec (400, 401, 403, 404)
- [ ] Check that ownership enforcement is implemented
- [ ] Validate JSON response formats match spec
- [ ] Verify security best practices are implemented
- [ ] Confirm performance targets are achievable
- [ ] Ensure deployment configuration is ready

## Gates

- [ ] All endpoints have corresponding tests written first (TDD)
- [ ] Error responses follow consistent format
- [ ] Validation rules match CLI implementation exactly
- [ ] Ownership checks prevent cross-user data access
- [ ] Performance targets (<100ms response time) are achievable
- [ ] Security measures are in place
- [ ] Deployment configuration is ready

---

## Phase 0: Research & Setup

### Research Tasks
- [ ] Investigate FastAPI best practices for authentication middleware
- [ ] Research file-based to database migration strategies
- [ ] Study rate limiting implementations for FastAPI
- [ ] Examine audit logging patterns in FastAPI applications

### Setup Tasks
- [ ] Initialize FastAPI application structure
- [ ] Set up project dependencies (FastAPI, uvicorn, pydantic, etc.)
- [ ] Configure testing framework (pytest, httpx for API testing)
- [ ] Import existing Python CLI models and services

---

## Phase 1: Data Models & API Contracts

### Data Model Implementation
- [ ] Create Pydantic models matching Task entity from CLI app
- [ ] Define request/response schemas for all endpoints
- [ ] Implement validation rules matching CLI app exactly
- [ ] Create error response models

### API Contract Implementation
- [ ] Define all 6 API endpoints with proper HTTP methods
- [ ] Set up path parameter validation
- [ ] Define request body schemas
- [ ] Define response schemas for success and error cases

---

## Phase 2: Implementation Order

### Endpoint Implementation Sequence

**Priority 1: GET endpoints (foundation for testing)**
1. [ ] **GET /api/{user_id}/tasks** - List all tasks for a user
   - [ ] Write tests first (empty list, multiple tasks, user isolation)
   - [ ] Implement endpoint using TaskService.get_all_tasks()
   - [ ] Add user ownership validation
   - [ ] Handle error cases (401, 403)

2. [ ] **GET /api/{user_id}/tasks/{id}** - Get single task details
   - [ ] Write tests first (valid task, not found, user isolation)
   - [ ] Implement endpoint using TaskService.get_task_by_id()
   - [ ] Add user ownership validation
   - [ ] Handle error cases (401, 403, 404)

**Priority 2: POST endpoint (creation)**
3. [ ] **POST /api/{user_id}/tasks** - Create new task
   - [ ] Write tests first (valid creation, validation errors)
   - [ ] Implement endpoint using TaskService.add_task()
   - [ ] Apply validation rules from CLI app
   - [ ] Handle error cases (400, 401, 403)

**Priority 3: PUT endpoint (update)**
4. [ ] **PUT /api/{user_id}/tasks/{id}** - Update existing task
   - [ ] Write tests first (valid update, not found, validation errors)
   - [ ] Implement endpoint using TaskService.update_task()
   - [ ] Apply validation rules from CLI app
   - [ ] Handle error cases (400, 401, 403, 404)

**Priority 4: PATCH endpoint (completion toggle)**
5. [ ] **PATCH /api/{user_id}/tasks/{id}/complete** - Toggle completion
   - [ ] Write tests first (valid toggle, not found, user isolation)
   - [ ] Implement endpoint using TaskService.mark_complete/mark_incomplete
   - [ ] Handle error cases (400, 401, 403, 404)

**Priority 5: DELETE endpoint (cleanup)**
6. [ ] **DELETE /api/{user_id}/tasks/{id}** - Delete task
   - [ ] Write tests first (valid deletion, not found, user isolation)
   - [ ] Implement endpoint using TaskService.delete_task()
   - [ ] Handle error cases (401, 403, 404)

---

## Phase 3: Validation & Ownership Implementation

### Input Validation
- [ ] Implement title validation (required, max 100 chars) matching CLI
- [ ] Implement description validation (optional, max 500 chars) matching CLI
- [ ] Implement completion status validation (boolean) matching CLI
- [ ] Create consistent validation error responses

### Ownership Enforcement
- [ ] Extract user ID from JWT token (placeholder for now)
- [ ] Verify user owns the task before operations
- [ ] Return 403 Forbidden for unauthorized access attempts
- [ ] Ensure user ID in path matches JWT token user ID

### Error Handling Integration
- [ ] Implement 400 Bad Request for validation errors
- [ ] Implement 401 Unauthorized for auth failures
- [ ] Implement 403 Forbidden for ownership violations
- [ ] Implement 404 Not Found for missing resources
- [ ] Ensure all error responses follow format: `{"error": "message"}`

---

## Phase 4: Testing & Verification

### Test-Driven Development Approach
For each endpoint, implement in this order:
1. [ ] Write comprehensive test suite covering all scenarios
2. [ ] Test valid requests and expected responses
3. [ ] Test all error conditions and status codes
4. [ ] Test user isolation (cross-user access prevention)
5. [ ] Test validation edge cases
6. [ ] Verify response format matches spec exactly

### Sample Test Scenarios
- [ ] Create task with valid data → 201 Created
- [ ] Create task with invalid title → 400 Bad Request
- [ ] Get all tasks for user with no tasks → 200 OK, empty array
- [ ] Get all tasks for user with multiple tasks → 200 OK, task array
- [ ] Get single task that exists → 200 OK, task object
- [ ] Get single task that doesn't exist → 404 Not Found
- [ ] Update existing task → 200 OK, updated task
- [ ] Update non-existent task → 404 Not Found
- [ ] Delete existing task → 204 No Content
- [ ] Delete non-existent task → 404 Not Found
- [ ] Access task owned by different user → 403 Forbidden

---

## Phase 5: Dependencies & Flow Notes

### Implementation Dependencies
- **GET endpoints first**: Needed to verify other operations worked
- **Authentication middleware**: Required before ownership enforcement
- **Pydantic models**: Foundation for request/response validation
- **Error handling utilities**: Shared across all endpoints

### Critical Path
1. Data models and validation schemas
2. GET endpoints for basic functionality
3. Authentication and ownership middleware
4. POST/PUT/PATCH/DELETE endpoints
5. Comprehensive testing and error handling

### Integration Points
- [ ] Frontend will call these endpoints for all task operations
- [ ] Authentication system will provide user context
- [ ] Future database migration will replace file storage
- [ ] Rate limiting will be applied to all endpoints
- [ ] Monitoring system will collect metrics
- [ ] Logging system will record all operations

---

## Phase 6: Performance & Non-Functional Requirements

### Performance Targets
- [ ] All endpoints respond in <100ms (p95)
- [ ] File I/O operations optimized for concurrent access
- [ ] Efficient user isolation mechanisms

### Audit & Compliance
- [ ] Log all task operations with user ID, timestamp, IP
- [ ] Track operation types (create, read, update, delete)
- [ ] Implement rate limiting (1000 requests/hour/user)

### Future Considerations
- [ ] Prepare for database migration from file storage
- [ ] Plan for optimistic locking mechanism
- [ ] Design for horizontal scaling
- [ ] Plan caching strategy for read operations

---

## Phase 7: Environment Setup & Dependencies

### Environment Configuration
- [ ] Set up virtual environment with Python 3.8+
- [ ] Install FastAPI and uvicorn: `pip install fastapi uvicorn`
- [ ] Install Pydantic: `pip install pydantic`
- [ ] Install security dependencies: `pip install python-jose[cryptography] passlib[bcrypt]`
- [ ] Install testing dependencies: `pip install pytest httpx pytest-cov`
- [ ] Install rate limiting: `pip install slowapi`
- [ ] Install environment management: `pip install python-dotenv`

### Environment Variables Setup
- [ ] Create `.env` file with configuration variables
- [ ] Define `TODO_STORAGE_FILE` for task persistence
- [ ] Define `JWT_SECRET_KEY` for token generation
- [ ] Define `JWT_ALGORITHM` for token encoding
- [ ] Define `ACCESS_TOKEN_EXPIRE_MINUTES` for token expiration
- [ ] Define `LOG_LEVEL` for application logging
- [ ] Define `DATABASE_URL` for future database connection

### Project Structure Setup
- [ ] Create `src/api/` directory for FastAPI application
- [ ] Create `src/api/models/` for Pydantic models
- [ ] Create `src/api/routers/` for API routes
- [ ] Create `src/api/services/` for business logic wrappers
- [ ] Create `src/api/utils/` for utility functions
- [ ] Create `src/api/middleware/` for middleware components
- [ ] Create `src/api/config/` for configuration management

---

## Phase 8: Security & Authentication

### Authentication Implementation
- [ ] Create JWT token generation and verification utilities
- [ ] Implement authentication middleware
- [ ] Create authentication dependency for protected endpoints
- [ ] Implement password hashing utilities
- [ ] Add CSRF protection if needed
- [ ] Implement session management considerations

### Security Best Practices
- [ ] Add input sanitization and validation
- [ ] Implement protection against common web vulnerabilities (XSS, CSRF, SQL injection)
- [ ] Add request rate limiting to prevent abuse
- [ ] Implement secure headers (CORS, CSP, etc.)
- [ ] Add API key management if needed for third-party access
- [ ] Implement encryption for sensitive data

### Rate Limiting
- [ ] Implement per-user rate limiting (1000 requests/hour/user)
- [ ] Create rate limiter middleware
- [ ] Add rate limit headers to responses
- [ ] Implement different rate limits for different endpoints
- [ ] Add rate limit bypass for admin users if needed

---

## Phase 9: Advanced Testing Strategy

### Testing Types
- [ ] Unit tests for individual service methods
- [ ] Integration tests for API endpoints
- [ ] Security tests for authentication and authorization
- [ ] Performance tests for response times
- [ ] Load tests for concurrent users
- [ ] API contract tests to ensure consistency

### Advanced Test Scenarios
- [ ] Rate limit exceeded → 429 Too Many Requests
- [ ] Invalid JWT token → 401 Unauthorized
- [ ] Malformed request body → 400 Bad Request
- [ ] Large payload handling → 413 Payload Too Large
- [ ] Cross-site scripting attempts → Blocked
- [ ] SQL injection attempts → Blocked

---

## Phase 10: Performance Optimization

### Performance Targets
- [ ] All endpoints respond in <100ms (p95)
- [ ] File I/O operations optimized for concurrent access
- [ ] Efficient user isolation mechanisms
- [ ] Caching strategy for read-heavy operations
- [ ] Database connection pooling (when migrated)
- [ ] Memory usage optimization

### Caching Strategy
- [ ] Plan caching for GET endpoints to improve performance
- [ ] Implement cache invalidation strategies
- [ ] Consider Redis for distributed caching (future)
- [ ] Add cache headers to responses
- [ ] Plan for cache warming strategies

---

## Phase 11: Deployment & Monitoring

### Containerization
- [ ] Create Dockerfile for the application
- [ ] Create docker-compose.yml for development environment
- [ ] Configure production-ready Docker setup
- [ ] Optimize Docker image size
- [ ] Implement multi-stage Docker builds

### Health Checks & Monitoring
- [ ] Create health check endpoint (`/health`)
- [ ] Implement readiness and liveness probes
- [ ] Set up metrics collection (Prometheus integration)
- [ ] Configure logging for monitoring systems
- [ ] Create monitoring dashboards
- [ ] Set up alerting for critical issues

### Configuration Management
- [ ] Environment-specific configuration files
- [ ] Secure secret management
- [ ] Feature flag implementation
- [ ] Configuration validation
- [ ] Zero-downtime deployment configuration

---

## Phase 12: Future Migration Path

### Database Migration Strategy
- [ ] Plan migration from file storage to database
- [ ] Design database schema matching current models
- [ ] Create migration scripts for existing data
- [ ] Plan for zero-downtime migration
- [ ] Test migration process in staging environment

### Advanced Features
- [ ] Plan for optimistic locking mechanism
- [ ] Design for horizontal scaling
- [ ] Plan caching strategy for read operations
- [ ] Implement real-time updates with WebSockets (future)
- [ ] Plan for microservices architecture (future)
- [ ] Consider GraphQL API alongside REST (future)

### Maintenance & Operations
- [ ] Create runbooks for common operations
- [ ] Plan for automated backups
- [ ] Implement automated testing pipeline
- [ ] Create deployment automation scripts
- [ ] Plan for rollback procedures
- [ ] Document operational procedures