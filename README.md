# FastAPI StarterPack

An all-in-one blueprint and starter kit for building full-stack web applications with FastAPI.


> [!WARNING]
> **This project is in its early development stage.**
>
> It is not production-ready and may undergo significant changes. Use it for learning, prototyping, or as a base for
> custom projects.

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
- **SQLite or PostgreSQL**: Databases integrated with SQLAlchemy for ORM and query management.
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

> [!TIP]
> For a better development experience, you can start the application using an IDE to help with debugging code and
> templates.

### Database Setup

This project supports both **SQLite** and **PostgreSQL** as database backends.

#### Using SQLite (default):

1. Create and apply migrations:
    ```bash
    task alembic-up
    ```
2. When prompted, enter a migration message (e.g., "initial").
3. Review the generated migration file in the alembic/versions directory.
4. Confirm the upgrade by typing "Y" when prompted.

#### Using PostgreSQL:

1. Install PostgreSQL dependencies:
    ```bash
    uv sync --extra postgres
    ```

2. Create and start a PostgreSQL Docker container:
    ```bash
    task db-create
    ```

3. Create and apply migrations:
    ```bash
    task alembic-up
    ```
4. When prompted, enter a migration message (e.g., "initial").
5. Review the generated migration file in the alembic/versions directory.
6. Confirm the upgrade by typing "Y" when prompted.

## Project Structure

> [!NOTE]
> The structure is a work in progress and may evolve as the project develops.

```
.
├── app/
│   ├── main.py               # Application entry point and startup configuration
│   ├── core/                 # Core backend functionality
│   │   ├── config/           # Configuration management and settings
│   │   ├── data/             # Data structures, types, and enumerations
│   │   ├── database/         # Database layer
│   │   ├── gateway/          # Middlewares, exception handlers, and API gateway logic
│   │   ├── logging/          # Logging configuration and custom logger setup
│   │   ├── templates/        # Template rendering setup
│   │   ├── typedefs/         # Custom type definitions (enums, datatypes, exceptions)
│   │   ├── utils/            # Utility functions and helper modules
│   │   └── lifecycle/        # Application lifecycle management
│   ├── domain/               # Encapsulates domain-specific logic
│   │   └──  module_n/        # Represents a specific domain (e.g., Users, Products)
│   │       ├── model.py      # Repository pattern implementation for db operations
│   │       ├── schema.py     # Pydantic schemas for validation and serialization
│   │       ├── crud.py       # CRUD for repository design pattern
│   │       ├── enums.py      # Enumerations for structured choices
│   │       └── exeptions.py  # Handles domain-specific exceptions
│   ├── services/             # Business logic and service layer functionalities
│   ├── routes/               # API endpoints and application routes
│   ├── static/               # Static assets (CSS, JavaScript, images)
│   └── templates/            # HTML templates (Jinja2)
├── scripts/                  # Standalone automation scripts
├── alembic/                  # Database migration scripts
├── pyproject.toml            # Python project configuration
├── .pre-commit-config.yaml   # Pre-commit hooks configuration
└── .env                      # Local development configuration
```

## Development Tools

### Tasks

To view the full list of available tasks, run the following command:

```bash
task list
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

#### Usage Example

To run a task, use the following command:

```
task <task-name>
```

For example, to create a PostgreSQL container:

```
task db-create
```

### Linting and Formatting

Run the Ruff linter and formatter:

```
task ruff
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
