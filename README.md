# FastAPI StarterPack

> An all-in-one blueprint and starter kit for building full-stack web applications with FastAPI.

Currently in its very early development stage, suggestions and insights are highly encouraged!  
A contributing guide will be provided soon.

## Overview

**FastAPI StarterPack** is a foundation for building async full-stack web applications.
Engineered to simplify development while ensuring scalability, it offers a robust and organized starting
point for your projects.

### Technology Stack

- **FastAPI/Starlette**:  A modern framework for building high-performance asynchronous web services.
- **Jinja2**:  A fast and flexible templating engine for server-side rendering.
- **Tailwind CSS**: A utility-first CSS framework for responsive design.
- **Alpine.js**: A lightweight JavaScript framework for declarative UI interactions.
- **HTMX.js**:  A simple library that simplifies AJAX and dynamic content updates.
- **PostgreSQL**: A powerful and reliable relational database, integrated using **SQLModel** package.
- **Alembic**: A simple yet powerful tool for managing database migrations.
- **UV**: An extremely fast Python package and project manager.
- **MyPy and Ruff**: Ensures static type checking, linting, and code formatting.

## Prerequisites

Before getting started, ensure you have the following installed:

- **Python >=3.12**
- **[uv >=0.5.9](https://docs.astral.sh/uv/getting-started/installation/)**: An extremely fast Python package and
  project manager.
- **[just >=1.37.0](https://just.systems/man/en/packages.html)** (Optional): A handy way to save and run
  project-specific commands.
    - **fzf >=0.56.3** (Optional): Used with `just` for an interactive recipe chooser.

## How to Run

### Install Dependencies

Set up the project by installing the required dependencies (including dev dependencies) using the following command:

```bash
uv sync
```

### Start the Application

If you're using the application locally, make sure to create a `.env` file in the root directory.
You can use the `.env.template` file as a reference to properly configure your environment variables.

To start the development server, run the following command:

```bash
uv run uvicorn app.main:app --reload --port 8000
```

This command starts the application on port `8000` with hot-reload enabled,
allowing you to see code changes in real time.

## Setting Up the Database

The project uses a lightweight command runner `just`, to manage project-specific tasks. In the future, it may be
replaced. If you prefer not to use the provided Justfile, you can review its contents and run the commands manually.

Follow these steps to create, initialize, and upgrade the database:

1. Start a PostgreSQL database instance using Docker:

```
just docker-run-postgres
```

2. Apply the initial database migration and upgrade the schema:

```
just alembic-up
```

You will be prompted to enter a migration message. For the first migration, you can use a message like `initial`.
This will generate a Python migration file in your Alembic folder. Review this file to ensure it reflects the expected
database schema.
Once reviewed, return to the terminal and confirm to proceed with the database upgrade.

## Project Structure

_Note: The structure is a work in progress and may evolve as the project develops._

### Explanation of Key Folders and Files

```
.
├── app/
│   ├── main.py   # Manages the initialization and configuration of the FastAPI application
│   ├── core/     # Contains core backend functionality
│   │   ├── config.py       # Handles application configuration settings
│   │   ├── database.py     # Manages database connections and ORM setup
│   │   ├── handler.py      # Implements exception handlers
│   │   ├── lifespan.py     # Manages application startup and shutdown lifecycle
│   │   ├── logger.py       # Configure Loguru's logger
│   │   ├── middleware.py   # Defines custom middleware
│   │   └── templates.py    # Manages a Jinja2 template environment for the application
│   ├── models/     # Houses the database models, implemented using SQLModel
│   ├── routes/     # Defines API endpoints and application routes, automatically gathered
│   ├── services/   # Defines API endpoints and application routes, automatically gathered
│   ├── services/   # Encapsulates the business logic of the application
│   ├── static/     # Directory for static assets such as CSS, JavaScript, and images
│   └── templates/  # Stores HTML templates written with Jinja2, used for rendering pages
├── alembic/                  # Contains scripts and configuration for managing database migrations
├── pyproject.toml            # Configuration file for the Python project, including dependencies and build tools
├── justfile                  # Task runner file for automating common development commands
├── .pre-commit-config.yaml   # Configuration file for pre-commit hooks
└── .env                      # Contains configuration settings for local development
```

Designed to ensure modularity and maintainability, this structure simplifies scaling and managing the application.

### Running Development Tools

If development dependencies are installed, you can use the following commands to run various code quality and formatting
checks.

Run linting checks with ruff:

```
uv run ruff check .
```

Fix linting issues automatically:

```
uv run ruff check . --fix
```

Format the code using ruff:

```
uv run ruff format
```

Type-check the code with mypy:

```
uv run mypy .
```

Run all pre-commit hooks:

```
uv run pre-commit run --all-files
```

## To-Do List

There are numerous areas that need improvement. Below is a list of tasks and enhancements I aim to address in the
future. Contributions, suggestions, and ideas are always welcome to help shape this project into something even better!

### Backend Improvements

- **Integrate S3 Object Storage**: Use boto3 to manage static files efficiently.
- **Admin Interface**: Implement SQLAdmin for managing database models.
- **Implement Additional Endpoints**: Add more API endpoints to showcase functionality.
- **Enhance Security**: Integrate authentication, authorization, and rate-limiting features.
- **Add Caching**: Implement caching example for better performance.

### Frontend Enhancements

- **Add Interactive Components**: Use Alpine.js and HTMX.js to create more examples.
- **Form Validation Examples**: Provide examples of form validation and error handling.

### Development & Deployment

- **Set Up CI/CD Pipeline**: Configure GitHub Actions for automated deployments and code quality checking.
- **Production Configurations**: Add deployment configurations.
- **Project-Specific Commands**: Add new commands and refine existing ones to ensure reliability and efficiency.

### Documentation

- **Enhance the Documentation**: Add detailed instructions for installation, setup, and usage.
- **Add Examples and Tutorials**: Include practical examples and tutorials.

---

Stay tuned for updates! Thank you for your interest! 🙌
