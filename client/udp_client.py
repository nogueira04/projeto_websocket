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
            
                print("Received", data.decode(), "from", addr)

            except Exception as e:
                if e == KeyboardInterrupt:
                    self.sckt.close()
                    break
                else:
                    continue
    
    def send(self, server_addr, msg):
        self.sckt.sendto(msg.encode(), server_addr)
        print("Sent", msg, "to", server_addr)
        time.sleep(0.0001)


def main():
    client = UDPClient(socket.AF_INET, socket.SOCK_DGRAM, ("localhost", 8091), 1024)
    client.send(("localhost", 8092), "olá servidor")
    client.listen()


if __name__ == "__main__":
    main()