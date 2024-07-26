import socket
from udp_rdt_server import UDPServer
from server_cmds import ServerCommands

def main():
    server = UDPServer(socket.AF_INET, socket.SOCK_DGRAM, ("localhost", 5000), 1024)
    server_commands = ServerCommands(server)

    while True:
        data, address = server.receive()
        command_parts = data.split()
        command = command_parts[0]


        if command == "login":
            username = command_parts[1]
            server_commands.handle_login(address, username)
        elif command == "logout":
            server_commands.handle_logout(address)
        elif command == "create":
            _, name, location, description = command_parts
            server_commands.handle_create_accommodation(address, name, location, description)
        elif command == "book":
            _, name, location, day = command_parts
            server_commands.handle_book_accommodation(address, name, location, day)
        elif command == "cancel":
            _, owner, name, location, day = command_parts
            server_commands.handle_cancel_reservation(address, owner, name, location, day)
        elif command == "list:myacmd":
            server_commands.handle_list_my_accommodations(address)
        elif command == "list:acmd":
            server_commands.handle_list_accommodations(address)
        elif command == "list:myrsv":
            server_commands.handle_list_my_reservations(address)

if __name__ == "__main__":
    main()
