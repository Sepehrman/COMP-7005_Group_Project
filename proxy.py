#!/usr/bin/python
# Proxy server

'''

This is a proxy server that sits between server and client. The proxy server passes data from sender to receiver.
The proxy can randomly drop packets and allows user to dynamically set % of data and ack packets dropped.
It also maintains a list of stats. The Proxy takes command line arguments for IP of server, port to send to (receiver),
and port to listen to (sender).

The Receiver (server) is run first.
Then Proxy,
And then Sender.

'''

import argparse
import socket
import pickle
import random

from request import ProxyRequest

PROXY_HOST = '127.0.0.1'
MAX_INCOMING_CONNECTIONS = 999

def setup_proxy_cmd_request() -> ProxyRequest:
    # Command line arguments

    # Create a command line parser
    parser = argparse.ArgumentParser()

    # Arguments: ./proxy.py -p 8000 -s 8000 -i <IP of proxy> -o <IP of receiver>
    parser.add_argument("-p", "--receiver", dest="port_receiver", help="The port in which the program should run. Defaults to 8000",
                        required=True, type=int)
    parser.add_argument("-s", "--sender", dest="port_sender", help="The port in which the program should run. Defaults to 8000",
                        required=True, type=int)
    parser.add_argument("-i", "--proxy", help="IP Address of the proxy host", required=False, default=PROXY_HOST)
    parser.add_argument("-o", "--display", help="IP Address of the Display host", required=True)

    try:
        # Execute the parse_args() method
        args = parser.parse_args()

        # Initialize proxy request object
        req = ProxyRequest()

        req.port_receiver = args.port_receiver
        req.port_sender = args.port_sender
        req.next_host = args.display
        req.previous_host = args.proxy

        return req

    except Exception as e:
        print(f"Exception: {e}")
        quit()
    except KeyboardInterrupt:
        quit()


def execute_requests(req: ProxyRequest):

    try:

        receiver_socket = socket.socket()
        receiver_socket.connect((req.next_host, req.port_receiver))


        sender_socket = socket.socket()
        sender_socket.bind((req.previous_host, req.port_sender))
        sender_socket.listen(MAX_INCOMING_CONNECTIONS)

        client_socket, address = sender_socket.accept()
        print(f"[LOG] {address} has connnected.")
        drop_data_packets = int(input("Drop % data packets [1% - 100%]: "))
        drop_data_packets = drop_data_packets / 100
        #print(drop_data_packets)
        # drop_ack_packets = int(input("Drop % ack packets: "))
        # drop_ack_packets = drop_ack_packets / 100

        received_packets = []
        data_pkt = 0

        while True:

            # Receive data packets from sender
            received_message = pickle.loads(client_socket.recv(2048))
            print(received_message)
            received_packets.append(received_message)
            #print(len(received_packets))
            # for pkt in received_packets:



            # if there is data, send it to the receiver host
            receiver_socket.send(pickle.dumps(received_message))


            ack_packet = pickle.loads(receiver_socket.recv(2048))
            print(ack_packet)

            client_socket.send(pickle.dumps(ack_packet))

            # client_socket.close()

    except Exception as e:
        print(f"Error with {e}")


def receive_ack(sock):
    ack_packet = pickle.loads(sock.recv(1024))
    if ack_packet.ack == "ACK":
        print("ACK")
    else:
        print("No ACK Received")

    return ack_packet


# def drop_data_packets():
#     # Randomly drop data packets from sender
#     drop_packets = int(input("Drop % of data packets: "))
#
#     print(drop_packets)

def list_of_stats():
    pass


def main():
    requests = setup_proxy_cmd_request()
    execute_requests(requests)


if __name__ == '__main__':
    main()