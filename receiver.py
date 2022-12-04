#!/usr/bin/python
# Server

'''

This is the receiver (server). The receiver starts up first, waits for connections,
receives data and writes it to console. The server also sends acks back for each packet received.
Maintains a list of stats and takes cmd line args for port to receive from.

'''


import argparse
import os
import pickle
import socket

from packet import Packet
from request import ReceiverRequest

SERVER_HOST = '192.168.1.138'
DEFAULT_PORT = 9000
MAX_INCOMING_CONNECTIONS = 999


def execute_requests(req):

    try:

        # Create a socket object
        s = socket.socket()
        print("Socket created!")

        # Bind socket to server host and port (default, if not provided)
        s.bind((SERVER_HOST, req.port))
        print("Bind complete!")

        # Socket now listening
        s.listen(MAX_INCOMING_CONNECTIONS)
        print(f"[LOG] Socket now Listening as {SERVER_HOST}:{req.port}")

        accepting = True

        # Accept connections
        client_socket, address = s.accept()
        print(f"[LOG] {address} has connected.")

        data_pkt_received = 0
        ack_pkt_sent = 0

        while accepting:

            # Receive data (packet object)
            packet = pickle.loads(client_socket.recv(2048))
            data_pkt_received += 1

            # Print to console
            # print(f"'{address[0]}': {packet.data}")

            # Send acks back for data received
            send_back_ack(client_socket, packet)
            ack_pkt_sent += 1

            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"'{address[0]}': {packet.data}")
            print("Data packets received: {}".format(data_pkt_received))
            print("Ack packets sent: {}".format(ack_pkt_sent))

        s.close()

    except Exception as e:
        print(f"Error: {e}")
        quit()


def send_back_ack(csocket, packet):
    # Send acknowledgement packets for each data packet received.
    packet.ack = "ACK"
    csocket.send(pickle.dumps(packet))


def setup_receiver_cmd_request() -> ReceiverRequest:
    # Command line arguments

    # Create a command line parser
    parser = argparse.ArgumentParser()

    # Arguments: ./receiver.py -p 8000
    parser.add_argument("-p", "--port", help="The port in which the program should run. Defaults to 8000",
                        required=False, default=DEFAULT_PORT, type=int)
    try:
        # Execute the parse_args() method
        args = parser.parse_args()

        # Initialize receive request object
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