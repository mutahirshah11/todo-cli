# Quickstart Guide: Authentication Implementation

## Prerequisites
- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- Better Auth library installed
- Existing Todo application codebase

## Environment Setup

### Backend (FastAPI)
1. Install required packages:
```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

2. Add JWT secret to environment:
```bash
# .env
JWT_SECRET_KEY=your-super-secret-jwt-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Frontend (Next.js)
1. Install Better Auth:
```bash
npm install better-auth
```

2. Configure auth environment:
```bash
# frontend/.env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Implementation Steps

### 1. Frontend Auth Setup
1. Create auth provider in `frontend/src/providers/auth-provider.tsx`
2. Set up Better Auth client configuration
3. Implement login/register forms in dedicated routes
4. Add auth state management hooks

### 2. Backend JWT Middleware
1. Create JWT utility functions for token creation/validation
2. Implement auth middleware for token verification
3. Add user identity extraction from JWT claims
4. Apply middleware to all protected endpoints

### 3. Task Ownership Verification
1. Update existing task endpoints to verify user_id from JWT
2. Ensure 403 Forbidden responses for cross-user access attempts
3. Test user isolation with multi-user scenarios

### 4. API Integration
1. Configure frontend to attach JWT tokens to all API requests
2. Handle 401/403 responses appropriately
3. Implement token refresh logic for expired tokens

## Testing Commands

### Backend Tests
```bash
# Run all auth-related tests
pytest tests/unit/test_auth_service.py
pytest tests/integration/test_auth_endpoints.py
pytest tests/contract/test_auth_contracts.py

# Run with coverage
pytest --cov=backend/api/services/auth_service.py
```

### Frontend Tests
```bash
# Run auth component tests
npm test src/components/auth/
npm test src/hooks/useAuth.test.ts

# Run integration tests
npm run test:integration auth-flow
```

## Key Endpoints

### Auth Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user info

### Protected Task Endpoints (require JWT)
- `GET /api/v1/{user_id}/tasks` - Get user's tasks
- `POST /api/v1/{user_id}/tasks` - Create user's task
- `PUT /api/v1/{user_id}/tasks/{id}` - Update user's task
- `DELETE /api/v1/{user_id}/tasks/{id}` - Delete user's task
- `PATCH /api/v1/{user_id}/tasks/{id}/complete` - Toggle task completion

## Error Responses

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing authentication token",
  "code": "AUTH_001"
}
```

### 403 Forbidden
```json
{
  "error": "Forbidden",
  "message": "Access denied - insufficient permissions",
  "code": "AUTH_002"
}
```

## Development Workflow

1. Start backend: `uvicorn main:app --reload`
2. Start frontend: `npm run dev`
3. Register user through UI
4. Log in and obtain JWT token
5. Perform task operations with authenticated context
6. Test token expiration scenarios
7. Verify user isolation for tasks