#!/usr/bin/python
# Client

import argparse
import socket

from packet import Packet
from request import SenderRequest
import os.path
import pickle

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

        if req.file is not None and is_file(req.file):
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
    packet = Packet()
    s.settimeout(10)
    try:
        s.connect((req.next_host, DEFAULT_PORT))
        while True:
            if req.payload:
                s.send(req.payload.encode('utf-8'))
            packet.data = input()
            send_packet(s, packet)
            receive_ack(s)

    except TimeoutError as e:
        handle_timeout_error(s, packet)
    except Exception as e:
        print(f'Error: {e}')
    finally:
        s.close()


def receive_ack(sock):
    packet = pickle.loads(sock.recv(1024))
    if packet.ack == "ACK":
        print("ACK")
    else:
        print("No ACK Received")


def send_packet(s, packet):
    s.send(pickle.dumps(packet))


def handle_timeout_error(sock, packet):
    print("Handling Timeout")
    sock.send(packet.data.encode('utf-8'))


def main():
    request = setup_sender_cmd_request()
    execute_request(request)


if __name__ == '__main__':
    main()
