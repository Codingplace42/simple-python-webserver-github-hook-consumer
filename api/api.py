import argparse
import logging
import socketserver
import uuid

from http.server import BaseHTTPRequestHandler

logging.basicConfig(level=logging.INFO)

TOKEN = uuid.uuid4().hex
logging.info(f"Init Token: {TOKEN}")


def get_token(header):
    auth = header.get('Authorization')
    return auth.replace("Token ", "")    


class HTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/git-hook":
            self.delivery()
        else:
            self.send_response(400)
        self.end_headers()

    def delivery(self):
        token = get_token(self.headers)
        if token != TOKEN:
            self.send_response(401)
            return
        self.send_response(200)


def parse_cmd_arguments():
    parser = argparse.ArgumentParser(
        description="Simple Webserver for opening ports for Git Hooks"
    )
    parser.add_argument(
        "--port", help="Portnumber. Default 5050", default=5050
    )

    return vars(parser.parse_args())


if __name__ == "__main__":
    args = parse_cmd_arguments()
    Handler = HTTPHandler
    with socketserver.TCPServer(("", args["port"]), Handler) as httpd:
        print("serving at port", args["port"])
        httpd.serve_forever()
