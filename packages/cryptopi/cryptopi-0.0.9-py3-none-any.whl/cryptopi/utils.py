"""
utils.py This file contains utility functions.
"""

import os
import json

#: The environment variable for the API key.
API_KEY_ENV_VAR = "CMC_PRO_API_KEY"


def find_api_key(path: str = None, key: str = None) -> str:
    """
    Find the API key.
    :return:
    """

    # If a path is provided, load the API key from the file.
    if path is not None:
        return load_api_key_from_file(path, key=key)

    # If no path is provided, check the environment variables.
    key = os.environ.get(API_KEY_ENV_VAR)

    # If the key isn't set in the env, raise an exception.
    if key is None:
        raise Exception(f"API Key not found in env: {API_KEY_ENV_VAR}")

    return key


def load_api_key_from_file(path: str, key="api_key") -> str:
    """
    Load the API key from a file.
    :param key: The key in the json file for the API Key value.
    :param path: The path.
    :return:
    """

    # The API Key.
    with open(path, "r") as f:
        content = f.read()
        api_key = json.loads(content)[key]

    return api_key
