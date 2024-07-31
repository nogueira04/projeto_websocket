import datetime
import time

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
        
        self.rdt.send(response.encode(), address)
        print(f"Resposta enviada para {address}: {response}")

    def handle_logout(self, address):
        print(f"Tentativa de logout: address={address}")
        if address in self.users:
            username = self.users[address]
            del self.users[address]
            response = "Você saiu do sistema!"
            print(f"Sucesso no logout: {username} foi removido.")
        else:
            response = "Erro: Usuário não está logado."
            print(f"Falha no logout: {response}")
        
        self.rdt.send(response.encode(), address)
        print(f"Resposta enviada para {address}: {response}")

    def handle_create_accommodation(self, address, name, location, id):
        username = self.users.get(address)
        print(f"Tentativa de criação de acomodação: username={username}, address={address}, name={name}, location={location}, id={id}")
        key = (name, location)
        if key in self.accommodations:
            response = "Acomodação já existente!"
            print(f"Falha na criação: {response}")
        else:
            accommodation_id = f"{name}_{location}_{username}"
            start_date = datetime.datetime.strptime("17/07/2024", "%d/%m/%Y")
            end_date = datetime.datetime.strptime("22/07/2024", "%d/%m/%Y")
            availability = {start_date + datetime.timedelta(days=x) for x in range((end_date - start_date).days + 1)}
            not_available = {}
            self.accommodations[key] = {"address":address, "id": accommodation_id, "description": id, "owner": username, "availability": availability, "not_available":not_available}
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
                    self.accommodations[key]["not_available"][date] = address
                    self.reservations[(name, location, day)] = username
                    response = f"Reserva confirmada para {username} em acomodação de ID {self.accommodations[key]['description']} no dia {day}."
                    print(f"Sucesso na reserva: {response}")
                    owner_address = next((addr for addr, user in self.users.items() if user == self.accommodations[key]["owner"]), None)
                    if owner_address:
                        self.rdt.send(f"[{username}/{address}] Reserva confirmada: {username} na acomodação de ID {self.accommodations[key]['description']} no dia {day}".encode(), owner_address)
        
        self.rdt.send(response.encode(), address)
        print(f"Resposta enviada para {address}: {response}")

    def handle_cancel_reservation(self, address, name, location, day):
        username = self.users.get(address)
        print(f"Tentativa de cancelamento de reserva: username={username}, address={address}, name={name}, location={location}, day={day}")
        if not username:
            response = "Erro: Usuário não está logado."
            self.rdt.send(response.encode(), address)
            print(f"Falha no cancelamento: {response}")
            return

        key = (name, location)
        if key not in self.accommodations:
            response = "Acomodação não encontrada!"
            self.rdt.send(response.encode(), address)
            print(f"Falha no cancelamento: {response}")
            return

        reservation_key = (name, location, day)
        if reservation_key not in self.reservations:
            response = "Reserva não encontrada!"
            self.rdt.send(response.encode(), address)
            print(f"Falha no cancelamento: {response}")
            return

        if self.reservations[reservation_key] != username:
            response = "Você só pode cancelar suas próprias reservas."
            self.rdt.send(response.encode(), address)
            print(f"Falha no cancelamento: {response}")
            return

        date = datetime.datetime.strptime(day, "%d/%m/%Y")
        self.accommodations[key]["availability"].add(date)
        del self.accommodations[key]["not_available"][date]
        del self.reservations[reservation_key]

        response = f"Reserva cancelada para {name} em {location} no dia {day}."
        self.rdt.send(response.encode(), address)
        print(f"Sucesso no cancelamento: {response}")

        owner_address = next((addr for addr, user in self.users.items() if user == self.accommodations[key]["owner"]), None)
        if owner_address:
            self.rdt.send(f"[{username}/{address}] Reserva cancelada: {username} cancelou a reserva na acomodação {name} em {location} no dia {day}".encode(), owner_address)


    
    def handle_list_my_accommodations(self, address):
        username = self.users.get(address)
        if not username:
            response = "Erro: Usuário não está logado."
            self.rdt.send(response.encode(), address)
            return

        user_accommodations = [acmd for acmd in self.accommodations.values() if acmd["owner"] == username]
        if not user_accommodations:
            response = "Você não tem acomodações."
            self.rdt.send(response.encode(), address)
            return

        response = ["Suas acomodações:"]
        for acmd in user_accommodations:
            acmd_info = f"Nome: {acmd['id'].split('_')[0]}, Localização: {acmd['id'].split('_')[1]}"

            available_days = sorted(acmd['availability'])
            available_days_str = [date.strftime("%d/%m/%Y") for date in available_days]

            reserved_days_str = []
            for date, addr in acmd['not_available'].items():
                reservation_key = (acmd['id'].split('_')[0], acmd['id'].split('_')[1], date.strftime('%d/%m/%Y'))
                if reservation_key in self.reservations:
                    reserver = self.reservations[reservation_key]
                    reserved_days_str.append(f"{date.strftime('%d/%m/%Y')} - Reservado por {reserver} ({addr[0]}:{addr[1]})")

            acmd_info += "\nID da acomodação: {}".format(acmd['description'])
            acmd_info += "\n  Dias disponíveis:\n  {}".format('\n  '.join(available_days_str))
            acmd_info += "\n  Dias indisponíveis:\n  {}".format('\n  '.join(reserved_days_str) if reserved_days_str else "Nenhum.")
            response.append(acmd_info)

        response = "\n\n".join(response)
        self.rdt.send(response.encode(), address)
        print(f"Resposta enviada para {address}: {response}")
        
    def handle_list_accommodations(self, address):
        username = self.users.get(address)
        if not username:
            response = "Erro: Usuário não está logado."
            self.rdt.send(response.encode(), address)
            return

        if not self.accommodations:
            response = "Nenhuma acomodação disponível."
            self.rdt.send(response.encode(), address)
            return

        response = ["Acomodações disponíveis:"]
        for acmd in self.accommodations.values():
            acmd_info = f"Nome: {acmd['id'].split('_')[0]}, Localização: {acmd['id'].split('_')[1]}"
            
            available_days = sorted(acmd['availability'])
            available_days_str = sorted(date.strftime("%d/%m/%Y") for date in available_days)

            # Encontrar dias reservados
            reserved_days = []
            for date in available_days:
                date_str = date.strftime('%d/%m/%Y')
                if (acmd['owner'], acmd['id'].split('_')[0], acmd['id'].split('_')[1], date_str) in self.reservations:
                    reserved_days.append(f"{date_str} ({self.reservations[(acmd['owner'], acmd['id'].split('_')[0], acmd['id'].split('_')[1], date_str)]})")

            # Remover dias reservados dos dias disponíveis
            available_days_str = [d for d in available_days_str if d not in [r.split(' ')[0] for r in reserved_days]]

            acmd_info += f"\nID da acomodação: {acmd['description']}"
            acmd_info += f"\nOfertante: {acmd['owner']}"
            acmd_info += "\n  Dias disponíveis:\n  {}".format('\n  '.join(available_days_str))
            response.append(acmd_info)

        response = "\n\n".join(response)
        self.rdt.send(response.encode(), address)

    def handle_list_my_reservations(self, address):
        username = self.users.get(address)
        if not username:
            response = "Erro: Usuário não está logado."
            self.rdt.send(response.encode(), address)
            return

        user_reservations = [
            (name, location, day)
            for (name, location, day), reserv_username in self.reservations.items()
            if reserv_username == username
        ]

        if not user_reservations:
            response = "Você não tem reservas."
            self.rdt.send(response.encode(), address)
            return

        response = ["Suas reservas:"]
        for name, location, day in user_reservations:
            acmd_key = (name, location)
            if acmd_key in self.accommodations:
                acmd = self.accommodations[acmd_key]
                owner = acmd['owner']
                owner_address = acmd['address']
                message = f">>> {name} em {location} no dia {day} (Ofertante: {owner} / {owner_address[0]}:{owner_address[1]})"
                response.append(message)

        response = "\n".join(response)
        self.rdt.send(response.encode(), address)
        print(f"Resposta enviada para {address}: {response}")

    def broadcast(self, message, exclude=None):
        print(f"Broadcasting message: '{message}' to all users except {exclude}")
        for user_address in self.users:
            if user_address != exclude:
                try:
                    print(f"Sending message to {user_address}")
                    self.rdt.send(message.encode(), user_address)
                    print(f"Message sent to {user_address}")
                except Exception as e:
                    print(f"Failed to send message to {user_address}: {e}")

