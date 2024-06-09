import socket
import time

class UDPClient():
    def __init__(self, sckt_family, sckt_type, sckt_binding, MAX_BUFF):
        self.sckt = socket.socket(sckt_family, sckt_type)
        self.sckt.bind(sckt_binding)
        self.sckt.settimeout(0.1)

        if self.sckt is None:
            raise "Socket not available."
        
        self.MAX_BUFF = MAX_BUFF
    
    def listen(self):
        while True:
            try:
                data, addr = self.sckt.recvfrom(self.MAX_BUFF)
            
            except:
                continue
    
    def send(self, server_addr, msg):
        self.sckt.sendto(msg, server_addr)
        time.sleep(0.0001)