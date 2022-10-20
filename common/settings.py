import argparse
import logging
import os
import sys
from typing import Dict

import requests


class Settings:
    util_port: int
    host_for_request: str
    base64_key: str
    get_cached_response: Dict[str, requests.Response]
    post_cached_response: Dict[str, requests.Response]

    # noinspection PyTypeChecker
    def __init__(self, args_dict):
        self.util_port = args_dict["util_port"]
        self.host_for_request = args_dict["host_for_request"]
        self.base64_key = args_dict["base64_key"]

        if self.host_for_request is None:
            logging.error("Host for request is NULL!")
            sys.exit(1)

        self.get_cached_response = {}
        self.post_cached_response = {}


def parse_console_args_and_get_settings() -> Settings:
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--util_port", type=int, default=os.environ.get("UTIL_PORT", default=9119))
    args_parser.add_argument("--host_for_request", type=str, default=os.environ.get("HOST_FOR_REQUEST"))
    args_parser.add_argument("--base64_key", type=str, default=os.environ.get("BASE64_KEY"))

    args_dict = args_parser.parse_args().__dict__

    settings = Settings(args_dict)

    return settings
