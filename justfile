### SETTINGS ###

## Shell Configuration
# Uncomment your preferred shell, otherwise default will be used.
#set shell := ['powershell', "-c"]
#set shell := ["sh", "-c"]
#set shell := ["bash", "-c"]
#set shell := ["nu", "-c"]

## Environment settings
set dotenv-required := true
set dotenv-load := true

## Python interpreter
# Default paths to use python in justfile. Adjust for your OS to use a custom Python interpreter.
BASE_PY_WINDOWS := 'python.exe'
BASE_PY_UNIX := '/usr/bin/env python3'
# Determine the Python path dynamically based on the operating system.
base_py_path := if os_family() == "windows" { BASE_PY_WINDOWS } else { BASE_PY_UNIX }

## Constants
postgres_continer_name := 'my-postgres'
postgres_user := env_var('POSTGRES_USER')
postgres_password := env_var('POSTGRES_PASSWORD')
postgres_db := env_var('POSTGRES_DB')

### RECEPIES ###

# Default task: Allows you to interactively choose from available tasks when no task is specified.
[private]
default:
    @just --list
    @echo ""
    @just --choose

# Generate requirements.txt from pyproject.toml
[group('uv')]
uv-create-req:
    uv lock
    uv pip compile pyproject.toml -o requirements.txt

# Tailwind CSS watch task - watches the `input.css` file for changes and continuously updates `styles.css`.
[group('tailwind')]
tailwind-watch:
    npx tailwindcss -i ./app/static/css/input.css -o ./app/static/css/styles.css --watch

# Installs Tailwind CSS as a development dependency and initializes its configuration file.
[group('tailwind')]
tailwind-install:
    npm install -D tailwindcss
    npx tailwindcss init

# Creates and starts a Docker container for PostgreSQL with default credentials and a database.
[group('docker')]
docker-run-postgres:
    docker run --name {{ postgres_continer_name }} -e POSTGRES_USER={{ postgres_user }} -e POSTGRES_PASSWORD={{ postgres_password }} -e POSTGRES_DB={{ postgres_db }} -p 5432:5432 -d postgres

[group('docker')]
docker-start-postgres:
    docker start {{ postgres_continer_name }}

# Stops and removes the running PostgreSQL Docker container after confirmation.
[group('docker')]
[confirm('Do you want to stop and remove "my-postgres"? (y/n):')]
docker-remove-postgres:
    docker stop {{ postgres_continer_name }}
    docker rm {{ postgres_continer_name }}

# Alembic migration and database upgrade.
[group('python')]
alembic-up:
    #!{{ base_py_path }}
    import subprocess

    migration_message = input("Enter migration message:\n").strip()
    if not migration_message:
        print("Migration message cannot be empty. Aborting.")
        exit(1)

    revision_result = subprocess.run(f"alembic revision --autogenerate -m '{migration_message}'", shell=True)
    if revision_result.returncode != 0:
        print("Failed to create migration. Aborting.")
        exit(1)

    if input("Proceed with upgrade? (y/n):\n").lower() == "y":
        subprocess.run("alembic upgrade head", shell=True)
        print("Database upgraded successfully.")
    else:
        print("Upgrade aborted.")

# Test the `justfile` by running a series of test.
[group('test')]
test-justfile:
    @echo "Starting all tests..."
    @just test-python
    @just test-shell
    @echo "All tests completed."

# Private task: Test the `justfile` with a Python script.
[private]
[group('test')]
test-python:
    #!{{ base_py_path }}
    print("Hello world from Python!")

# Private task: Test the `justfile` with a shell script.
[private]
[group('test')]
test-shell:
    @echo "Hello world from shell!"
