class ServerRequest:

    def __init__(self):
        self.port = None
        self.private_key = None
        self.public_key = None

    def __str__(self):
        return f"ServerRequest: port: {self.port}, private_key: {self.private_key}, public_key {self.public_key}"


class ClientRequest:

    def __init__(self):
        self.ip_address = None
        self.files = None
        self.port = None

    def __str__(self):
        return f"ClientRequest: ip_address: {self.ip_address}, port {self.port}"