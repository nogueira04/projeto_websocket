import socket

class RDT:
    def __init__(self, udp_socket, buffer_size=1024):
        self.udp_socket = udp_socket
        self.buffer_size = buffer_size
        self.udp_socket.settimeout(1)
        self.seq_nums = {}  # Dictionary to store sequence numbers
        self.expected_seq_nums = {}  # Dictionary to store expected sequence numbers

    def send_packet(self, seq_num, data, addr):
        seq_bytes = seq_num.to_bytes(1, byteorder='big')
        packet = seq_bytes + data
        self.udp_socket.sendto(packet, addr)
        # print(f"Sent packet {seq_num} to {addr}: {len(data)} bytes")

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
        self.seq_nums.setdefault(addr, 0)
        while packet_number * (self.buffer_size - 1) < data_length:
            start = packet_number * (self.buffer_size - 1)
            end = min((packet_number + 1) * (self.buffer_size - 1), data_length)
            packet_data = data[start:end]

            while True:
                self.send_packet(self.seq_nums[addr], packet_data, addr)
                try:
                    ack_packet, _ = self.udp_socket.recvfrom(self.buffer_size)
                    ack_seq = int.from_bytes(ack_packet[:1], byteorder='big')
                    if ack_seq == self.seq_nums[addr]:
                        break
                except socket.timeout:
                    continue

            packet_number += 1
            self.seq_nums[addr] = (self.seq_nums[addr] + 1) % 256 

        # Send end of message packet
        eof_seq_num = self.seq_nums[addr]
        while True:
            self.send_packet(eof_seq_num, b'', addr)
            try:
                ack_packet, _ = self.udp_socket.recvfrom(self.buffer_size)
                ack_seq = int.from_bytes(ack_packet[:1], byteorder='big')
                if ack_seq == eof_seq_num:
                    break
            except socket.timeout:
                continue

    def receive(self):
        received_data = []

        while True:
            try:
                packet, addr = self.receive_packet()
                self.expected_seq_nums.setdefault(addr, 0)

                if packet['seq'] < self.expected_seq_nums[addr]:
                    ack_packet = packet['seq'].to_bytes(1, byteorder='big')
                    self.udp_socket.sendto(ack_packet, addr)
                    continue

                if packet['seq'] == self.expected_seq_nums[addr]:
                    if packet['data'] == b'':  # End of message packet
                        ack_packet = packet['seq'].to_bytes(1, byteorder='big')
                        self.udp_socket.sendto(ack_packet, addr)
                        break

                    received_data.append(packet['data'])
                    self.expected_seq_nums[addr] = (self.expected_seq_nums[addr] + 1) % 256
                    ack_packet = packet['seq'].to_bytes(1, byteorder='big')
                    self.udp_socket.sendto(ack_packet, addr)

            except socket.timeout:
                # If timeout, break the loop and return what has been received so far
                if received_data:
                    break
                else:
                    return None, None

        message = b''.join(received_data).decode('utf-8')
        return message, addr

    def close(self):
        self.udp_socket.close()
