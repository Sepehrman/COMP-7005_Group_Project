class SenderRequest:

    def __init__(self):
        self.port = None
        self.next_host = None
        self.file = None
        self.payload = None

    def __str__(self):
        return f"SenderRequest: port: {self.port}, next_host: {self.next_host}, file: {self.file}, payload: {self.payload}"


class ProxyRequest:

    def __init__(self):
        self.port_sender = None
        self.port_receiver = None
        self.previous_host = None
        self.next_host = None

    def __str__(self):
        return f"ProxyRequest: Sender port: {self.port_sender}, Receiver port: {self.port_receiver}, " \
               f"previous_host: {self.previous_host}, next_host {self.next_host}"


class ReceiverRequest:

    def __init__(self):
        self.port = None
        # self.display_host = None

    def __str__(self):
        return f"ReceiverRequest: port: {self.port}, display_host: {self.display_host}"
