from app.core.config import logger
from app.core.config import settings
from app.core.database import base
from app.core.database import repository
from app.core.database import session
from app.core.rendering import templates

# Expose key components for direct import from core
main_logger = logger.main_logger
AppConfig = settings.AppConfig
Base = base.Base
Repository = repository.Repository
get_session = session.get_session
main_templates = templates.main_templates

__all__ = ["main_logger", "AppConfig", "Base", "Repository", "get_session", "main_templates"]
