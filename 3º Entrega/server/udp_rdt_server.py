import socket
from udp_rdt import RDT

class UDPServer:
    def __init__(self, sckt_family, sckt_type, sckt_binding, max_buff):
        self.sckt = socket.socket(sckt_family, sckt_type)
        self.sckt.bind(sckt_binding)
        self.rdt = RDT(self.sckt, max_buff)
        if self.sckt is None:
            raise "Socket not available."
        print("Listening on", sckt_binding)

    def receive(self):
        return self.rdt.receive()

    def send(self, client_addr, data):
        self.rdt.send(data, client_addr)

