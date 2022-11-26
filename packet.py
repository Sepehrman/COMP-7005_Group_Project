class Packet:

    def __init__(self):
        self.data = None
        self.ack = "ACK"

    def __str__(self):
        return f'Packet data: {self.data}, ack: {self.ack}'
