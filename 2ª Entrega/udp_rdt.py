import socket
import random

class RDT:
    def __init__(self, udp_socket, buffer_size=1024, loss_probability=0.1):
        self.udp_socket = udp_socket
        self.buffer_size = buffer_size
        self.seq_num = 0
        self.loss_probability = loss_probability
        self.udp_socket.settimeout(1)  

    def simulate_packet_loss(self):
        return random.random() < self.loss_probability

    def send_packet(self, seq_num, data, addr):
        seq_bytes = seq_num.to_bytes(1, byteorder='big') 
        packet = seq_bytes + data  
        self.udp_socket.sendto(packet, addr)
        print(f"Sent packet {seq_num}: {len(data)} bytes")

    def receive_packet(self):
        data, addr = self.udp_socket.recvfrom(self.buffer_size)
        seq_num = int.from_bytes(data[:1], byteorder='big') 
        data = data[1:] 
        return {'seq': seq_num, 'data': data}, addr

    def send(self, data, addr):
        packet_number = 0
        data_length = len(data)
        while packet_number * (self.buffer_size - 1) < data_length:  # account for sequence number
            start = packet_number * (self.buffer_size - 1)
            end = min((packet_number + 1) * (self.buffer_size - 1), data_length)
            packet_data = data[start:end]

            while True:
                self.send_packet(self.seq_num, packet_data, addr)
                try:
                    ack_packet, _ = self.udp_socket.recvfrom(self.buffer_size)
                    ack_seq = int.from_bytes(ack_packet[:1], byteorder='big')
                    if ack_seq == self.seq_num:
                        print(f"ACK for packet {self.seq_num} received")
                        break
                except socket.timeout:
                    print(f"Timeout, resending packet {self.seq_num}")

            packet_number += 1
            self.seq_num += 1  

        # send end of file packet
        eof_seq_num = self.seq_num  
        while True:
            self.send_packet(eof_seq_num, b'', addr)
            print("End of file sent")
            try:
                ack_packet, _ = self.udp_socket.recvfrom(self.buffer_size)
                ack_seq = int.from_bytes(ack_packet[:1], byteorder='big')
                if ack_seq == eof_seq_num:
                    print(f"ACK for EOF packet received")
                    break
            except socket.timeout:
                print("Timeout, resending EOF packet")

    def receive(self, file_path):
        expected_seq_num = 0
        
        with open(file_path, "wb") as file:
            while True:
                try:
                    packet, addr = self.receive_packet()
                    
                    if self.simulate_packet_loss():
                        print(f"Simulated packet loss for packet {packet['seq']}")
                        continue

                    if packet['seq'] < expected_seq_num:
                        print(f"Duplicate packet {packet['seq']} received, resending ACK")
                        ack_packet = packet['seq'].to_bytes(1, byteorder='big')
                        self.udp_socket.sendto(ack_packet, addr)
                        continue

                    if packet['seq'] == expected_seq_num:
                        if packet['data'] == b'':  # EOF packet
                            ack_packet = packet['seq'].to_bytes(1, byteorder='big')
                            self.udp_socket.sendto(ack_packet, addr)
                            print("EOF packet received, closing connection")
                            break
                        
                        file.write(packet['data'])
                        print(f"Packet {expected_seq_num} received from {addr}: {len(packet['data'])} bytes")
                        expected_seq_num += 1
                        ack_packet = packet['seq'].to_bytes(1, byteorder='big')
                        self.udp_socket.sendto(ack_packet, addr)

                except socket.timeout:
                    print(f"Timeout occurred. Waiting for packet {expected_seq_num}")

        print("File reception complete")

    def close(self):
        print("Closing socket")
        self.udp_socket.close()
