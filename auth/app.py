from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import auth

# Create FastAPI app instance
app = FastAPI(
    title="Authentication Service",
    description="Standalone Authentication API using Better Auth principles",
    version="1.0.0"
)

# Add standard CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "*"],  # Allow frontend origin
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