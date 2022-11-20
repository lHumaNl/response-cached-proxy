import json
import logging
import os
import sys
from typing import Dict, Any, List

import requests

from models.param_names import ParamNames


class Settings:
    util_port: int
    host_for_request: str
    timeout: int
    base64_keys: List[str]
    append_parameter: Dict[str, str]
    strings_for_replace: Dict[str, Dict[str, str]]
    get_cached_response: Dict[str, requests.Response]
    post_cached_response: Dict[str, requests.Response]

    # noinspection PyTypeChecker
    def __init__(self, args_dict):
        config_file_name = self.__get_value_from_dict(args_dict, ParamNames.CONFIG_FILE)
        config_dict: Dict = self.decode_json_file(os.path.join("config", config_file_name))

        self.util_port = self.__get_value_from_dict(args_dict, ParamNames.UTIL_PORT)
        self.host_for_request = self.__get_value_from_dict(config_dict, ParamNames.LINK)
        self.timeout = self.__get_value_from_dict(config_dict, ParamNames.TIMEOUT, True, 10)
        self.base64_keys = self.__get_value_from_dict(config_dict, ParamNames.BASE64_KEYS, True)
        self.append_parameter = self.__get_value_from_dict(config_dict, ParamNames.APPEND_PARAM, True)
        self.strings_for_replace = self.__get_value_from_dict(config_dict, ParamNames.STRINGS_FOR_REPLACE, True)

        self.get_cached_response = {}
        self.post_cached_response = {}

    @staticmethod
    def __get_value_from_dict(config_dict: Dict, dict_key: str, pass_if_not_in_dict=False,
                              value_if_not_in_dict: Any = None) -> Any:
        if dict_key in config_dict:
            return config_dict[dict_key]
        else:
            if pass_if_not_in_dict:
                return value_if_not_in_dict
            else:
                logging.error(f'Key "{dict_key}" wasn\'t found in dict:'
                              f'{os.linesep + json.dumps(config_dict, ensure_ascii=False, indent=4)}')
                sys.exit(1)

    @staticmethod
    def decode_json_file(json_file: str, ignore_error: bool = False) -> Dict:
        if not os.path.exists(json_file):
            if ignore_error:
                return {}
            else:
                logging.error(f'"{os.path.basename(json_file)}" file not found')
                sys.exit(1)

        try:
            with open(json_file, "r", encoding="utf-8") as file:
                json_dict = json.load(file)
                file.close()

        except json.decoder.JSONDecodeError as json_decoder_error:
            logging.error(f'Failed to decode "{os.path.basename(json_file)}". Reason:{os.linesep}'
                          f'{f"{os.linesep}".join(arg for arg in json_decoder_error.args)}')
            sys.exit(1)
        except UnicodeDecodeError as unicode_decode_error:
            logging.error(unicode_decode_error.reason)
            sys.exit(1)

        return json_dict
