"""Pydantic models for API request and response validation."""
from typing import Optional
from pydantic import BaseModel, Field


class ProxyCheckRequest(BaseModel):
    """Request model for checking a single proxy."""

    proxy: str = Field(
        ...,
        description="Proxy URL in format: protocol://host:port or host:port",
        examples=["http://proxy.example.com:8080", "user:pass@proxy.com:3128"],
    )
    timeout: int = Field(
        default=10,
        ge=1,
        le=60,
        description="Timeout in seconds (1-60)",
    )


class ProxyBatchCheckRequest(BaseModel):
    """Request model for checking multiple proxies."""

    proxies: list[str] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="List of proxy URLs (max 100)",
        examples=[["http://proxy1.com:8080", "http://proxy2.com:3128"]],
    )
    timeout: int = Field(
        default=10,
        ge=1,
        le=60,
        description="Timeout in seconds (1-60)",
    )
    max_concurrent: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum concurrent checks (1-50)",
    )


class ProxyCheckResponse(BaseModel):
    """Response model for proxy check result."""

    proxy: str = Field(..., description="The proxy URL that was tested")
    status: str = Field(..., description="Status: working, failed, or timeout")
    response_time: Optional[float] = Field(
        None,
        description="Response time in seconds (null if failed)",
    )
    ip_address: Optional[str] = Field(
        None,
        description="External IP address visible through proxy",
    )
    country: Optional[str] = Field(
        None,
        description="Country of the proxy IP",
    )
    city: Optional[str] = Field(
        None,
        description="City of the proxy IP",
    )
    error: Optional[str] = Field(
        None,
        description="Error message if check failed",
    )


class ProxyBatchCheckResponse(BaseModel):
    """Response model for batch proxy check."""

    results: list[ProxyCheckResponse] = Field(
        ...,
        description="List of proxy check results",
    )
    total: int = Field(..., description="Total number of proxies checked")
    working: int = Field(..., description="Number of working proxies")
    failed: int = Field(..., description="Number of failed proxies")
    success_rate: float = Field(..., description="Success rate as percentage")


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""

    status: str = Field(default="healthy", description="API health status")
    app_name: str = Field(..., description="Application name")
    version: str = Field(..., description="Application version")
