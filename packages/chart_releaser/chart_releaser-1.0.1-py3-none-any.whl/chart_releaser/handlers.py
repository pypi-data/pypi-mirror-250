"""Handlers unit."""
from chart_releaser.cli import (
    BasicArgs, HelmLintArgs,
    HelmReleaseStageArgs, HelmReleaseArgs,
    HelmCheckVersionArgs
)
from chart_releaser.logger import Logging
from chart_releaser.gitlab_api import GitlabApi
from dataclasses import dataclass
from pathlib import Path
import subprocess
import os
import sys
import yaml
import requests
from subprocess import run

@dataclass
class Helper:
    """Helper class."""

    cmd_args: BasicArgs
    logger: Logging
    token_type: str

    def get_chart_version(self, is_stage=True):
        """Get chart version.

        Return chart version any way except release args.
        If this is release return non-zero exit code.
        """
        self.logger.info("Get %s chart version...", self.cmd_args.chart_name)
        with open(f"{self.cmd_args.chart_path}/Chart.yaml", 'r', encoding="utf8") as chart_file:
            chart_version = yaml.safe_load(chart_file)
            chart_version = chart_version["version"]
        self.logger.info("Chart %s current version: %s", self.cmd_args.chart_name, chart_version)
        packages_data = GitlabApi.send_request(self, "GET", chart_version, self.token_type)
        try:
            previous_chart_version = packages_data[-1]["version"]
            if previous_chart_version == chart_version and is_stage is False:
                self.logger.error(
                    "Local chart version: %s equal repository chart version: %s. "
                    "This is not allowed for stable channel.",
                    chart_version, previous_chart_version
                )
                sys.exit(1)
            self.logger.info(
                "Chart %s repository version: %s",
                self.cmd_args.chart_name,
                previous_chart_version
            )
        except (IndexError, KeyError):
            self.logger.warning("Packages in package registry is empty...")
        return chart_version

@dataclass
class HelmLintHandler:
    """Helm lint handler class."""

    cmd_args: HelmLintArgs
    logger: Logging

    def handler(self):
        """Run handler linting args."""
        charts_dir = []
        for file_path in Path(self.cmd_args.chart_path).rglob("Chart.yaml"):
            chart_dir = str(file_path).replace("Chart.yaml", "")
            if os.path.isdir(chart_dir):
                charts_dir.append(chart_dir)
        for chart_dir in charts_dir:
            try:
                self.logger.info("Run linting for chart %s...", chart_dir)
                if self.cmd_args.debug:
                    run( [ "helm", "lint", chart_dir, "--debug" ], check=True)
                else:
                    run( [ "helm", "lint", chart_dir ], check=True)
            except subprocess.CalledProcessError as err:
                self.logger.error("Helm lint failed with error: %s", err)
                sys.exit(1)

class HelmReleaseStageHandler(Helper):
    """Helm release_stage handler."""

    cmd_args: HelmReleaseStageArgs
    logger: Logging

    def handler(self):
        """Run handler helm release_stage args."""
        try:
            self.logger.info("Create helm package...")
            run ( ["helm", "package", self.cmd_args.chart_path ], check=True)
            chart_version = self.get_chart_version(self.token_type)
            GitlabApi.send_request(self, "POST", chart_version, self.token_type, is_stage=True)
            self.logger.info(
                "Upload %s-%s.tgz to https://%s.",
                self.cmd_args.chart_name,
                chart_version,
                self.cmd_args.registry_url
            )
        except (subprocess.CalledProcessError, requests.exceptions.RequestException) as err:
            self.logger.error("Make helm release stage failed with error: %s", err)
            sys.exit(1)

class HelmReleaseHandler(Helper):
    """Helm release handler class."""

    cmd_args: HelmReleaseArgs
    logger: Logging

    def handler(self):
        """Helm release handler."""
        try:
            self.logger.info("Create helm package...")
            run ( ["helm", "package", self.cmd_args.chart_path ], check=True)
            chart_version = self.get_chart_version(is_stage=False)
            GitlabApi.send_request(self, "POST", chart_version, self.token_type)
            self.logger.info(
                "Upload %s-%s.tgz to https://%s.",
                self.cmd_args.chart_name,
                chart_version,
                self.cmd_args.registry_url
            )
        except (subprocess.CalledProcessError, requests.exceptions.RequestException) as err:
            self.logger.error("Make helm release stage failed with error: %s", err)
            sys.exit(1)

class HelmCheckVersionHandler(Helper):
    """Helm check version handler class."""

    cmd_args: HelmCheckVersionArgs
    logger: Logging

    def handler(self):
        """Helm check args handler."""
        chart_version = self.get_chart_version()
        packages_data = GitlabApi.send_request(self, "GET", chart_version, self.token_type)
        for _, package in enumerate(packages_data):
            if package["name"] == self.cmd_args.chart_name and chart_version == package["version"]:
                self.logger.error("You must increase Chart version.")
                sys.exit(1)
        self.logger.info("Check was success.")


@dataclass
class HandlerFactory:
    """Class make handler fabric."""

    @staticmethod
    def create_handler(cmd_args, logger, token_type):
        """Create an object of the class depending on the class of arguments."""
        if isinstance(cmd_args, HelmLintArgs):
            return HelmLintHandler(cmd_args, logger)
        elif isinstance(cmd_args, HelmReleaseStageArgs):
            return HelmReleaseStageHandler(cmd_args, logger, token_type)
        elif isinstance(cmd_args, HelmReleaseArgs):
            return HelmReleaseHandler(cmd_args, logger, token_type)
        elif isinstance(cmd_args, HelmCheckVersionArgs):
            return HelmCheckVersionHandler(cmd_args, logger, token_type)
