import logging
from os import linesep

import requests


class Exceptions:

    @staticmethod
    def resolve_requests_exceptions_connection_error(connection_error: requests.exceptions.ConnectionError):
        error_args = connection_error.args

        error_log = ""
        for error_arg in error_args:
            host = f'{error_arg.pool.host}:{error_arg.pool.port}'
            error_log += f'Connection error on host: "{host}". Reason:{linesep}'

            reason = ""
            for reason_arg in error_arg.reason.args:
                reason += reason_arg + linesep

            error_log += reason

        logging.error(error_log)
