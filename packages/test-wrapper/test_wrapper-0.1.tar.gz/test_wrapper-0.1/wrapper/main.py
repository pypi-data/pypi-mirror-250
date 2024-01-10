import argparse
import logging
import sys

import uvicorn

from wrapper.wrapper import create_wrapper
from utilities.toml import parse_runloop_toml_file

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run runloop wrapper")
    parser.add_argument("--port", type=int, default=8000, help="Bind socket to this port.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Bind socket to this host.")
    parser.add_argument("--toml_path", type=str, help="Path to runloop .toml file")
    args = parser.parse_args()

    file_path = args.toml_path
    if not file_path:
        _logger.error("provide valid path to runloop .toml file")
        sys.exit(1)

    try:
        lambda_descriptors = parse_runloop_toml_file(file_path)
        _logger.debug(f"starting wrapper, found lambda_descriptors={lambda_descriptors}")
        app = create_wrapper(lambda_descriptors)
        uvicorn.run(app, port=args.port, host=args.host)

    except Exception as e:
        print(e)
        sys.exit(1)
