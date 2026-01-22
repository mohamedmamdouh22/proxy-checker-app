"""Test cases for proxy checking endpoints."""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app_name"] == "Proxy Checker API"
    assert data["version"] == "1.0.0"


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data


def test_check_proxy_invalid_request():
    """Test proxy check with invalid request."""
    response = client.post("/api/v1/proxy/check", json={})
    assert response.status_code == 422  # Validation error


def test_check_batch_invalid_request():
    """Test batch proxy check with invalid request."""
    response = client.post("/api/v1/proxy/check-batch", json={})
    assert response.status_code == 422  # Validation error


def test_check_batch_empty_list():
    """Test batch proxy check with empty list."""
    response = client.post("/api/v1/proxy/check-batch", json={"proxies": []})
    assert response.status_code == 422  # Validation error (min 1 item)


def test_openapi_schema():
    """Test that OpenAPI schema is accessible."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert data["info"]["title"] == "Proxy Checker API"
