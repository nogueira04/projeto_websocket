import socket
import random

class RDT:
    def __init__(self, udp_socket, buffer_size=1024, loss_probability=0.1):
        self.udp_socket = udp_socket
        self.buffer_size = buffer_size
        self.seq_num = 0
        self.loss_probability = loss_probability
        self.udp_socket.settimeout(1)
        self.expected_seq_num = 0

    def simulate_packet_loss(self):
        return random.random() < self.loss_probability

    def send_packet(self, seq_num, data, addr):
        seq_bytes = seq_num.to_bytes(1, byteorder='big')
        packet = seq_bytes + data
        self.udp_socket.sendto(packet, addr)
        print(f"Sent packet {seq_num} to {addr}: {len(data)} bytes")

    def receive_packet(self):
        data, addr = self.udp_socket.recvfrom(self.buffer_size)
        seq_num = int.from_bytes(data[:1], byteorder='big')
        data = data[1:]
        return {'seq': seq_num, 'data': data}, addr

    def send(self, addr, message):
        if isinstance(message, str):
            data = message.encode('utf-8')
        else:
            data = message

        packet_number = 0
        data_length = len(data)
        while packet_number * (self.buffer_size - 1) < data_length:
            start = packet_number * (self.buffer_size - 1)
            end = min((packet_number + 1) * (self.buffer_size - 1), data_length)
            packet_data = data[start:end]

            while True:
                self.send_packet(self.seq_num, packet_data, addr)
                try:
                    ack_packet, _ = self.udp_socket.recvfrom(self.buffer_size)
                    ack_seq = int.from_bytes(ack_packet[:1], byteorder='big')
                    if ack_seq == self.seq_num:
                        print(f"ACK for packet {self.seq_num} received from {addr}")
                        break
                except socket.timeout:
                    print(f"Timeout, resending packet {self.seq_num}")

            packet_number += 1
            self.seq_num = (self.seq_num + 1) % 256  # Keep seq_num within 1 byte

        # send end of message packet
        eof_seq_num = self.seq_num
        while True:
            self.send_packet(eof_seq_num, b'', addr)
            print(f"End of message packet {eof_seq_num} sent to {addr}")
            try:
                ack_packet, _ = self.udp_socket.recvfrom(self.buffer_size)
                ack_seq = int.from_bytes(ack_packet[:1], byteorder='big')
                if ack_seq == eof_seq_num:
                    print(f"ACK for end of message packet {eof_seq_num} received from {addr}")
                    break
            except socket.timeout:
                print(f"Timeout, resending end of message packet {eof_seq_num}")

    def receive(self):
        received_data = []

        while True:
            try:
                packet, addr = self.receive_packet()
                print(f"Received packet {packet['seq']} from {addr}")
                if self.simulate_packet_loss():
                    print(f"Simulated packet loss for packet {packet['seq']} from {addr}")
                    continue

                if packet['seq'] < self.expected_seq_num:
                    print(f"Duplicate packet {packet['seq']} received from {addr}, resending ACK")
                    ack_packet = packet['seq'].to_bytes(1, byteorder='big')
                    self.udp_socket.sendto(ack_packet, addr)
                    continue

                if packet['seq'] == self.expected_seq_num:
                    if packet['data'] == b'':  # End of message packet
                        ack_packet = packet['seq'].to_bytes(1, byteorder='big')
                        self.udp_socket.sendto(ack_packet, addr)
                        print(f"End of message packet {packet['seq']} received from {addr}, closing connection")
                        break

                    received_data.append(packet['data'])
                    print(f"Packet {self.expected_seq_num} received from {addr}: {len(packet['data'])} bytes")
                    self.expected_seq_num = (self.expected_seq_num + 1) % 256
                    ack_packet = packet['seq'].to_bytes(1, byteorder='big')
                    self.udp_socket.sendto(ack_packet, addr)

            except socket.timeout:
                print(f"Timeout occurred. Waiting for packet {self.expected_seq_num}")

        message = b''.join(received_data).decode('utf-8')
        print(f"Message reception complete from {addr}")
        return message, addr

    def close(self):
        print("Closing socket")
        self.udp_socket.close()
