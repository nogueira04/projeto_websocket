import socket
import random
import time

class RDT:
    def __init__(self, udp_socket, buffer_size=1024, loss_probability=0.1):
        self.udp_socket = udp_socket
        self.buffer_size = buffer_size
        self.seq_num = 0
        self.loss_probability = loss_probability

    def simulate_packet_loss(self):
        return random.random() < self.loss_probability

    def send_packet(self, data, addr):
        packet = str({'seq': self.seq_num, 'data': data}).encode()
        self.udp_socket.sendto(packet, addr)

    def receive_packet(self):
        data, addr = self.udp_socket.recvfrom(self.buffer_size)
        packet = eval(data.decode())
        return packet, addr

    def send(self, data, addr):
        packet_number = 0
        while True:
            packet = str({'seq': self.seq_num, 'data': data}).encode()
            ack_received = False
            while not ack_received:
                if not self.simulate_packet_loss():
                    self.udp_socket.sendto(packet, addr)
                    print(f"Sent packet {packet_number + 1}")

                try:
                    ack, _ = self.udp_socket.recvfrom(self.buffer_size)
                    ack_packet = eval(ack.decode())
                    if ack_packet['seq'] == self.seq_num and ack_packet['ack']:
                        ack_received = True
                        self.seq_num = 1 - self.seq_num
                        packet_number += 1
                        print(f"Received ACK for packet {packet_number}")
                except socket.timeout:
                    print(f"Timeout for packet {packet_number + 1}, retransmitting...")

            if not data:
                break

        self.udp_socket.sendto(b'', addr)
        print("File sent in", packet_number, "packets")

    def receive(self, file_path):
        packet_number = 0
        with open(file_path, "wb") as file:
            while True:
                try:
                    data, addr = self.udp_socket.recvfrom(self.buffer_size)
                    if not data:
                        break

                    packet = eval(data.decode())
                    if packet['seq'] == self.seq_num:
                        file.write(packet['data'])
                        self.seq_num = 1 - self.seq_num
                        self.udp_socket.sendto(str({'seq': packet['seq'], 'ack': True}).encode(), addr)
                        packet_number += 1
                        print("Packet ", packet_number, " received from ", addr)

                except socket.timeout:
                    continue

        print("File received")
        return addr

    def close(self):
        print("Closing socket")
        self.udp_socket.close()