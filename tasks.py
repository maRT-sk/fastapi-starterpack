# TODO: Evaluate the possibility of using a different task runner
from _tasks.alembic import alembic_up
from _tasks.db_postgres import db_create
from _tasks.db_postgres import db_remove
from _tasks.db_postgres import db_start
from _tasks.generic import createsuperuser
from _tasks.generic import generate_req
from _tasks.tailwind import check_node_tools
from _tasks.tailwind import tw_install
from _tasks.tailwind import tw_watch

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
