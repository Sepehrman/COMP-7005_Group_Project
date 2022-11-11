import argparse
import socket

from request import ClientRequest

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
DEFAULT_PORT = 5001


def setup_client_cmd_request() -> ClientRequest:
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--ip", help="The IP address the client sends the request for. "
                                           "Must be set to a valid IP Address", required=True)
    parser.add_argument("-p", "--port", help="The port in which the client runs on "
                                             "Defaults to 5001", required=False, default=DEFAULT_PORT, type=int)

    try:
        args = parser.parse_args()
        req = ClientRequest()

        req.ip_address = args.ip
        req.port = args.port

        return req
    except Exception as e:
        print(f"An unexpected error occurred. {e}")
        quit()


def execute_request(req: ClientRequest):
    s = socket.socket()
    try:
        s.connect((req.ip_address, req.port))
        while True:
            message = input()
            s.send(message.encode('utf-8'))
            # print(s.recv(1024).decode('utf-8'))
    except Exception as e:
        print(f'Error: {e}')
    finally:
        s.close()

def main():
    request = setup_client_cmd_request()
    execute_request(request)


if __name__ == '__main__':
    main()