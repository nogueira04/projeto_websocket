import socket
from udp_rdt import RDT
from client_cmds import ClientCommands

def main():
    username = input("Insira seu nome: ")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 5000)
    rdt = RDT(client_socket)
    client_commands = ClientCommands(rdt, username, server_address)

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
            _, owner, name, location, day, room = command.split(' ', 5)
            client_commands.book_accommodation(owner, name, location, day, room)
        elif command.startswith("cancel"):
            _, owner, name, location, day = command.split(' ', 4)
            client_commands.cancel_reservation(owner, name, location, day)
        else:
            print("Comando inválido.")

if __name__ == "__main__":
    main()
