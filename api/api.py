import argparse
import logging
import socketserver
import uuid
import subprocess
import os

from http.server import BaseHTTPRequestHandler
from functools import partial


logging.basicConfig(level=logging.INFO)

TOKEN = uuid.uuid4().hex
with open(".secret", "w") as f:
    f.write(TOKEN)


class HTTPHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server, directory):
        self.directory = directory
        super().__init__(request, client_address, server)

    def do_POST(self):
        if self.path == "/git-hook":
            self.delivery()
        else:
            self.send_response(400)
        self.end_headers()

    def delivery(self):
        auth = self.headers.get('Authorization')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        subprocess.call(f"ls {dir_path}", shell=True)
        if not auth:
            self.send_response(401)
            return
        token = auth.replace("Token ", "")
        if token != TOKEN:
            self.send_response(401)
            return
        self.send_response(200)
        subprocess.call(
            f"bash {os.path.join(dir_path, 'deploy.sh')} -d {self.directory}",
            shell=True
        )


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(
        description="Simple Webserver for opening ports for Git Hooks"
    )
    parser.add_argument(
        "directory", help="Directory to compare to remote branch"
    )
    parser.add_argument(
        "--port", help="Portnumber. Default 5050", default=5050
    )

    return vars(parser.parse_args())


if __name__ == "__main__":
    args = parse_cmd_arguments()
    handler = partial(HTTPHandler, directory=args["directory"])
    with socketserver.TCPServer(("", args["port"]), handler) as http_:
        logging.info(f"serving at port {args['port']}")
        http_.serve_forever()
