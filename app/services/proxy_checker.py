"""Proxy checking service module."""
import asyncio
import time
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

import aiohttp


class ProxyStatus(Enum):
    """Proxy status enumeration."""

    WORKING = "working"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class ProxyResult:
    """Result of a proxy check operation."""

    proxy: str
    status: ProxyStatus
    response_time: Optional[float] = None
    ip_address: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    error: Optional[str] = None


class ProxyChecker:
    """Service for checking proxy connectivity and performance."""

    def __init__(self, timeout: int = 10, test_url: str = "http://ip-api.com/json/"):
        """
        Initialize proxy checker.

        Args:
            timeout: Connection timeout in seconds
            test_url: URL to test proxies against (ip-api.com for geo location)
        """
        self.timeout = timeout
        self.test_url = test_url

    async def check_proxy(self, proxy: str) -> ProxyResult:
        """
        Check if a single proxy is working.

        Args:
            proxy: Proxy string in format 'protocol://host:port' or 'host:port'

        Returns:
            ProxyResult with validation details
        """
        # Normalize proxy format
        if not proxy.startswith(("http://", "https://", "socks4://", "socks5://")):
            proxy = f"http://{proxy}"

        start_time = time.time()

        try:
            proxy_url = proxy

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.test_url,
                    proxy=proxy_url,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                    ssl=False,
                ) as response:
                    response_time = time.time() - start_time

                    if response.status == 200:
                        data = await response.json()

                        return ProxyResult(
                            proxy=proxy,
                            status=ProxyStatus.WORKING,
                            response_time=round(response_time, 2),
                            ip_address=data.get("query"),
                            country=data.get("country"),
                            city=data.get("city"),
                        )
                    else:
                        return ProxyResult(
                            proxy=proxy,
                            status=ProxyStatus.FAILED,
                            error=f"HTTP {response.status}",
                        )

        except asyncio.TimeoutError:
            return ProxyResult(
                proxy=proxy,
                status=ProxyStatus.TIMEOUT,
                error="Connection timeout",
            )
        except Exception as e:
            return ProxyResult(
                proxy=proxy,
                status=ProxyStatus.FAILED,
                error=str(e),
            )

    async def check_proxies(
        self, proxies: List[str], max_concurrent: int = 10
    ) -> List[ProxyResult]:
        """
        Check multiple proxies concurrently.

        Args:
            proxies: List of proxy strings
            max_concurrent: Maximum number of concurrent checks

        Returns:
            List of ProxyResult objects
        """
        semaphore = asyncio.Semaphore(max_concurrent)

        async def check_with_semaphore(proxy: str) -> ProxyResult:
            async with semaphore:
                return await self.check_proxy(proxy)

        tasks = [check_with_semaphore(proxy) for proxy in proxies]
        results = await asyncio.gather(*tasks)

        return results
