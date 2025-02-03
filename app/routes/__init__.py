import importlib
import pkgutil
from pathlib import Path

from fastapi import APIRouter
from fastapi.routing import APIRoute

from app.core import main_logger


class RouterManager:
    """
    Manages the discovery and inclusion of FastAPI routers into a single, centralized APIRouter.
    """

    def __init__(self, package_name: str, package_path: Path):
        """Initializes the RouterManager with information about the module/package."""
        self.package_name = package_name
        self.package_path = package_path
        self.main_router = APIRouter()  # The main router that will hold all included routers.

    def _include_router_from_module(self, module_full_name: str, base_prefix: str) -> None:
        """Includes a router from a given module if it exists."""
        try:
            module = importlib.import_module(module_full_name)
        except ImportError as e:
            main_logger.critical(f"Failed to import module {module_full_name}: {e}")
            raise e

        router = getattr(module, "router", None)
        if isinstance(router, APIRouter):
            self.main_router.include_router(router, prefix=base_prefix.rstrip("/"))
        else:
            main_logger.warning(f"No valid APIRouter found in module {module_full_name}.")

    def _discover_routers(self, _package_name: str, _package_path: Path, base_prefix: str = "") -> None:
        """
        Recursively discovers all modules and sub-packages in the provided package path
        and attempts to include any defined routers into the main router.
        """
        if not _package_path.exists():
            main_logger.error(f"Package path {_package_path} does not exist.")
            return

        for module_info in pkgutil.iter_modules([str(_package_path)]):
            module_name = module_info.name
            module_full_name = f"{_package_name}.{module_name}"
            module_path = _package_path / module_name

            if module_info.ispkg:
                # If it's a package, recursively discover routers in the package
                self._discover_routers(module_full_name, module_path, f"{base_prefix}/{module_name}")
            else:
                # If it's a module, attempt to include its router
                self._include_router_from_module(module_full_name, base_prefix)

    def log_registered_endpoints(self) -> None:
        """Logs all registered endpoints in the main APIRouter by grouping them by path."""
        grouped_endpoints: dict[str, set[str]] = {}

        for route in self.main_router.routes:  # Iterate over registered routes in the main router
            if isinstance(route, APIRoute):
                path = route.path
                methods = route.methods

                # # Group routes by path
                if path in grouped_endpoints:
                    grouped_endpoints[path].update(methods)  # Update methods for the path
                else:
                    grouped_endpoints[path] = set(methods)  # Create new set for the path

        # Log each path and its associated HTTP methods
        for path, methods in grouped_endpoints.items():
            main_logger.info(f"Registered endpoint: {path} {sorted(methods)}")
        main_logger.info("Routers have been successfully registered.")

    def create_router(self) -> APIRouter:
        """Discovers routers in the package and returns the main APIRouter."""
        self._discover_routers(self.package_name, self.package_path)
        self.log_registered_endpoints()
        return self.main_router


# Initialize the main router by specifying the package name and path that holds the routers
package_name_main_router = __name__  # Name of the current package
package_path_main_router = Path(__file__).parent  # Path of the current file's directory
router_manager = RouterManager(package_name_main_router, package_path_main_router)
main_router = router_manager.create_router()  # Generate the main application router with all discovered sub-routers
