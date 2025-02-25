from fastapi.routing import APIRoute
from fastapi.routing import Mount
from starlette.routing import BaseRoute
from starlette.routing import Route

from app.core.logging import main_logger


def log_route_details(routes: list[BaseRoute]) -> None:
    """Logs details of a list of FastAPI routes."""
    for route in routes:
        if isinstance(route, APIRoute):
            methods = ", ".join(route.methods or [])
            main_logger.info(f"Registered API Route: {methods} {route.path}")
        elif isinstance(route, Mount):
            main_logger.info(f"Mounted Route: {route.path} (for static files)")
        elif isinstance(route, Route):
            methods = ", ".join(route.methods or [])
            main_logger.info(f"Registered Page Route: {methods} {route.path}")
