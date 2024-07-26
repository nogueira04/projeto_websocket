class ServerCommands:
    def __init__(self, rdt):
        self.rdt = rdt
        self.users = {}  
        self.accommodations = {}  

    def handle_login(self, address, username):
        if username in self.users:
            response = "Nome de usuário já está em uso!"
        else:
            self.users[username] = address
            response = "Você está online!"
            self.broadcast(f"[{username}/{address}] entrou no sistema.", exclude=address)
        self.rdt.send(response, address)

    def handle_logout(self, address, username):
        if username in self.users and self.users[username] == address:
            del self.users[username]
            response = "Você saiu do sistema!"
            self.broadcast(f"[{username}/{address}] saiu do sistema.", exclude=address)
        else:
            response = "Erro ao fazer logout!"
        self.rdt.send(response, address)

    def handle_create_accommodation(self, address, username, name, location, description):
        key = (name, location)
        if key in self.accommodations:
            response = "Acomodação já existente!"
        else:
            self.accommodations[key] = description
            print(f"Usuário {username} criou acomodação {name} em {location}")
            response = f"Acomodação de nome {name} criada com sucesso!"
            self.broadcast(f"[{username}/{address}] Nova acomodação: {name} em {location}", exclude=address)
        self.rdt.send(response.encode(), address)

    def handle_book_accommodation(self, address, username, owner, name, location, day, room):
        pass

    def handle_cancel_reservation(self, address, username, owner, name, location, day):
        pass

    def handle_list_my_accommodations(self, address, username):
        pass

    def handle_list_accommodations(self, address):
        pass

    def handle_list_my_reservations(self, address, username):
        pass

    def broadcast(self, message, exclude=None):
        for user, user_address in self.users.items():
            if user_address != exclude:
                self.rdt.send(message.encode(), user_address)
