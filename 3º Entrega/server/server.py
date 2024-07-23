import socket
from udp_rdt import RDT
from server_cmds import ServerCommands

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 5000))
    rdt = RDT(server_socket)
    server_commands = ServerCommands(rdt)

    while True:
        data, address = rdt.receive()
        command_parts = data.decode().split()
        command = command_parts[0]
        
        username = command_parts[1] if len(command_parts) > 1 else None

        if command == "login":
            server_commands.handle_login(address, username)
        elif command == "logout":
            server_commands.handle_logout(address, username)
        elif command == "create":
            _, name, location, description = command_parts
            server_commands.handle_create_accommodation(address, username, name, location, description)
        elif command == "book":
            _, owner, name, location, day, room = command_parts
            server_commands.handle_book_accommodation(address, username, owner, name, location, day, room)
        elif command == "cancel":
            _, owner, name, location, day = command_parts
            server_commands.handle_cancel_reservation(address, username, owner, name, location, day)
        elif command == "list:myacmd":
            server_commands.handle_list_my_accommodations(address, username)
        elif command == "list:acmd":
            server_commands.handle_list_accommodations(address)
        elif command == "list:myrsv":
            server_commands.handle_list_my_reservations(address, username)

if __name__ == "__main__":
    main()
