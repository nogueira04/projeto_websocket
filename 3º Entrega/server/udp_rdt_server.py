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

    def receive(self, file_path):
        self.rdt.receive(file_path)
        print(f"Received file saved as {file_path}")

    def send(self, client_addr, file_path):
        with open(file_path, "rb") as file:
            data = file.read()
        self.rdt.send(data, client_addr)
        print(f"Sent file {file_path} to {client_addr}")

def main():
    server = UDPServer(socket.AF_INET, socket.SOCK_DGRAM, ("localhost", 8092), 1024)
    filename = input("Nome do arquivo a ser recebido (com extensão, ex: .png, .txt): ")
    server.receive(f"received_{filename}")
    server.send(("localhost", 8091), f"received_{filename}")
    server.sckt.close()

if __name__ == "__main__":
    main()
