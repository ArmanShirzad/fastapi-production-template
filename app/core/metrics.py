from prometheus_fastapi_instrumentator import Instrumentator


def setup_metrics(app):
    """Setup Prometheus metrics for the FastAPI application."""
    instrumentator = Instrumentator()
    instrumentator.instrument(app).expose(app)
