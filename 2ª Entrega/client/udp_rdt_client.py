import socket
from udp_rdt import RDT

class UDPClient:
    def __init__(self, sckt_family, sckt_type, sckt_binding, max_buff):
        self.sckt = socket.socket(sckt_family, sckt_type)
        self.sckt.bind(sckt_binding)
        self.rdt = RDT(self.sckt, max_buff)
        if self.sckt is None:
            raise "Socket not available."

    def send(self, server_addr, file_path):
        with open(file_path, "rb") as file:
            data = file.read()  
        self.rdt.send(data, server_addr)
        print(f"Sent file {file_path} to {server_addr}")

    def receive(self, file_path):
        self.rdt.receive(file_path)
        print(f"Received file saved as {file_path}")

def main():
    client = UDPClient(socket.AF_INET, socket.SOCK_DGRAM, ("localhost", 8091), 1024)
    filename = input("Nome do arquivo a ser enviado (com extensão, ex: .png, .txt): ")
    client.send(("localhost", 8092), filename)
    client.receive(f"received_{filename}")
    client.sckt.close()

if __name__ == "__main__":
    main()
