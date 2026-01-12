# Data Model: Authentication and Authorization for Todo Application

## User Entity
**Entity Name**: User
**Fields**:
- `id`: String (UUID) - Unique identifier for the user
- `email`: String - User's email address (unique, validated format)
- `password_hash`: String - Hashed password (stored securely)
- `created_at`: DateTime - Timestamp of account creation
- `updated_at`: DateTime - Timestamp of last update
- `is_active`: Boolean - Whether the account is active

**Validation Rules**:
- Email: Valid email format
- Password: Minimum 8 characters with mixed case, numbers, and special characters (as per spec)
- ID: Must be unique across all users

## JWT Token Entity
**Entity Name**: JWT Token
**Fields**:
- `token`: String - The JWT token string
- `user_id`: String - Reference to the user
- `expires_at`: DateTime - Expiration timestamp (1 hour from issue)
- `issued_at`: DateTime - Issue timestamp
- `type`: String - Token type (access/refresh)

**Validation Rules**:
- Token: Proper JWT format with valid signature
- Expiry: Must be within 1 hour of issue for access tokens
- User ID: Must correspond to an existing user

## Session Entity (Logical)
**Entity Name**: Session
**Fields**:
- `user_id`: String - Reference to the authenticated user
- `token_valid`: Boolean - Whether the token is currently valid
- `last_access`: DateTime - Last time the session was used

**Validation Rules**:
- User must be authenticated with valid JWT
- Session is stateless - relies entirely on token validity

## Task Access Relationship
**Relationship**: User ↔ Task (Ownership)
**Rule**: Each task belongs to exactly one user
**Validation**:
- When creating a task: assign to authenticated user
- When accessing a task: verify user_id matches token's user_id
- When modifying a task: verify user_id matches token's user_id

## State Transitions

### User Registration
```
Anonymous → Pending Verification → Active
```
- Anonymous: Not yet registered
- Pending Verification: Registration initiated, email verification may be needed
- Active: Account confirmed and ready for use

### User Authentication
```
Unauthenticated → Authenticating → Authenticated → Session Active
```
- Unauthenticated: No valid token present
- Authenticating: Login/registration in progress
- Authenticated: Valid JWT obtained
- Session Active: Token validated by backend, user context available

## API Request Flow with Authentication

### Authenticated Request Processing
1. Client sends request with `Authorization: Bearer <token>`
2. Server validates JWT signature and expiry
3. Server extracts user_id from token claims
4. Server verifies user_id matches route/user context
5. Server processes request with user context
6. Server returns response

### Unauthorized Request Handling
1. Client sends request without valid token
2. Server detects missing/invalid token
3. Server returns 401 Unauthorized
4. Client handles error appropriately

### Cross-User Access Attempt
1. Client sends request with valid token for user A
2. Request targets resources for user B
3. Server validates token belongs to user A
4. Server detects user mismatch
5. Server returns 403 Forbidden