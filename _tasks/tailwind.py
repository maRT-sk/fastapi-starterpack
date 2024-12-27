import shutil
from pathlib import Path

from invoke import Context  # type: ignore[attr-defined]  # type: ignore[attr-defined]
from invoke import task  # type: ignore[attr-defined]  # type: ignore[attr-defined]

from _tasks import is_pty
from _tasks import task_logger


@task
def check_node_tools(c: Context) -> None:
    """Verifies the availability of Node.js tools (npm and npx)."""
    if not shutil.which("npm"):
        task_logger.error("Preflight check: npm is not installed or not in PATH. Install Node.js and npm first.")
        raise SystemExit(1)

    if not shutil.which("npx"):
        task_logger.error("Preflight check: npx is not installed or not in PATH. Install Node.js and npm first.")
        raise SystemExit(1)


@task(pre=[check_node_tools])
def tw_install(c: Context) -> None:
    """Installs Tailwind CSS as a dependency and initializes its configuration file."""
    # Proceed with Tailwind installation
    c.run("npm install -D tailwindcss", pty=is_pty)
    task_logger.info("Tailwind CSS installed successfully.")
    c.run("npx tailwindcss init", pty=is_pty)
    task_logger.info("Tailwind CSS configuration initialized successfully.")


@task(pre=[check_node_tools])
def tw_watch(
    c: Context, _input: str = "./app/static/css/input.css", _output: str = "./app/static/css/styles.css"
) -> None:
    """Watches the input CSS file and project files for changes and updates the output CSS file."""
    if not Path(_input).exists():
        task_logger.error(f"Input file '{_input}' does not exist. ")
        raise SystemExit(1)
    task_logger.info(f"Watching '{_input}' and project files for changes and writing output to '{_output}'.")
    c.run(f"npx tailwindcss -i {_input} -o {_output} --watch", pty=is_pty)
