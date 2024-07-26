import datetime

class ServerCommands:
    def __init__(self, rdt):
        self.rdt = rdt
        self.users = {}  # {address: username}
        self.accommodations = {}  # {(name, location): {"id": id, "description": description, "owner": username, "availability": set(dates)}}
        self.reservations = {}  # {("owner, name, location, day): username}

    def handle_login(self, address, username):
        print(f"Tentativa de login: username={username}, address={address}")
        if address in self.users:
            response = "Usuário já está logado!"
            print(f"Falha no login: {response}")
        elif username in self.users.values():
            response = "Nome de usuário já está em uso!"
            print(f"Falha no login: {response}")
        else:
            self.users[address] = username
            response = "Você está online!"
            print(f"Sucesso no login: {username} foi adicionado com o endereço {address}")
            self.broadcast(f"[{username}/{address}] entrou no sistema.", exclude=address)
        
        self.rdt.send(response.encode(), address)
        print(f"Resposta enviada para {address}: {response}")

    def handle_logout(self, address):
        print(f"Tentativa de logout: address={address}")
        if address in self.users:
            username = self.users[address]
            del self.users[address]
            response = "Você saiu do sistema!"
            print(f"Sucesso no logout: {username} foi removido.")
            self.broadcast(f"[{username}/{address}] saiu do sistema.", exclude=address)
        else:
            response = "Erro: Usuário não está logado."
            print(f"Falha no logout: {response}")
        
        self.rdt.send(response.encode(), address)
        print(f"Resposta enviada para {address}: {response}")

    def handle_create_accommodation(self, address, name, location, description):
        username = self.users.get(address)
        print(f"Tentativa de criação de acomodação: username={username}, address={address}, name={name}, location={location}, description={description}")
        key = (name, location)
        if key in self.accommodations:
            response = "Acomodação já existente!"
            print(f"Falha na criação: {response}")
        else:
            accommodation_id = f"{name}_{location}_{username}"
            start_date = datetime.datetime.strptime("17/07/2024", "%d/%m/%Y")
            end_date = datetime.datetime.strptime("22/07/2024", "%d/%m/%Y")
            availability = {start_date + datetime.timedelta(days=x) for x in range((end_date - start_date).days + 1)}
            self.accommodations[key] = {"id": accommodation_id, "description": description, "owner": username, "availability": availability}
            response = f"Acomodação de nome {name} criada com sucesso!"
            print(f"Sucesso na criação: {response}")
            self.broadcast(f"[{username}/{address}] Nova acomodação: {name} em {location}", exclude=address)
        
        self.rdt.send(response.encode(), address)
        print(f"Resposta enviada para {address}: {response}")

    def handle_book_accommodation(self, address, name, location, day):
        username = self.users.get(address)
        print(f"Tentativa de reserva: username={username}, address={address}, name={name}, location={location}, day={day}")
        key = (name, location)
        if key not in self.accommodations:
            response = "Acomodação não encontrada!"
            print(f"Falha na reserva: {response}")
        else:
            if username == self.accommodations[key]["owner"]:
                response = "Você não pode reservar suas próprias acomodações."
                print(f"Falha na reserva: {response}")
            else:
                date = datetime.datetime.strptime(day, "%d/%m/%Y")
                print(self.accommodations[key]["availability"])
                if date not in self.accommodations[key]["availability"]:
                    response = "Dia indisponível para reserva."
                    print(f"Falha na reserva: {response}")
                else:
                    self.accommodations[key]["availability"].remove(date)
                    print(self.accommodations[key]["availability"])
                    self.reservations[(name, location, day)] = username
                    response = f"Reserva confirmada para {name} em {location} no dia {day}."
                    print(f"Sucesso na reserva: {response}")
                    owner_address = next((addr for addr, user in self.users.items() if user == self.accommodations[key]["owner"]), None)
                    if owner_address:
                        self.rdt.send(f"[{username}/{address}] Reserva confirmada: {name} em {location} no dia {day}".encode(), owner_address)
        
        self.rdt.send(response.encode(), address)
        print(f"Resposta enviada para {address}: {response}")

    def handle_cancel_reservation(self, address, owner, name, location, day):
        pass

    def handle_list_my_accommodations(self, address):
        pass

    def handle_list_accommodations(self, address):
        pass

    def handle_list_my_reservations(self, address):
        pass

    def broadcast(self, message, exclude=None):
        for user_address in self.users:
            if user_address != exclude:
                self.rdt.send(message.encode(), user_address)
