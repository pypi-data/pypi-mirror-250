"""Unit for CLI."""
from dataclasses import dataclass
from importlib.metadata import version
import argparse
import os

@dataclass
class BasicArgs:
    """Basis class.

    This class has all CLI arguments, except HelmLintArgs.
    """

    token: str
    ssl_path: str
    registry_url: str
    project_id: str
    chart_name: str
    chart_path: str
    tool_config_path: str

@dataclass
class HelmLintArgs:
    """Class for helm linting cmd args."""

    command: str
    helm_args: str
    debug: str
    chart_path: str

@dataclass
class HelmReleaseArgs(BasicArgs):
    """Class for helm release cmd args."""

    command: str
    helm_args: str

@dataclass
class HelmReleaseStageArgs(BasicArgs):
    """Class for helm release_stage cmd args."""

    command: str
    helm_args: str
    branch: str

@dataclass
class HelmCheckVersionArgs(BasicArgs):
    """Class for helm check cmd args."""

    command: str
    helm_args: str


def create_common_arguments_group(parser):
    """Create common CLI arguments."""
    common_args = parser.add_argument_group('Common arguments')
    common_args.add_argument(
        "-t", "--token",
        required=False,
        default=os.environ.get("CHART_RELEASE_TOKEN", ""),
        help="Registry upload token",
        dest="token"
    )
    common_args.add_argument(
        "--ssl",
        required=False,
        default=os.environ.get("SSL_PATH", "/usr/local/share/ca-certificates/CA.crt"),
        help="Path to SSL certificate",
        dest="ssl_path"
    )
    common_args.add_argument(
        "-u", "--registry-url",
        dest="registry_url",
        required=False,
        default=os.environ.get("REGISTRY_URL", "gitlab.com"),
        help="Registry URL"
    )
    common_args.add_argument(
        "-p", "--project-id",
        required=False,
        default=os.environ.get("RELEASE_PROJECT_ID", ""),
        dest="project_id",
        help="Actual if usage gitlab registry"
    )
    common_args.add_argument(
        "-n", "--chart_name",
        required=True,
        dest="chart_name",
        help="Chart name."
    )
    common_args.add_argument(
        "-path", "--path",
        required=True,
        dest="chart_path",
        help="Chart path"
    )
    common_args.add_argument(
        "-c", "--config",
        required=False,
        default=os.environ.get("TOOL_CONFIG_PATH", "hc-releaser.config"),
        dest="tool_config_path",
        help="Path to tool config file."
    )

def create_switch_args_fabric(class_type, args):
    """Arguments fabric.

    Returns the passed class object.
    """
    if class_type == HelmLintArgs:
        return class_type(
            command=args.command,
            helm_args=args.helm_args,
            debug=args.debug,
            chart_path=args.chart_path
        )
    else:
        return class_type(
            command=args.command,
            helm_args=args.helm_args,
            token=args.token,
            ssl_path=args.ssl_path,
            registry_url=args.registry_url,
            project_id=args.project_id,
            chart_path=args.chart_path,
            chart_name=args.chart_name,
            tool_config_path=args.tool_config_path,
            **({'branch': args.branch} if class_type is HelmReleaseStageArgs else {})

        )

def parse_args():
    """Create CLI."""
    parser = argparse.ArgumentParser(description="Helm chart releaser.")
    parser.add_argument(
            "-v", "--version",
            action="version",
            version=f"%(prog)s {version('chart_releaser')}",
            help="Show package version"
    )
    subparsers = parser.add_subparsers(
        title="subcommands",
        description='Valid subcommands',
        dest="command"
    )
    ## Add helm parser
    helm_parser = subparsers.add_parser("helm", help="Usage 'linting|release|release_stage|check'")
    helm_subparsers = helm_parser.add_subparsers(dest='helm_args')
    ## Linting parser
    linting_parser = helm_subparsers.add_parser('linting', help='helm lint cmd')
    linting_parser.add_argument(
        "-d", "--debug",
        required=False,
        action='store_true',
        help="Helm lint with debug",
        dest="debug"
    )
    linting_parser.add_argument(
        "-p", "--path",
        required=True,
        help="Helm chart path",
        dest="chart_path"
    )
    ## Helm release parser
    helm_release_parser = helm_subparsers.add_parser(
        "release",
        help="Helm release cmd"
    )
    ## Helm release stage parser
    helm_release_stage_parser = helm_subparsers.add_parser(
        "release_stage",
        help="Helm release stage cmd"
    )
    helm_release_stage_parser.add_argument(
        "-b", "--branch",
        required=True,
        help="Git branch",
        dest="branch"
    )
    ## Helm check version parser
    helm_check_version_parser = helm_subparsers.add_parser(
        "check",
        help="Helm check version cmd"
    )
    create_common_arguments_group(helm_release_parser)
    create_common_arguments_group(helm_release_stage_parser)
    create_common_arguments_group(helm_check_version_parser)
    args = parser.parse_args()

    if args.command == "helm" and args.helm_args is not None:
        switch_classes = {
            "linting": HelmLintArgs,
            "release": HelmReleaseArgs,
            "release_stage": HelmReleaseStageArgs,
            "check": HelmCheckVersionArgs
        }
        return create_switch_args_fabric(switch_classes.get(args.helm_args), args)
    else:
        parser.print_help()
