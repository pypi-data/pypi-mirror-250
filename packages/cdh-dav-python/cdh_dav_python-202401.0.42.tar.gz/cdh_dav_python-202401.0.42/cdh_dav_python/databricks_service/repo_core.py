""" Module for rep_core for it_cdc_admin_service that handles repository and cluster functions with minimal dependencies. """

import os
from importlib import util  # library management

from calendar import c
from html.parser import HTMLParser  # web scraping html
from datetime import date, datetime

import requests

# http
from urllib.parse import urlparse

# certs
import certifi
from pathlib import Path


# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class RepoCore:
    @staticmethod
    def get_cicd_destination_path(cdh_folder_config: str) -> str:
        """Create file path for cicd storage event trigger

        Args:
            config (dict): configuration dictionary

        Returns:
            str: cicd destination path

        """

        cicd_action_folder = cdh_folder_config.replace("config", "cicd")

        current_date_time = datetime.now().strftime("%Y_%m_%d_%I_%M_%S_%p")

        cicd_action_folder = cicd_action_folder.replace("abfss", "https")
        url = urlparse(cicd_action_folder)
        container = url.netloc.split("@")[0]
        base_address = url.netloc.split("@")[1]
        path = url.path
        destination_path = f"https://{base_address}/{container}{path}pull_request_{current_date_time}.json"

        return destination_path

    @staticmethod
    def write_issues(r, csvout):
        "output a list of issues to csv"
        if not r.status_code == 200:
            raise Exception(r.status_code)
        for issue in r.json():
            Tag = []
            labels = issue["labels"]
            for label in labels:
                Tag.append(label["name"])

            csvout.writerow(
                [
                    issue["number"],
                    issue["title"].encode("utf-8"),
                    Tag,
                    issue["state"],
                    issue["created_at"],
                    issue["closed_at"],
                ]
            )

    @classmethod
    def pull_repository_latest(
        cls,
        config: dict,
        token: str,
        base_path: str,
        repository_name: str,
        branch_name: str,
    ) -> str:
        """Pulls the lastest repository branch for the given repo

        Args:
            config (dict): global config dictionary
            token (str): security token
            base_path (str): reository base path location to pull
            repository_name (str): repository name to pull
            branch_name (str): repository branch name to pull

        Returns:
            str: result message from pull request
        """

        databricks_instance_id = config["databricks_instance_id"]
        json_text = {"path": base_path}
        headers = {"Authentication": f"Bearer {token}"}
        api_url = f"https://{databricks_instance_id}"
        url = f"{api_url}/api/2.0/workspace/list"
        verify = certifi.where()

        print(f"------- Fetch {base_path}  -------")
        print(f"url:{str(url)}")
        headers_redacted = str(headers).replace(token, "[bearer REDACTED]")
        print(f"headers:{headers_redacted}")

        response = requests.get(url=url, headers=headers, json=json_text, verify=verify)
        data = None

        try:
            data = response.json()
            response_text_fetch = (
                f"Suceess: Received list_repos with length : {len(str(data))}"
            )
            response_text_fetch = response_text_fetch + f" when posting to : {url}"
            print(f"{response_text_fetch}")
            print(f"listed files for : {base_path}")
            print(str(data))
            lst = data["objects"]
            repos = list(
                filter(
                    lambda itm: str(Path(itm["path"]).stem).upper()
                    == repository_name.upper(),
                    lst,
                )
            )

            if repos[0] is None:
                repo_data = "Error Repo Not found"
            else:
                repo_object = repos[0]
                repo_id = repo_object["object_id"]
                url = f"{api_url}/api/2.0/repos/{repo_id}"
                print(f"repo_id:{repo_id} branch_name:{branch_name}")
                repo_data = requests.patch(
                    url=url,
                    headers=headers,
                    verify=verify,
                    json={"branch": branch_name},
                ).json()
        except Exception as exception_object:
            filter_object = HTMLFilter()
            filter_object.feed(response.text)
            response_text = filter_object.text
            repo_data = f"Response : error - {exception_object}: {response_text}"

        print(repo_data)

        return repo_data


class HTMLFilter(HTMLParser):
    text = ""

    def handle_data(self, data):
        self.text += data


class CDHObject(object):
    pass
