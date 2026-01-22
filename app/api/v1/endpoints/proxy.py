"""Proxy checking endpoints."""
from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.core.schemas import (
    ProxyCheckRequest,
    ProxyCheckResponse,
    ProxyBatchCheckRequest,
    ProxyBatchCheckResponse,
)
from app.services.proxy_checker import ProxyChecker, ProxyStatus

router = APIRouter()


@router.post(
    "/check",
    response_model=ProxyCheckResponse,
    summary="Check a single proxy",
    description="Test a single proxy for connectivity and retrieve geographic information",
)
async def check_proxy(request: ProxyCheckRequest) -> ProxyCheckResponse:
    """
    Check if a single proxy is working.

    Args:
        request: ProxyCheckRequest containing proxy URL and timeout

    Returns:
        ProxyCheckResponse with proxy test results

    Raises:
        HTTPException: If the request is invalid
    """
    try:
        checker = ProxyChecker(
            timeout=request.timeout,
            test_url=settings.test_url,
        )
        result = await checker.check_proxy(request.proxy)

        return ProxyCheckResponse(
            proxy=result.proxy,
            status=result.status.value,
            response_time=result.response_time,
            ip_address=result.ip_address,
            country=result.country,
            city=result.city,
            error=result.error,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking proxy: {str(e)}")


@router.post(
    "/check-batch",
    response_model=ProxyBatchCheckResponse,
    summary="Check multiple proxies",
    description="Test multiple proxies concurrently and get aggregated results",
)
async def check_batch(request: ProxyBatchCheckRequest) -> ProxyBatchCheckResponse:
    """
    Check multiple proxies concurrently.

    Args:
        request: ProxyBatchCheckRequest containing list of proxies and settings

    Returns:
        ProxyBatchCheckResponse with all results and statistics

    Raises:
        HTTPException: If the request is invalid
    """
    try:
        checker = ProxyChecker(
            timeout=request.timeout,
            test_url=settings.test_url,
        )
        results = await checker.check_proxies(
            request.proxies,
            max_concurrent=request.max_concurrent,
        )

        # Convert results to response models
        response_results = [
            ProxyCheckResponse(
                proxy=r.proxy,
                status=r.status.value,
                response_time=r.response_time,
                ip_address=r.ip_address,
                country=r.country,
                city=r.city,
                error=r.error,
            )
            for r in results
        ]

        # Calculate statistics
        total = len(results)
        working = sum(1 for r in results if r.status == ProxyStatus.WORKING)
        failed = total - working
        success_rate = round((working / total * 100), 2) if total > 0 else 0.0

        return ProxyBatchCheckResponse(
            results=response_results,
            total=total,
            working=working,
            failed=failed,
            success_rate=success_rate,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking proxies: {str(e)}")
