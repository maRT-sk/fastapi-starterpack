# Alembic Versions Directory

This directory contains migration scripts for managing database schema changes using **Alembic**.
Each file in this directory corresponds to a specific migration, tracking changes made to the database schema over time.

## Usage

To generate a new migration script, use the following command:

```bash
alembic revision --autogenerate -m "Description of the migration"
```

To apply migrations and upgrade the database to the latest version, run:

```bash
alembic upgrade head
```

To downgrade to a previous version, use:

```bash
alembic downgrade <revision_identifier>
```

### Notes

- Ensure your database models are up to date before generating migrations to accurately reflect schema changes.
- The migrations are automatically stored in this directory and can be reviewed or edited as needed.

## Alembic using the taskipy tasks

For a more streamlined process, you can perform migrations and database upgrades using the provided scripts.
To apply all migrations and upgrade the database, run:

```bash
task alembic-up
```

> [!WARNING]
> This should work, but it requires further testing. A different approach may be considered in the future if necessary.

---

More details and enhancements to this README will be added in the future.
