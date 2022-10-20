from http.server import HTTPServer

from common.http_get_handler import HttpGetHandler
from common.settings import parse_console_args_and_get_settings


def main():
    settings = parse_console_args_and_get_settings()

    http_get_handler = HttpGetHandler
    http_get_handler.settings = settings

    web_server = HTTPServer(("", settings.util_port), http_get_handler)

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        web_server.server_close()


if __name__ == '__main__':
    main()
