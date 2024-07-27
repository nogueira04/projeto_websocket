import socket
from udp_rdt_client import UDPClient
from client_cmds import ClientCommands

def main():
    server_address = ("localhost", 5000)
    client = UDPClient(socket.AF_INET, socket.SOCK_DGRAM, ('localhost', 0), 1024)
    
    while True:
        username = input("Insira o nome de usuário: ").strip()
        if username:
            break

    client_commands = ClientCommands(client, username, server_address)

    while True:
        command = input("Insira o comando: ").strip()
        if not command:
            continue

        if command == "login":
            client_commands.login()
        elif command == "logout":
            client_commands.logout()
            # Solicitar novamente o nome de usuário após o logout
            while True:
                username = input("Insira o nome de usuário: ").strip()
                if username:
                    break
            client_commands.username = username
        elif command == "list:myacmd":
            client_commands.list_my_accommodations()
        elif command == "list:acmd":
            client_commands.list_accommodations()
        elif command == "list:myrsv":
            client_commands.list_my_reservations()
        elif command.startswith("create"):
            try:
                _, name, location, description = command.split(' ', 3)
                client_commands.create_accommodation(name, location, description)
            except ValueError:
                print("Uso correto: create <nome> <local> <descrição>")
        elif command.startswith("book"):
            try:
                _, name, location, day = command.split(' ', 3)
                client_commands.book_accommodation(name, location, day)
            except ValueError:
                print("Uso correto: book <nome> <local> <dia>")
        elif command.startswith("cancel"):
            try:
                _, owner, name, location, day = command.split(' ', 4)
                client_commands.cancel_reservation(owner, name, location, day)
            except ValueError:
                print("Uso correto: cancel <dono> <nome> <local> <dia>")
        else:
            print("Comando inválido.")

if __name__ == "__main__":
    main()
