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
import os
import pickle
import random
import time

from request import ProxyRequest
from matplotlib import pyplot as plt

PROXY_HOST = '127.0.0.1'
MAX_INCOMING_CONNECTIONS = 999
timer = []
start_time = time.time()
data = []


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

        receive_and_drop_data(client_socket, receiver_socket)


    except Exception as e:
        print(f"Error with {e}")


def receive_and_drop_data(client_socket, receiver_socket):

    drop_data_packets= int(input("Drop % data packets [0% - 100%]: "))
    # print(drop_data_packets)
    drop_ack_packets = int(input("Drop % ack packets [0% - 100%]: "))

    received_packets = []
    data_pkt = 0
    dropped_data_pkt = 0
    sent_data_pkt = 0

    ack_pkt = 0
    dropped_ack_pkt = 0
    sent_ack_pkt = 0

    while True:

        # Receive data packets from sender
        received_message = pickle.loads(client_socket.recv(2048))
        # print(received_message.data)
        received_packets.append(received_message)
        # print("Received packets list: {}" .format(received_packets))

        current_time = time.time() - start_time
        timer.append(current_time)
        data.append(received_message.data)
        generate_graph(timer, data)

        data_pkt += 1
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Data packets received: {}".format(data_pkt))

        # if received_message in received_packets:
        if random.randrange(start=0, stop=100) <= drop_data_packets:
            received_packets.remove(received_message)
            dropped_data_pkt += 1
            print("Data packets dropped: {}".format(dropped_data_pkt))
            print("Data packets sent to receiver: {}".format(sent_data_pkt))

        if received_message in received_packets:
            receiver_socket.send(pickle.dumps(received_message))
            sent_data_pkt += 1
            print("Data packets dropped: {}".format(dropped_data_pkt))
            print("Data packets sent to receiver: {}".format(sent_data_pkt))
            ack_pkt += 1
            print("ACK packets received: {}".format(ack_pkt))
            # print("ACK packets received: {}".format(ack_pkt))
            dropped_ack_pkt, sent_ack_pkt = receive_and_drop_acks(client_socket, receiver_socket, drop_ack_packets, dropped_ack_pkt, sent_ack_pkt)
            dropped_ack_pkt = dropped_ack_pkt
            print("ACK packets dropped: {}".format(dropped_ack_pkt))

            sent_ack_pkt = sent_ack_pkt
            print("ACK packets sent to sender: {}".format(sent_ack_pkt))

        #print("Data packets received: {}".format(data_pkt))
        #
        # print("ACK packets dropped: {}".format(dropped_ack_pkt))
        # print("ACK packets sent to receiver: {}".format(sent_ack_pkt))


def receive_and_drop_acks(client_socket, receiver_socket, drop_ack_packets, dropped_ack_pkt, sent_ack_pkt):

    received_acks = receive_ack(receiver_socket)
    # print(received_acks)

    # if received_message in received_packets:
    if random.randrange(start=0, stop=100) <= drop_ack_packets:
        dropped_ack_pkt += 1
        pass
    else:
        client_socket.send(pickle.dumps(received_acks))
        sent_ack_pkt += 1

    return dropped_ack_pkt, sent_ack_pkt


def receive_ack(sock):
    ack_packet = pickle.loads(sock.recv(1024))
    # if ack_packet.ack == "ACK":
    #    print("ACK")
    # else:
    #    print("No ACK Received")

    return ack_packet


def generate_graph(x, y):
    plt.title("Data Transfer")
    plt.ylabel("Data")
    plt.xlabel("Time")
    plt.plot(x, y)
    plt.draw()
    plt.pause(0.001)


def main():
    requests = setup_proxy_cmd_request()
    execute_requests(requests)


if __name__ == '__main__':
    main()
