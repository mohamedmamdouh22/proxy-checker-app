# Proxy Checker API

A production-ready FastAPI application for testing HTTP/HTTPS/SOCKS proxies with geographic location detection.

## Features

- **Web UI** - Beautiful, responsive single-page frontend
- Test single or multiple proxies concurrently
- Async/await support for high performance
- Geographic location detection (IP, country, city)
- Response time measurement
- RESTful API with OpenAPI documentation
- Docker containerization
- Health check endpoint
- CORS support
- Environment-based configuration

## Tech Stack

- **FastAPI** - Modern, fast web framework
- **uvicorn** - Lightning-fast ASGI server
- **aiohttp** - Async HTTP client for proxy testing
- **Pydantic** - Data validation using Python type hints
- **uv** - Fast Python package manager
- **Docker** - Container platform

## Project Structure

```
proxy-checker/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   └── proxy.py      # Proxy endpoints
│   │       └── router.py          # API router
│   ├── core/
│   │   ├── config.py              # Configuration
│   │   └── schemas.py             # Pydantic models
│   ├── services/
│   │   └── proxy_checker.py       # Proxy checking logic
│   └── main.py                    # FastAPI app
├── static/
│   └── index.html                 # Web UI frontend
├── tests/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── proxy_checker.py               # CLI version
```

## Installation

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Docker (for containerized deployment)

### Local Development

1. **Install uv** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Clone the repository** (or navigate to the project directory):
```bash
cd proxy-checker
```

3. **Install dependencies**:
```bash
uv sync
```

4. **Run the application**:
```bash
uv run uvicorn app.main:app --reload
```

5. **Access the application**:
   - **Web UI**: http://localhost:8000 (Main interface)
   - API docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health: http://localhost:8000/api/v1/health

### Docker Deployment

#### Using Docker Compose (Recommended)

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

#### Using Docker directly

```bash
# Build the image
docker build -t proxy-checker .

# Run the container
docker run -d -p 8000:8000 --name proxy-checker-api proxy-checker

# View logs
docker logs -f proxy-checker-api

# Stop the container
docker stop proxy-checker-api
docker rm proxy-checker-api
```

## Using the Web Interface

The application includes a beautiful, responsive web interface accessible at the root URL.

### Features

- **Single Proxy Check**: Test individual proxies with custom timeout settings
- **Batch Checking**: Test up to 100 proxies simultaneously
- **Real-time Results**: See live results with response times and geographic data
- **Statistics Dashboard**: View success rates, working/failed counts
- **Mobile Responsive**: Works perfectly on all device sizes

### How to Use

1. **Open your browser** and navigate to http://localhost:8000

2. **Single Proxy Tab**:
   - Enter a proxy URL (e.g., `http://proxy.example.com:8080`)
   - Set timeout (1-60 seconds)
   - Click "Check Proxy"
   - View results with IP, location, and response time

3. **Batch Check Tab**:
   - Enter multiple proxies (one per line)
   - Configure timeout and max concurrent connections
   - Click "Check All Proxies"
   - View comprehensive results table with statistics

### Supported Proxy Formats

