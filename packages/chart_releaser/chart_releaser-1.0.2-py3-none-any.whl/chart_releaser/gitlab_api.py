"""Unit for gitlab API."""
from dataclasses import dataclass
from chart_releaser.cli import BasicArgs
from chart_releaser.logger import Logging
import sys
import requests

@dataclass
class GitlabApi:
    """Class for work with gitlab API."""

    cmd_args: BasicArgs
    logger: Logging

    def send_request(self, request_method, chart_version, token_type, is_stage=False):
        """Send request to gitlab API."""
        packages_list = []
        if request_method == "POST":
            chart_file = {
                'chart': open(f"{self.cmd_args.chart_name}-{chart_version}.tgz", 'rb')
            }
            if is_stage is False:
                requests.post(
                    f"http://{self.cmd_args.registry_url}/api/v4/projects/{self.cmd_args.project_id}/packages/helm/api/stable/charts",
                    files=chart_file, auth=('JOB-TOKEN', self.cmd_args.token),
                    verify=self.cmd_args.ssl_path, timeout=120
                )
            else:
                requests.post(
                    f"http://{self.cmd_args.registry_url}/api/v4/projects/{self.cmd_args.project_id}/packages/helm/api/develop/charts",
                    files=chart_file, auth=('JOB-TOKEN', self.cmd_args.token),
                    verify=self.cmd_args.ssl_path, timeout=120
                )
        elif request_method == "GET":
            headers = {
                token_type : self.cmd_args.token
            }
            data = requests.get(
                f"http://{self.cmd_args.registry_url}/api/v4/projects/{self.cmd_args.project_id}/packages?package_type=helm&package_name={self.cmd_args.chart_name}",
                headers=headers,
                verify=self.cmd_args.ssl_path, timeout=120
            )
            if data.status_code == 401:
                self.logger.error("Authorization falied.")
                sys.exit(1)
            elif data.status_code == 404:
                self.logger.error(
                    "Project %s not found or you do not have permissions for project.",
                    self.cmd_args.project_id
                )
                sys.exit(1)
            elif data.status_code == 200:
                total_page_number = int(data.headers["X-Total-Pages"])
                current_page_number = int(data.headers["X-Page"])
                while current_page_number <= total_page_number:
                    response = requests.get(
                        f"http://{self.cmd_args.registry_url}/api/v4/projects/"
                        f"{self.cmd_args.project_id}/packages?package_type=helm&package_name={self.cmd_args.chart_name}",
                        params={'page': current_page_number}, headers=headers,
                        verify=self.cmd_args.ssl_path, timeout=120
                    ).json()
                    for _, item in enumerate(response):
                        packages_mapping = {
                            "name": item["name"],
                            "version": item["version"]
                        }
                        packages_list.append(packages_mapping)
                    current_page_number += 1
                return packages_list
            else:
                self.logger.error("Unexpected status code %s", data.status_code)
                sys.exit(1)
        return None
