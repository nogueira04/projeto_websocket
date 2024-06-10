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
    
    def listen(self, file_path):
        with open(file_path, "wb") as file:
            while True:
                try:
                    data, addr = self.sckt.recvfrom(self.MAX_BUFF)

                    if not data: 
                        return addr
                    
                    file.write(data)
                    print("File ", file_path, " received from ", addr)
            
                except Exception as e:
                    if e == KeyboardInterrupt:
                        self.sckt.close()
                        break
                    else:
                        continue
    
    def send(self, server_addr, file_path):
        with open(file_path, "rb") as file:
            while True:
                data = file.read(self.MAX_BUFF)
                if not data:
                    break
                self.sckt.sendto(data, server_addr)
        
        self.sckt.sendto(b'', server_addr)
        print("File ", file_path, " sent to ", server_addr)
        time.sleep(0.0001)


def main():
    server = UDPServer(socket.AF_INET, socket.SOCK_DGRAM, ("localhost", 8092), 1024)
    addr = server.listen("received_digit.png")
    server.send(addr, "received_digit.png")


if __name__ == "__main__":
    main()