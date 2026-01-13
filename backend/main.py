from fastapi import FastAPI
from api.routers import tasks
from api.config.settings import settings
from api.config.security import add_security_middleware
from api.middleware.request_size import RequestSizeLimitMiddleware
from api.middleware.correlation_id import CorrelationIdMiddleware
from api.handlers.error_handlers import add_error_handlers


# Create FastAPI app instance
app = FastAPI(
    title="Todo API",
    description="REST API for Todo Full-Stack Web Application",
    version="1.0.0"
)

# Add various middleware layers
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(RequestSizeLimitMiddleware, max_size=10 * 1024 * 1024)  # 10MB limit
add_security_middleware(app)

# Include API routers
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])

# Add error handlers
add_error_handlers(app)

@app.get("/")
async def root():
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}