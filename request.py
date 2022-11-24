class SenderRequest:

    def __init__(self):
        self.port = None
        self.next_host = None

    def __str__(self):
        return f"SenderRequest: port: {self.port}, next_host: {self.next_host}"


class ProxyRequest:

    def __init__(self):
        self.port = None
        self.previous_host = None
        self.next_host = None

    def __str__(self):
        return f"ProxyRequest: port: {self.port}, previous_host: {self.previous_host}, next_host {self.next_host}"


class ReceiverRequest:

    def __init__(self):
        self.port = None
        # self.display_host = None

    def __str__(self):
        return f"ReceiverRequest: port: {self.port}, display_host: {self.display_host}"
