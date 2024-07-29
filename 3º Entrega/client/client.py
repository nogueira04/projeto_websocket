import threading
import socket
import time
from udp_rdt_client import UDPClient
from client_cmds import ClientCommands

print_lock = threading.Lock()
receive_lock = threading.Lock()

def receive_messages(client):
    while True:
        try:
            with receive_lock: 
                message, _ = client.receive()

            if message is not None:
                with print_lock: 
                    print(f"\n{message}\nInsira o comando: ", end="")
            time.sleep(0.1)
        except Exception as e:
            with print_lock:  
                print(f"Erro ao receber mensagem: {e}")
            break

def main():
    server_address = ("localhost", 5000)
    client = UDPClient(socket.AF_INET, socket.SOCK_DGRAM, ('localhost', 0), 1024)
    
    while True:
        username = input("Insira o nome de usuário: ").strip()
        if username:
            break

    client_commands = ClientCommands(client, username, server_address)

    receiver_thread = threading.Thread(target=receive_messages, args=(client,))
    receiver_thread.daemon = True # Termina a thread quando o programa principal termina
    receiver_thread.start()

    while True:
        command = input("Insira o comando: ").strip()
        if not command:
            continue

        with print_lock: 
            with receive_lock:
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
                        client_commands.cancel_reservation(name, location, day)
                    except ValueError:
                        print("Uso correto: cancel <nome> <local> <dia>")
                else:
                    print("Comando inválido.")

if __name__ == "__main__":
    main()
