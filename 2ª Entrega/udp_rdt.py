import socket
import random
import pickle

class RDT:
    def __init__(self, udp_socket, buffer_size=1024, loss_probability=0.4):
        self.udp_socket = udp_socket
        self.buffer_size = buffer_size
        self.seq_num = 0
        self.loss_probability = loss_probability

    def simulate_packet_loss(self):
        return random.random() < self.loss_probability

    def send_packet(self, data, addr):
        packet = pickle.dumps({'seq': self.seq_num, 'data': data})
        self.udp_socket.sendto(packet, addr)

    def receive_packet(self):
        data, addr = self.udp_socket.recvfrom(self.buffer_size)
        packet = pickle.loads(data)
        return packet, addr

    def send(self, data, addr):
        packet_number = 0
        data_length = len(data)
        while packet_number * (self.buffer_size - 128) < data_length:
            start = packet_number * (self.buffer_size - 128)
            end = min((packet_number + 1) * (self.buffer_size - 128), data_length)
            packet_data = data[start:end]
            packet = pickle.dumps({'seq': self.seq_num, 'data': packet_data})
            ack_received = False
            while not ack_received:
                if not self.simulate_packet_loss():
                    self.udp_socket.sendto(packet, addr)
                    print(f"Sent packet {packet_number + 1}: {len(packet_data)} bytes")

                try:
                    ack, _ = self.udp_socket.recvfrom(self.buffer_size)
                    ack_packet = pickle.loads(ack)
                    if ack_packet['seq'] == self.seq_num and ack_packet['ack']:
                        ack_received = True
                        self.seq_num = 1 - self.seq_num
                        packet_number += 1
                        print(f"Received ACK for packet {packet_number}")
                except socket.timeout:
                    print(f"Timeout for packet {packet_number + 1}, retransmitting...")

        end_packet = pickle.dumps({'seq': self.seq_num, 'data': b''})
        self.udp_socket.sendto(end_packet, addr)
        print("File sent in", packet_number, "packets")

    def receive(self, file_path):
        packet_number = 0
        with open(file_path, "wb") as file:
            while True:
                try:
                    data, addr = self.udp_socket.recvfrom(self.buffer_size)
                    if not data:
                        continue

                    packet = pickle.loads(data)
                    if packet['seq'] == self.seq_num:
                        if packet['data'] == b'':
                            break
                        file.write(packet['data'])
                        self.seq_num = 1 - self.seq_num
                        ack_packet = pickle.dumps({'seq': packet['seq'], 'ack': True})
                        self.udp_socket.sendto(ack_packet, addr)
                        packet_number += 1
                        print("Packet", packet_number, "received from", addr, ": ", len(packet['data']), "bytes")

                except (socket.timeout, pickle.UnpicklingError) as e:
                    continue

        print("File received")
        return addr

    def close(self):
        print("Closing socket")
        self.udp_socket.close()
