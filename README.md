# FastAPI Production Starter Template

[![CI](https://github.com/armanshirzad/fastapi-production-template/actions/workflows/ci.yml/badge.svg)](https://github.com/armanshirzad/fastapi-production-template/actions/workflows/ci.yml)
[![Release](https://github.com/armanshirzad/fastapi-production-template/actions/workflows/release.yml/badge.svg)](https://github.com/armanshirzad/fastapi-production-template/actions/workflows/release.yml)
[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ghcr.io%2Farmanshirzad%2Ffastapi--production--template-blue.svg)](https://github.com/armanshirzad/fastapi-production-template/pkgs/container/fastapi-production-template)

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

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/armanshirzad/fastapi-production-template)

1. Fork this repository
2. Connect your GitHub account to Render
3. Click "Deploy to Render" button above
4. Configure environment variables
5. Deploy!

### Deploy to Koyeb

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=docker&image=ghcr.io/armanshirzad/fastapi-production-template:latest)

1. Fork this repository
2. Create account at [Koyeb](https://app.koyeb.com)
3. Click "Deploy to Koyeb" button above
4. Configure environment variables
5. Deploy!

## CI/CD Overview

- **Workflow files:** `.github/workflows/ci.yml` runs lint and tests; `.github/workflows/release.yml` builds the Docker image and pushes to GHCR on tag pushes (guarded to run only on this repository, not forks).
- **Registry:** pushes to `ghcr.io/armanshirzad/fastapi-production-template`.
- **Branch strategy:** run CI on `main` and `develop`, require tags `v*` for releases.
- **Publishing guard:** image publishing only runs on this repository owner (`github.repository_owner == 'ArmanShirzad'`) so forks don't attempt to push.

## Quick Start

```bash
# Clone and setup (replace with your repo URL)
git clone https://github.com/armanshirzad/fastapi-production-template.git
cd fastapi-production-template
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

The template runs out of the box with no secrets. You can optionally add these for production:

- **`SECRET_KEY`** — Secret used by the application for signing and security. If not provided, a random key is generated at startup in development/test.
- **`DATABASE_URL`** — PostgreSQL connection string. When set, the app uses PostgreSQL; when unset, the app runs without a database and the readiness endpoint will report "not configured" for the database.
- **`SENTRY_DSN`** — When set, Sentry SDK is initialized in the application for error reporting; when empty, Sentry is skipped.

Notes:

- **Workflows do not require any secrets.** CI always runs on pushes and pull requests. The release workflow uses the built‑in `GITHUB_TOKEN` and only pushes images from this repository (guarded by repository owner check). Forks will automatically skip the publishing step.

## Database Options

### Without Database (Minimal)
Leave `DATABASE_URL` empty in `.env` for a minimal API without database dependencies. The app will operate without persistence; `/health/ready` will still return 200 with `database: "not configured"`.

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
- Automatic error tracking when `SENTRY_DSN` is provided
- Performance monitoring
- Skipped automatically when `SENTRY_DSN` is empty

### Health Checks
- `/health` - Basic health check
- `/health/ready` - Readiness check; reports database status and succeeds whether the database is configured or not

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
- **Code Analysis**: CodeQL security scanning
- **Safe Defaults**: App runs without secrets by default; production deployments should set `SECRET_KEY` and configure `CORS_ORIGINS` explicitly.

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
