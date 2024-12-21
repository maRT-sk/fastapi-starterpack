# FastAPI StarterPack

An all-in-one blueprint and starter kit for building full-stack web applications with FastAPI.


> [!WARNING]
> This project is in its early development stage.

Your feedback and contributions are highly valued! A contributing guide will be available soon.

## Overview

**FastAPI StarterPack** is a foundation for building async full-stack web applications.
Engineered to simplify development, it offers a robust and organized starting point for your projects, which can be
tailored to specific needs.

### Technology Stack

- **FastAPI/Starlette**: High-performance asynchronous web framework.
- **Jinja2**: Server-side templating engine.
- **Tailwind CSS**: Utility-first CSS framework for modern UI design.
- **Alpine.js**: JavaScript framework for composing behavior directly in your markup.
- **HTMX.js**:  JavaScript framework that simplifies AJAX and dynamic content updates.
- **PostgreSQL**: Reliable relational database, integrated with **SQLModel**.
- **Alembic**: Database migration management.
- **UV**: An extremely fast Python package and project manager.
- **MyPy and Ruff**: Ensures static type checking, linting, and code formatting.

## Prerequisites

Ensure the following are installed:

- **Python >=3.12**
- **[uv >=0.5.9](https://docs.astral.sh/uv/getting-started/installation/)**: Package and project manager.

## Getting Started

### Clone the Repository

Clone the project to your local machine:

```bash
git clone https://github.com/maRT-sk/fastapi-starterpack.git
cd fastapi-starterpack
```

### Install Dependencies

Synchronize and install the required dependencies:

```bash
uv sync
```

### Start the Application

1. Create a .env file in the project root directory. Use .env.template as a reference for required variables.

2. Start the development server:
    ```bash
    uv run uvicorn app.main:app --reload --port 8000
    ```

The server will run on port 8000 with hot-reload enabled for real-time updates.

### Database Setup

Manage the database using Invoke tasks or equivalent manual commands.

1. Create and start a Docker container for PostgreSQL:

    ```
    uvx invoke db-create
    ```

2. Apply migrations:

    ```
    uvx invoke alembic-up
    ```

3. Enter a migration message when prompted. For the first migration, use a message like "initial".
   A Python migration file will be created in the `alembic/versions` folder.
4. Review the migration file to ensure it reflects the expected database schema.
   Once satisfied, return to the terminal and confirm by typing "y" to proceed with the database upgrade.

## Project Structure

> [!NOTE]
> The structure is a work in progress and may evolve as the project develops.

```
.
├── app/
│   ├── main.py               # Application initialization and configuration
│   ├── core/                 # Core backend functionality
│   │   ├── config.py         # Configuration settings
│   │   ├── database.py       # Database connection and ORM setup
│   │   ├── handler.py        # Exception handlers
│   │   ├── lifespan.py       # Application lifecycle management
│   │   ├── logger.py         # Loguru logger configuration
│   │   ├── middleware.py     # Custom middleware
│   │   └── templates.py      # Jinja2 template environment
│   ├── models/               # Database models (SQLModel)
│   ├── routes/               # API endpoints and application routes
│   ├── services/             # Business logic encapsulation
│   ├── static/               # Static assets (CSS, JavaScript, images)
│   └── templates/            # HTML templates (Jinja2)
├── alembic/                  # Database migration scripts
├── pyproject.toml            # Python project configuration
├── tasks.py                  # Task automation and project management
├── .pre-commit-config.yaml   # Pre-commit hooks configuration
└── .env                      # Local development configuration
```

## Development Tools

### Tasks

To view the full list of available tasks, run the following command:

```bash
uvx invoke --list
```

Below is a list of the currently available tasks for project management and automation:

- **`alembic-up`**
  Creates an Alembic migration with a user-specified message and upgrades the database.

- **`db-create`**
  Creates and starts a Docker container for PostgreSQL with default credentials from .env file.

- **`db-remove`**
  Stops and removes the running PostgreSQL Docker container after confirmation.

- **`db-start`**
  Starts an existing PostgreSQL Docker container.

- **`generate-req`**
  Generates a `requirements.txt` file from `pyproject.toml`.

- **`tw-install`**
  Installs Tailwind CSS as a dependency and initializes its configuration file.

- **`tw-watch`**
  Watches the input CSS file and project files for changes and updates the output CSS file.

- **`check-docker`**
  Checks if Docker CLI is installed and Docker Desktop is running.

- **`check-node-tools`**
  Verifies that Node.js tools (`npm` and `npx`) are installed and available in the system PATH.

#### Usage Example

To run a task, use the following command:

```
uvx invoke <task-name>
```

For example, to create a PostgreSQL container:

```
uvx invoke db-create
```

> [!TIP]
> Refer to `tasks.py` for detailed implementation.

### Linting and Formatting

Run linting checks:

```
uv run ruff check .
```

Fix linting issues automatically:

```
uv run ruff check . --fix
```

Format the code:

```
uv run ruff format
```

### Type Checking

Type-check the code with mypy:

```
uv run mypy .
```

### Pre-commit Hooks

Execute all pre-commit hooks:

```
uv run pre-commit run --all-files
```

## Roadmap

### Backend Improvements

- **Integrate S3 Object Storage**: Use boto3 for efficient static file management.
- **Admin Interface**: Add SQLAdmin for database management.
- **Implement Additional Endpoints**: Add more API endpoints to showcase functionality.
- **Enhance Security**: Integrate authentication, authorization, and rate limiting.
- **Caching**: Demonstrate caching strategies for performance optimization.

### Frontend Enhancements

- **Interactive Components**: Use Alpine.js and HTMX.js to create more examples.
- **Form Validation Examples**: Provide examples of form validation and error handling.

### Development & Deployment

- **Set Up CI/CD Pipeline**: Configure GitHub Actions for automated deployments and code quality checking.
- **Production Configurations**: Add deployment-ready configurations.
- **Project-Specific Commands**: Refine and extend project-specific task runners.

### Documentation

- **Enhance the Documentation**: Comprehensive installation, setup, and usage documentation.
- **Examples and Tutorials**: Include practical examples and tutorials.

---

Stay tuned for updates! Your feedback and contributions are highly appreciated. 🙌
