from azure.storage.queue import QueueServiceClient
from azure.identity import ClientSecretCredential
import requests
from typing import List
import json
from html.parser import HTMLParser  # web scraping html
import subprocess
import os

from cdh_dav_python.cdc_admin_service import (
    environment_tracing as cdc_env_tracing,
    environment_logging as cdc_env_logging,
)

from cdh_dav_python.cdc_tech_environment_service import environment_file as cdc_env_file

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class GitHubRelease:
    # Get the currently running file name
    NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
    # Get the parent folder name of the running file
    SERVICE_NAME = os.path.basename(__file__)

    @staticmethod
    def get_releases(gh_access_token, gh_owner_name, gh_repository_name):
        """
        Retrieves the releases of a GitHub repository.

        Args:
            gh_access_token (str): The access token for authenticating the GitHub API requests.
            gh_owner_name (str): The name of the owner of the GitHub repository.
            gh_repository_name (str): The name of the GitHub repository.

        Returns:
            tuple: A tuple containing the HTTP status code, response content, and API URL.
                - HTTP status code (int): The status code of the API response.
                - response content (dict): The JSON content of the API response.
                - API URL (str): The URL used to make the API request.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
            json.JSONDecodeError: If the response content cannot be decoded as JSON.
        """

        logger_singleton = cdc_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        logger = logger_singleton.get_logger()
        cdc_env_tracing.TracerSingleton.log_to_console = False
        tracer_singleton = cdc_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME
        )
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_releases"):
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"Bearer {gh_access_token}",
            }

            api_url = f"https://api.github.com/repos/{gh_owner_name}/{gh_repository_name}/releases"

            logger.info(f"api_url:{str(api_url)}")

            try:
                response = requests.get(api_url, headers=headers)
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {e}")
                return 500, f"Request failed: {e}", api_url

            # Convert the response text to JSON
            try:
                response_content = response.json()
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON: {e}")
                return response.status_code, f"Failed to decode JSON: {e}", api_url

            # Log the response content
            logger.info(f"response_content: {response_content}")

            return response.status_code, response_content, api_url
