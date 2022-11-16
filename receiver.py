#!/usr/bin/python
import argparse
import os
import socket
import ssl

from request import ReceiverRequest

SERVER_HOST = socket.gethostbyname(socket.gethostname())
DEFAULT_PORT = 5000
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
MAX_INCOMING_CONNECTIONS = 999
DEFAULT_PATH = './server/downloads/'


def execute_requests(req):
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
            print(f"Display: {received_message}")
            # if received_message:
            #     client_socket.send(bytes(received_message.upper(), 'utf-8'))
            #     print(received_message)
        client_socket.close()
        s.close()

    except Exception as e:
        print(f"Error with {e}")


def setup_receiver_cmd_request() -> ReceiverRequest:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="The port in which the program should run. Defaults to 8000",
                        required=False, default=DEFAULT_PORT, type=int)
    parser.add_argument("-i", "--display", help="IP Address of the Display host", default=SERVER_HOST)
    try:
        args = parser.parse_args()
        req = ReceiverRequest()
        req.port = args.port
        req.display_host = args.display

        return req
    except Exception as e:
        print(f"An unexpected error occurred. {e}")
        quit()
    except KeyboardInterrupt:
        quit()


def main():
    request = setup_receiver_cmd_request()
    execute_requests(request)


if __name__ == "__main__":
    main()