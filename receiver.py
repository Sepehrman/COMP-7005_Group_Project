import argparse
import os
import socket
import ssl

from request import ServerRequest

SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
MAX_INCOMING_CONNECTIONS = 999
DEFAULT_PATH = './server/downloads/'


def create_socket(req):
    try:

        s = socket.socket()
        s.bind((SERVER_HOST, req.port))
        s.listen(MAX_INCOMING_CONNECTIONS)

        print(f"[LOG] Listening as {SERVER_HOST}:{req.port}")
        accepting = True
        client_socket, address = s.accept()
        print(f"[LOG] {address} has connnected.")
        while accepting:

            received_message = client_socket.recv(1024).decode()

            if received_message:
                client_socket.send(bytes(received_message.upper(), 'utf-8'))
                print(received_message)
        client_socket.close()
        s.close()

    except Exception as e:
        print(f"Error with {e}")


def init_server(req: ServerRequest):
    create_socket(req)


def setup_server_cmd_request() -> ServerRequest:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="The port in which the program should run. Defaults to 8000",
                        required=False, default=SERVER_PORT, type=int)

    try:
        args = parser.parse_args()
        req = ServerRequest()
        req.port = args.port

        return req
    except Exception as e:
        print(f"An unexpected error occurred. {e}")
        quit()
    except KeyboardInterrupt:
        quit()


def main():
    request = setup_server_cmd_request()
    init_server(request)


if __name__ == "__main__":
    main()