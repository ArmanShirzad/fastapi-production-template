# FastAPI Production Starter Template

[![CI](https://github.com/armanshirzad/FastiApiTemplate/actions/workflows/ci.yml/badge.svg)](https://github.com/armanshirzad/FastiApiTemplate/actions/workflows/ci.yml)
[![Release](https://github.com/armanshirzad/FastiApiTemplate/actions/workflows/release.yml/badge.svg)](https://github.com/armanshirzad/FastiApiTemplate/actions/workflows/release.yml)
[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ghcr.io%2Farmanshirzad%2Ffastiapitemplate-blue.svg)](https://github.com/armanshirzad/FastiApiTemplate/pkgs/container/fastiapitemplate)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/armanshirzad/FastiApiTemplate/badge)](https://api.securityscorecards.dev/projects/github.com/armanshirzad/FastiApiTemplate)

A production-ready FastAPI template with Docker, CI/CD, observability, and one-click deployment to Render or Koyeb.

## Features

- **FastAPI** with Python 3.12
- **Docker** multi-stage build for production
- **Prometheus** metrics integration
- **Sentry** error tracking
- **PostgreSQL** support (optional)
- **Health checks** for monitoring
- **One-click deploy** to Render or Koyeb
- **GitHub Actions** CI/CD
- **GitHub Container Registry** publishing
- **Testing** with pytest
- **Code quality** with ruff

## Quick Deploy

### Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/armanshirzad/FastiApiTemplate)

1. Fork this repository
2. Connect your GitHub account to Render
3. Click "Deploy to Render" button above
4. Configure environment variables
5. Deploy!

### Deploy to Koyeb

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=docker&image=ghcr.io/armanshirzad/fastiapitemplate:latest)

1. Fork this repository
2. Create account at [Koyeb](https://app.koyeb.com)
3. Click "Deploy to Koyeb" button above
4. Configure environment variables
5. Deploy!

## CI/CD Overview

- **Workflow files:** `.github/workflows/ci.yml` for lint, tests, and Docker build; `.github/workflows/release.yml` for multi-arch image publishes and tagged releases.
- **Registry:** pushes to `ghcr.io/armanshirzad/fastiapitemplate`.
- **Branch strategy:** run CI on `main` and `develop`, require tags `v*` for releases.
- **Health check:** release job hits `/health` after building the Docker image to ensure the container boots.

## Quick Start

```bash
# Clone and setup
git clone <your-repo-url>
cd FastiApiTemplate
cp .env.example .env

# Run locally (no database)
make dev

# Or with PostgreSQL
make docker-compose-up
```

## Architecture

```
┌─────────┐      ┌──────────────┐      ┌──────────┐
│ Client  │─────>│   FastAPI    │─────>│ Database │
└─────────┘      │   + Metrics  │      │(optional)│
                 │   + Sentry   │      └──────────┘
                 └──────────────┘
                        │
                        v
                 ┌──────────────┐
                 │  Prometheus  │
                 │   /metrics   │
                 └──────────────┘
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | FastAPI Template |
| `APP_VERSION` | Application version | 0.1.0 |
| `ENVIRONMENT` | Environment (dev/staging/prod) | development |
| `DEBUG` | Debug mode | True |
| `LOG_LEVEL` | Logging level | INFO |
| `DATABASE_URL` | Database connection string | (optional) |
| `SECRET_KEY` | Secret key for security | (generated if not provided) |
| `CORS_ORIGINS` | CORS allowed origins | (empty for security) |
| `SENTRY_DSN` | Sentry DSN for error tracking | (optional) |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |

## Secret Configuration

The template works out of the box with sensible defaults, but you can enhance it by adding secrets in your repository Settings:

- **`SECRET_KEY`** - Real random string for production signing (dev generates one automatically)
- **`DATABASE_URL`** - PostgreSQL connection for production and integration tests
- **`SENTRY_DSN`** - Enable Sentry error tracking and release notifications

### What happens when secrets are provided:

- **`DATABASE_URL`** → Enables PostgreSQL integration tests in CI
- **`SENTRY_DSN`** → Enables Sentry release step in GitHub Actions
- **`SECRET_KEY`** → Required for production; dev mode generates one if missing

## Database Options

### Without Database (Minimal)
Leave `DATABASE_URL` empty in `.env` for a minimal API without database dependencies.

### With PostgreSQL
Set `DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname` in `.env`.

## Development

```bash
# Install dependencies
make install

# Run development server
make dev

# Run tests
make test

# Lint code
make lint

# Format code
make format

# Build Docker image
make docker-build

# Run with Docker Compose (includes PostgreSQL)
make docker-compose-up
```

## Observability

### Prometheus Metrics
- Endpoint: `/metrics`
- Metrics: HTTP requests, duration, status codes
- Integration: `prometheus-fastapi-instrumentator`

### Sentry Integration
- Automatic error tracking
- Performance monitoring
- Configure via `SENTRY_DSN` environment variable

### Health Checks
- `/health` - Basic health check
- `/health/ready` - Readiness check (includes database)

## Project Structure

```
app/
├── __init__.py
├── main.py              # FastAPI application
├── config.py            # Configuration settings
├── api/
│   ├── __init__.py
│   └── routes/
│       ├── __init__.py
│       ├── health.py    # Health check endpoints
│       └── example.py   # Example CRUD endpoints
├── core/
│   ├── __init__.py
│   ├── database.py      # Database configuration
│   └── metrics.py       # Prometheus metrics
├── models/              # SQLAlchemy models (optional)
└── services/            # Business logic layer
tests/
├── __init__.py
├── conftest.py
└── test_health.py
```

## Security

This template includes several security features:

- **CORS Protection**: Empty origins by default (configure via `CORS_ORIGINS`)
- **Trusted Host Middleware**: Prevents host header attacks in production
- **Non-root Docker User**: Runs as `appuser` instead of root
- **Security Headers**: Basic security middleware included
- **Dependency Scanning**: Dependabot for automated security updates
- **Code Analysis**: CodeQL and Scorecard security scanning

For security vulnerabilities, please see [SECURITY.md](SECURITY.md).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run `make test` and `make lint`
6. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.
