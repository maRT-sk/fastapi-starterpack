from invoke import Context  # type: ignore[attr-defined]
from invoke import task  # type: ignore[attr-defined]

from _tasks import is_pty
from _tasks import task_logger


@task
def generate_req(c: Context) -> None:
    """Generates requirements.txt from pyproject.toml."""
    c.run("uv lock", pty=is_pty)
    c.run("uv pip compile pyproject.toml -o requirements.txt", pty=is_pty)
    task_logger.info("requirements.txt generated successfully.")


@task
def createsuperuser(c: Context) -> None:
    """Creates a new superuser via the API."""
    # TODO: Implement proper security mechanisms for this endpoint.
    import json
    from http import client

    task_logger.info("Starting admin user creation process...")
    username = input("Enter admin username: ").strip()
    if not username:
        task_logger.error("Username cannot be empty. Aborting.")
        raise SystemExit(1)

    password = input("Enter admin password: ").strip()
    if not password:
        task_logger.error("Password cannot be empty. Aborting.")
        raise SystemExit(1)

    payload = {
        "username": username,
        "full_name": username,
        "is_active": True,
        "is_superuser": True,
        "password": password,
    }

    conn = client.HTTPConnection("127.0.0.1", 8000)
    headers = {"Content-Type": "application/json"}

    try:
        conn.request("POST", "/api/v1/users", body=json.dumps(payload), headers=headers)
        response = conn.getresponse()
        data = response.read().decode()

        if response.status == 201:  # noqa: PLR2004
            print("User created successfully:", json.loads(data))
        else:
            print(f"Error {response.status}: {json.loads(data)}")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        conn.close()
