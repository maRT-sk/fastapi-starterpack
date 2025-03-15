# Instantiate the TemplateManager and expose it for application-wide use
from app.core.templates.templating import TemplateManager

template_manager = TemplateManager()
renderer = template_manager.templates
