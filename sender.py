#!/usr/bin/python
# Client

import argparse
import socket

from packet import Packet
from request import SenderRequest
import os.path

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
DEFAULT_PORT = 8000


def setup_sender_cmd_request() -> SenderRequest:
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--port", help="The port in which the client runs on "
                                             "Defaults to 5000", required=False, default=DEFAULT_PORT)
    parser.add_argument("-i", "--stdin", help="IP Address of the next host", required=True, type=str)
    parser.add_argument('-f', "--file", help="A file with a correct directory to read from")

    try:
        args = parser.parse_args()
        req = SenderRequest()
        req.next_host = args.stdin
        req.file = args.file

        if is_file(req.file):
            with open(req.file, "r") as file:
                data = file.read()
                req.payload = data

        return req
    except Exception as e:
        print(f"An unexpected error occurred. {e}")
        quit()


def is_file(file):
    return os.path.isfile(file)

def execute_request(req: SenderRequest):
    s = socket.socket()
    try:
        s.connect((req.next_host, DEFAULT_PORT))
        s.settimeout(10)
        while True:
            packet = Packet()
            if req.payload:
                s.send(req.payload.encode('utf-8'))
            packet.data = input()

            s.send(packet.data.encode('utf-8'))
            packet.ack = s.recv(1024).decode()
            print(packet.ack)
    except TimeoutError as e:
        print("Handling Timeout")

    except Exception as e:
        print(f'Error: {e}')
    finally:
        s.close()



def handle_timeout_error():
    pass


def main():
    request = setup_sender_cmd_request()
    print(request)
    execute_request(request)


if __name__ == '__main__':
    main()
