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

import requests
from _helpers import BLOG_URL
from dotenv import load_dotenv
from loguru import logger
from requests.exceptions import RequestException

# Constants
CONTENT_TYPE = "application/json"

if __name__ == "__main__":
    try:
        # Retrieve SECRET_KEY from the environment variables.
        load_dotenv()
        secret_key = os.getenv("SECRET_KEY")
        if not secret_key:
            raise OSError("SECRET_KEY not found in environment variables.")

        # Construct the authorization header using the secret key.
        headers = {
            "Content-Type": CONTENT_TYPE,
            "Authorization-Username": "SECRET_KEY",
            "Authorization-Password": f"{secret_key}",
        }

        # Define the payload data for the POST request.
        post_data = {"title": "Hello World", "content": "This is the content of my first post."}

        try:
            # Make the POST request to create a new post.
            logger.info(f"Sending POST request to {BLOG_URL} with data: {post_data}")
            response = requests.post(BLOG_URL, json=post_data, headers=headers)
            response.raise_for_status()
            logger.success(f"Post created successfully! Response: {response.json()}")
        except RequestException as e:
            # Handle and log HTTP-related exceptions.
            error_message = str(e)
            response_text = getattr(e.response, "text", "No response received.")
            logger.error(f"Failed to create post. Error: {error_message}, Response: {response_text}")

    except Exception as e:
        # Log any unexpected exceptions.
        logger.error(f"An unexpected error occurred: {e}")
