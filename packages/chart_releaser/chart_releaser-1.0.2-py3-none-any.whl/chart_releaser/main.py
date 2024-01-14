"""Main unit."""
from chart_releaser.cli import parse_args
from chart_releaser.logger import Logging
from chart_releaser.handlers import HandlerFactory
import configparser

cmd_args = parse_args()
logger = Logging("chart-releaser")
handlers = HandlerFactory()

config_parser = configparser.ConfigParser()
try:
    config_parser.read(cmd_args.tool_config_path)
    token_type = config_parser.get("main", "TOKEN_TYPE")
except (configparser.NoSectionError, AttributeError):
    token_type = "JOB-TOKEN"

def main():
    """Entry point."""
    if cmd_args is not None:
        handler = handlers.create_handler(cmd_args, logger, token_type)
        handler.handler()

if __name__ == "__main__":
    main()
