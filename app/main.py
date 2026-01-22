"""FastAPI application entry point."""
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.schemas import HealthResponse

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Include API v1 router
app.include_router(api_router, prefix="/api/v1")

# Mount static files
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get(
    "/api/v1/health",
    response_model=HealthResponse,
    tags=["health"],
    summary="Health check",
    description="Check if the API is running and healthy",
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns:
        HealthResponse with API status and version information
    """
    return HealthResponse(
        status="healthy",
        app_name=settings.app_name,
        version=settings.app_version,
    )


@app.get(
    "/",
    include_in_schema=False,
)
async def root():
    """
    Serve the frontend application.

    Returns:
        HTML page for the proxy checker UI
    """
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))

    # Fallback to API info if frontend not available
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/api/v1/health",
    }
