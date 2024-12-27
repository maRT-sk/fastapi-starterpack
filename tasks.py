# TODO: Evaluate the possibility of using a different task runner
from tasks_def.alembic import alembic_up
from tasks_def.db_postgres import db_create
from tasks_def.db_postgres import db_remove
from tasks_def.db_postgres import db_start
from tasks_def.generic import createsuperuser
from tasks_def.generic import generate_req
from tasks_def.tailwind import check_node_tools
from tasks_def.tailwind import tw_install
from tasks_def.tailwind import tw_watch

# Expose tasks to the task runner
__all__ = [
    "alembic_up",
    "db_create",
    "db_start",
    "db_remove",
    "tw_install",
    "tw_watch",
    "generate_req",
    "createsuperuser",
    "check_node_tools",
]