- `http://proxy.example.com:8080`
- `https://proxy.example.com:8080`
- `proxy.example.com:8080` (assumes http://)
- `user:pass@proxy.example.com:8080`
- `http://user:pass@proxy.example.com:8080`
- `socks4://proxy.example.com:1080`
- `socks5://proxy.example.com:1080`

## API Endpoints

### Health Check

```bash
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "app_name": "Proxy Checker API",
  "version": "1.0.0"
}
```

### Check Single Proxy

```bash
POST /api/v1/proxy/check
```

**Request body:**
```json
{
  "proxy": "http://proxy.example.com:8080",
  "timeout": 10
}
```

**Response:**
```json
{
  "proxy": "http://proxy.example.com:8080",
  "status": "working",
  "response_time": 1.23,
  "ip_address": "123.45.67.89",
  "country": "United States",
  "city": "New York",
  "error": null
}
```

### Check Multiple Proxies

```bash
POST /api/v1/proxy/check-batch
```

**Request body:**
```json
{
  "proxies": [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:3128",
    "192.168.1.100:8080"
  ],
  "timeout": 10,
  "max_concurrent": 10
}
```

**Response:**
```json
{
  "results": [
    {
      "proxy": "http://proxy1.example.com:8080",
      "status": "working",
      "response_time": 1.23,
      "ip_address": "123.45.67.89",
      "country": "United States",
      "city": "New York",
      "error": null
    },
    {
      "proxy": "http://proxy2.example.com:3128",
      "status": "failed",
      "response_time": null,
      "ip_address": null,
      "country": null,
      "city": null,
      "error": "Connection timeout"
    }
  ],
  "total": 2,
  "working": 1,
  "failed": 1,
  "success_rate": 50.0
}
```

## Usage Examples

### Using curl

```bash
# Check single proxy
curl -X POST http://localhost:8000/api/v1/proxy/check \
  -H "Content-Type: application/json" \
  -d '{"proxy": "http://proxy.example.com:8080", "timeout": 10}'

# Check multiple proxies
curl -X POST http://localhost:8000/api/v1/proxy/check-batch \
  -H "Content-Type: application/json" \
  -d '{
    "proxies": ["http://proxy1.com:8080", "http://proxy2.com:3128"],
    "timeout": 10,
    "max_concurrent": 10
  }'
```

### Using Python requests

```python
import requests

# Check single proxy
response = requests.post(
    "http://localhost:8000/api/v1/proxy/check",
    json={"proxy": "http://proxy.example.com:8080", "timeout": 10}
)
print(response.json())

# Check multiple proxies
response = requests.post(
    "http://localhost:8000/api/v1/proxy/check-batch",
    json={
        "proxies": [
            "http://proxy1.com:8080",
            "http://proxy2.com:3128"
        ],
        "timeout": 10,
        "max_concurrent": 10
    }
)
print(response.json())
```

### Using the CLI (Original Script)

The original CLI script is still available for direct command-line usage:

```bash
# Check proxies from file
uv run python proxy_checker.py -f proxies.txt

# Check single proxy
uv run python proxy_checker.py -p "http://proxy.example.com:8080"

# Save working proxies
uv run python proxy_checker.py -f proxies.txt -o working_proxies.txt
```

## Configuration

Environment variables can be configured in `.env` file or passed directly:

```bash
# Application
APP_NAME="Proxy Checker API"
APP_VERSION="1.0.0"

# Server
HOST="0.0.0.0"
PORT=8000

# Proxy Testing
DEFAULT_TIMEOUT=10
DEFAULT_MAX_CONCURRENT=10
TEST_URL="http://ip-api.com/json/"

# CORS
CORS_ORIGINS=["*"]
```

## Proxy Format

The API accepts proxies in various formats:

- `http://host:port`
- `https://host:port`
- `socks4://host:port`
- `socks5://host:port`
- `host:port` (assumes http://)
- `username:password@host:port`
- `http://username:password@host:port`

## Development

### Running tests

```bash
# Install dev dependencies
uv sync --dev

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=app tests/
```

### Code formatting and linting

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .
```

## Production Deployment

### Environment Variables for Production

Create a `.env` file:

```bash
APP_NAME="Proxy Checker API"
DEFAULT_TIMEOUT=10
DEFAULT_MAX_CONCURRENT=20
CORS_ORIGINS=["https://yourdomain.com"]
```

### Using Docker Compose in Production

```bash
# Modify docker-compose.yml to remove volume mounts
# Build and start
docker-compose up -d

# Scale if needed
docker-compose up -d --scale proxy-checker=3
```

### Kubernetes Deployment

Example deployment configuration:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: proxy-checker
spec:
  replicas: 3
  selector:
    matchLabels:
      app: proxy-checker
  template:
    metadata:
      labels:
        app: proxy-checker
    spec:
      containers:
      - name: proxy-checker
        image: proxy-checker:latest
        ports:
        - containerPort: 8000
        env:
        - name: DEFAULT_MAX_CONCURRENT
          value: "20"
        livenessProbe:
          httpGet:
            path: /api/v1/health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
```

## Performance Considerations

- **Concurrent checks**: Adjust `max_concurrent` based on your system resources
- **Timeout**: Lower timeouts improve throughput but may miss slow proxies
- **Batch size**: Keep batch requests under 100 proxies for optimal response times
- **Rate limiting**: Consider adding rate limiting for public deployments

## Security

- Runs as non-root user in Docker
- No authentication by default (add authentication for production use)
- CORS configured (adjust for production domains)
- Environment-based secrets management

## Troubleshooting

### Port already in use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process or use a different port
uv run uvicorn app.main:app --port 8001
```

### Docker build fails

```bash
# Clean Docker cache
docker builder prune

# Rebuild without cache
docker-compose build --no-cache
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue in the repository.
