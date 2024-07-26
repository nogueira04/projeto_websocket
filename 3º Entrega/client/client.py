import socket
from udp_rdt_client import UDPClient
from client_cmds import ClientCommands

def main():
    server_address = ("localhost", 5000)
    client = UDPClient(socket.AF_INET, socket.SOCK_DGRAM, ('localhost', 0), 1024)
    username = input("Insira o nome de usuário: ")
    client_commands = ClientCommands(client, username, server_address)

    while True:
        command = input("Insira o comando: ")
        if command == "login":
            client_commands.login()
        elif command == "logout":
            client_commands.logout()
        elif command == "list:myacmd":
            client_commands.list_my_accommodations()
        elif command == "list:acmd":
            client_commands.list_accommodations()
        elif command == "list:myrsv":
            client_commands.list_my_reservations()
        elif command.startswith("create"):
            _, name, location, description = command.split(' ', 3)
            client_commands.create_accommodation(name, location, description)
        elif command.startswith("book"):
            _, name, location, day = command.split(' ', 3)
            client_commands.book_accommodation(name, location, day)
        elif command.startswith("cancel"):
            _, owner, name, location, day = command.split(' ', 4)
            client_commands.cancel_reservation(owner, name, location, day)
        else:
            print("Comando inválido.")

if __name__ == "__main__":
    main()
