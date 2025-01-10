# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "loguru~=0.7.0",
#     "python-dotenv~=1.0.0",
#     "requests~=2.32.0"
# ]
# ///
# TODO: This file needs more work to be done.
import os
from getpass import getpass

import requests
from _helpers import SUPERUSER_URL
from dotenv import load_dotenv
from loguru import logger
from requests.exceptions import RequestException

# Constants
CONTENT_TYPE = "application/json"

if __name__ == "__main__":
    try:
        load_dotenv()
        secret_key = os.getenv("SECRET_KEY")
        if not secret_key:
            raise OSError("SECRET_KEY not found in environment variables.")

        logger.info("Superuser Creation")
        superuser_username = input("Superuser Username: ")
        superuser_password = getpass("Superuser Password: ")

        # Data payload for the superuser creation API.
        new_superuser_data = {
            "username": superuser_username,
            "full_name": superuser_username,
            "password": superuser_password,
            "is_superuser": True,
        }

        try:
            # Prepare headers with authorization and content type and send the request.
            headers = {
                "Content-Type": CONTENT_TYPE,
                "Authorization-Username": "SECRET_KEY",
                "Authorization-Password": f"{secret_key}",
            }
            logger.info(f"Sending POST request to {SUPERUSER_URL} with data: {new_superuser_data}")
            response = requests.post(SUPERUSER_URL, json=new_superuser_data, headers=headers)
            response.raise_for_status()
            logger.success(f"Superuser created successfully! Response: {response.json()}")
        except RequestException as e:
            # Handle and log HTTP-related exceptions.
            error_message = str(e)
            response_text = getattr(e.response, "text", "No response received.")
            logger.error(f"Failed to create superuser. Error: {error_message}, Response: {response_text}")

    except Exception as e:
        # Log any unexpected exceptions.
        logger.error(f"An unexpected error occurred: {e}")
