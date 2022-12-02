#!/usr/bin/python
# Client

'''

This is the sender (client). The sender reads from the keyboard and sends a file or a string and waits to receive
acknowledgements for data packets sent. If no acks are received by timeout, resend data packets. The sender maintains
a list of stats, and takes cmd line args for IP or proxy/receiver and port.

'''


import argparse
import socket

from packet import Packet
from request import SenderRequest
import os.path
import pickle
import os


DEFAULT_PORT = 9000             # Default port to connect to

# Command line arguments
def setup_sender_cmd_request() -> SenderRequest:

    # Create a command line parser
    parser = argparse.ArgumentParser()

    # Arguments: ./sender.py -p 8000 -i <IP of proxy/receiver>
    parser.add_argument("-p", "--port", help="The port to connect to. Defaults to 8000",
                        required=False, default=DEFAULT_PORT, type=int)
    parser.add_argument("-i", "--stdin", help="IP Address of the next host (receiver/proxy)",
                        required=True, type=str)
    parser.add_argument("-f", "--file", help="A file or string")

    try:
        # Execute the parse_args() method
        args = parser.parse_args()

        # Initialize a request object
        req = SenderRequest()

        req.port = args.port
        req.next_host = args.stdin
        req.file = args.file

        # Check if argument is a file or string or if no argument was provided.
        if req.file is not None and is_file(req.file):
            # Open and read file
            with open(req.file, "r") as file:
                data = file.read()
                # Set object payload to the data in file
                req.payload = data
                print(req.payload)
        elif req.file is not None and not is_file(req.file):
            req.payload = req.file

        return req

    except Exception as e:
        print(f"An unexpected error occurred. {e}")
        quit()


def is_file(file):
    # Checks to see if the argument is a file and returns bool.
    return os.path.isfile(file)


def execute_request(req: SenderRequest):

    # Create a socket object
    s = socket.socket()

    # Initialize a data packet object
    data_packet = Packet()

    try:
        # Check is port argument is argument
        if req.port is not None:
            s.connect((req.next_host, req.port))
        # No port argument. Default port = 8000
        else:
            s.connect((req.next_host, DEFAULT_PORT))

        # If a file is provided, req.payload is data from file.
        if req.payload:

            data = req.payload.split('\n')
            print(data)
            for word in data:
                data_packet.data = word
            send_packet(s, data_packet)
            s.settimeout(10)
            receive_ack(s)

        while True:

            # No file provided. Ask user for input
            data_packet.data = input()
            # print(data_packet.data)

            # Check if input is a file
            if is_file(data_packet.data):
                # Open and read file
                with open(data_packet.data, "r") as file:
                    data = file.read()
                    data_packet.data = data

            # os.system('cls' if os.name == 'nt' else 'clear')

            # Send data packet
            send_packet(s, data_packet)

            # Set timeout for 10 seconds
            s.settimeout(5)

            ''' 
            Timeout should be called after data is sent because it checks for subsequent 
            socket functions to be completed before timeout is called. In other words if acks are not received within
            10 seconds, timeout error is called. 
            '''

            # Receive ack packet
            receive_ack(s)

            # print(data_packet)

    except TimeoutError as e:
        handle_timeout_error(s, data_packet)
    except Exception as e:
        print(f'Error: {e}')
    finally:
        s.close()


def receive_ack(sock):
    ack_packet = pickle.loads(sock.recv(1024))
    if ack_packet.ack == "ACK":
        print(ack_packet)
    else:
        print("No ACK Received")


def send_packet(s, packet):
    s.send(pickle.dumps(packet))


def handle_timeout_error(sock, packet):
    # Recursive handler that keeps retransmitting data

    # 10 seconds are up!
    print("Handling Timeout")

    try:

        # Retransmit data packet object
        send_packet(sock, packet)
        print("Packet retransmitted ... ")

        # Set timeout for 10 seconds
        sock.settimeout(10)

        # Receive ack packet
        receive_ack(sock)
        print(packet)

    except TimeoutError as e:
        handle_timeout_error(sock, packet)


def main():
    #os.system('cls' if os.name == 'nt' else 'clear')
    request = setup_sender_cmd_request()
    execute_request(request)


if __name__ == '__main__':
    main()
