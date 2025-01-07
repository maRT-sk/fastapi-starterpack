from datetime import datetime

from fastapi.templating import Jinja2Templates

from app.core.utils.toml_utils import get_version_from_pyproject


class TemplateManager:
    """Manages a Jinja2 template environment for the application."""

    def __init__(self, template_dir: str = "app/templates") -> None:
        """Initialize the TemplateManager with the specified template directory."""
        self.templates = Jinja2Templates(directory=template_dir)
        self._register_globals()
        self._register_filters()

    def _register_globals(self) -> None:
        """Register global functions and variables to be used in Jinja2 templates."""
        self.templates.env.globals["static"] = self.static
        self.templates.env.globals["get_version"] = self.get_version

    def _register_filters(self) -> None:
        """Register custom Jinja2 filters."""
        self.templates.env.filters["days_ago"] = self.days_ago

    @staticmethod
    def static(path: str) -> str:
        # TODO: Custom logic for getting static files will be introduced later.
        return path

    @staticmethod
    def get_version(prefix: str = "") -> str:
        """Return a dynamic version string with an optional prefix."""
        version = get_version_from_pyproject()
        return f"{prefix}{version}"

    @staticmethod
    def days_ago(value: datetime) -> str:
        """Custom filter to display how many days ago a given datetime occurred."""
        if not isinstance(value, datetime):
            return str(value)  # Return as-is if not a datetime object

        now = datetime.now()
        delta = now - value
        if delta.days == 0:
            return "Today"
        elif delta.days == 1:
            return "Yesterday"
        else:
            return f"{delta.days} days ago"


# Instantiate the TemplateManager and expose it for application-wide use
template_manager = TemplateManager()
main_templates = template_manager.templates
