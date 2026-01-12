# Authentication Service

Standalone authentication service for the Todo application using JWT-based authentication.

## Overview

This service handles all authentication-related functionality including:
- User registration
- User login
- Token generation and validation
- User session management

## Endpoints

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login with email and password
- `GET /auth/me` - Get current authenticated user info

## Running the Service

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
cd auth
pip install -r requirements.txt
```

### Running Locally

```bash
python start_auth_service.py --port 8001
```

Or with auto-reload for development:
```bash
python start_auth_service.py --port 8001 --reload
```

### Using Docker

```bash
# Build the image
docker build -t auth-service .

# Run the container
docker run -p 8001:8001 auth-service
```

## Environment Variables

- `SECRET_KEY`: Secret key for JWT signing (defaults to "your-secret-key-change-in-production")

## Architecture

The auth service is designed to be deployed separately and accessed by the frontend for authentication operations. The backend services validate JWT tokens independently to protect resources.

## API Usage

### Registration

```bash
curl -X POST http://localhost:8001/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### Login

```bash
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### Get Current User

```bash
curl -X GET http://localhost:8001/auth/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```