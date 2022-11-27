#!/usr/bin/python
# Server


import argparse
import os
import pickle
import socket
import ssl

from packet import Packet
from request import ReceiverRequest

SERVER_HOST = '127.0.0.1'
#socket.gethostbyname(socket.gethostname())
DEFAULT_PORT = 8000
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
            packet = pickle.loads(client_socket.recv(1024))
            print(f"'{address[0]}': {packet.data}")
            send_back_ack(client_socket, packet)
        s.close()

    except Exception as e:
        print(f"Error: {e}")
        quit()


def send_back_ack(csocket, packet):
    packet.ack = "ACK"
    csocket.send(pickle.dumps(packet))


def setup_receiver_cmd_request() -> ReceiverRequest:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="The port in which the program should run. Defaults to 8000",
                        required=False, default=DEFAULT_PORT, type=int)
    try:
        args = parser.parse_args()
        req = ReceiverRequest()
        req.port = args.port

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