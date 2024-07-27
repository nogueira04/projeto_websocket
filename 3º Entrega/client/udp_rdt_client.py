import socket
from udp_rdt import RDT

class UDPClient:
    def __init__(self, sckt_family, sckt_type, sckt_binding, max_buff):
        self.sckt = socket.socket(sckt_family, sckt_type)
        self.sckt.bind(sckt_binding)
        print(f"Client bound to {self.sckt.getsockname()}")  # Adicionando mensagem de depuração para verificar a porta utilizada.
        self.rdt = RDT(self.sckt, max_buff)
        if self.sckt is None:
            raise "Socket not available."

    def send(self, server_addr, data):
        self.rdt.send(data, server_addr)

    def receive(self):
        return self.rdt.receive()
