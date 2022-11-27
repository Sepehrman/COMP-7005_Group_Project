class Packet:

    def __init__(self):
        self.data = None
        self.ack = None
        self.sequence_number = None

    def __str__(self):
        return f'Data: {self.data}\nACK: {self.ack}\n' \
               f'% ACK: ______\n%Data: ________'
