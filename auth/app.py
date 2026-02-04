from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from api.routers import auth

# Create FastAPI app instance
app = FastAPI(
    title="Authentication Service",
    description="Standalone Authentication API using Better Auth principles",
    version="1.0.0"
)

# Add standard CORS middleware
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
# Add common dev origins if not present
if "*" not in allowed_origins:
    dev_origins = ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001"]
    for origin in dev_origins:
        if origin not in allowed_origins:
            allowed_origins.append(origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers including Authorization
    # Expose authorization header to frontend
    expose_headers=["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials", "Authorization"]
)

# Include API routers
app.include_router(auth.router, prefix="", tags=["Authentication"])

@app.get("/")
async def root():
    return {"message": "Authentication Service", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    """Startup event that runs when the application starts."""
    print("Authentication service started successfully")
    print("Ready for user registration and authentication")
    # No demo user creation - users must register themselves