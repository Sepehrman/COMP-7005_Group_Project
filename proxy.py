import argparse
import socket

from request import ProxyRequest
DEFAULT_PORT = 5000
MAX_INCOMING_CONNECTIONS = 999

def setup_proxy_cmd_request() -> ProxyRequest:
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="The port in which the program should run. Defaults to 8000",
                        required=False, default=DEFAULT_PORT, type=int)
    parser.add_argument("-i", "--passer", help="IP Address of the Pass host", required=True)
    parser.add_argument("-o", "--display", help="IP Address of the Display host", required=True)

    try:
        args = parser.parse_args()
        req = ProxyRequest()
        req.port = args.port
        req.next_host = args.display
        req.previous_host = args.passer

        return req
    except Exception as e:
        print(f"Exception: {e}")
        quit()
    except KeyboardInterrupt:
        quit()


def execute_requests(req: ProxyRequest):
    try:

        s = socket.socket()
        s.bind((req.previous_host, req.port))
        s.listen(MAX_INCOMING_CONNECTIONS)

        client_socket, address = s.accept()
        print(f"[LOG] {address} has connnected.")

        received_message = client_socket.recv(1024).decode()

        if received_message:
            client_socket.send(bytes(received_message.upper(), 'utf-8'))
            print(f'Sending {received_message}')
        client_socket.close()
        s.close()

    except Exception as e:
        print(f"Error with {e}")

def main():
    requests = setup_proxy_cmd_request()
    execute_requests(requests)


if __name__ == '__main__':
    main()