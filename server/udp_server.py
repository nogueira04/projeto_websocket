import socket
import time

class UDPServer():
    def __init__(self, sckt_family, sckt_type, sckt_binding, MAX_BUFF):
        self.sckt = socket.socket(sckt_family, sckt_type)
        self.sckt.bind(sckt_binding)
        self.sckt.settimeout(0.1)

        if self.sckt is None:
            raise "Socket not available."
        
        print("Listening on", sckt_binding)
        
        self.MAX_BUFF = MAX_BUFF
    
    def listen(self):
        while True:
            try:
                data, addr = self.sckt.recvfrom(self.MAX_BUFF)

                print("Received", data.decode(), "from", addr)
                if data.decode() == "olá servidor":
                    self.send(addr, "olá cliente")
            
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
    server = UDPServer(socket.AF_INET, socket.SOCK_DGRAM, ("localhost", 8092), 1024)
    server.listen()



if __name__ == "__main__":
    main()