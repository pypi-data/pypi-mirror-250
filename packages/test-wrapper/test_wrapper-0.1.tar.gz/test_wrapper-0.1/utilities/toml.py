from pathlib import Path
from typing import List

import toml

from models.models import LambdaDescriptor

_LAMBDA_KEY = "lambda"


def parse_runloop_toml(toml_string: str) -> List[LambdaDescriptor]:
    """Converts a TOML string to a list of LambdaDescriptor objects.

    Args:
    ----
    toml_string (str): A TOML formatted string.

    Returns:
    -------
    List[LambdaDescriptor]: A list of LambdaDescriptor objects.
    """
    parsed_toml = toml.loads(toml_string)
    return [LambdaDescriptor(**descriptor) for descriptor in parsed_toml.get(_LAMBDA_KEY, [])]


def parse_runloop_toml_file(toml_file_path: str) -> List[LambdaDescriptor]:
    """Converts a TOML file to a list of LambdaDescriptor objects.

    Args:
    ----
    toml_file_path (str): Path to a toml formatted file

    Returns:
    -------
    List[LambdaDescriptor]: A list of LambdaDescriptor objects.
    """
    with Path(toml_file_path).open(mode="r") as f:
        return parse_runloop_toml(f.read())
