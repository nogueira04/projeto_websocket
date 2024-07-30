class ClientCommands:
    def __init__(self, rdt, username, address):
        self.rdt = rdt
        self.username = username
        self.address = address
        self.logged_in = False

    def login(self):
        command = f"login {self.username}"
        self.rdt.send(command, self.address)
        response, _ = self.rdt.receive()
        if response is not None:
            print(response)
            if "online" in response:
                self.logged_in = True  # Marca o cliente como logado
        
        return self.logged_in

    def logout(self):
        if not self.logged_in:
            print("Você não está logado.")
            return
        command = f"logout {self.username}"
        self.rdt.send(command, self.address)
        response, _ = self.rdt.receive()
        if response is not None:
            print(response)
            self.logged_in = False  # Marca o cliente como deslogado

    def list_my_accommodations(self):
        command = "list:myacmd"
        self.rdt.send(command, self.address)
        response, _ = self.rdt.receive()
        if response is not None:
            print(response)

    def list_accommodations(self):
        command = "list:acmd"
        self.rdt.send(command, self.address)
        response, _ = self.rdt.receive()
        if response is not None:
            print(response)

    def list_my_reservations(self):
        command = "list:myrsv"
        self.rdt.send(command, self.address)
        response, _ = self.rdt.receive()
        if response is not None:
            print(response)

    def create_accommodation(self, name, location, description):
        if not self.logged_in:
            print("Você precisa estar logado para criar uma acomodação.")
            return
        command = f"create {name} {location} {description}"
        self.rdt.send(command, self.address)
        response, _ = self.rdt.receive()
        if response is not None:
            print(response)

    def book_accommodation(self, name, location, day):
        command = f"book {name} {location} {day}"
        self.rdt.send(command, self.address)
        response, _ = self.rdt.receive()
        if response is not None:
            print(response)

    def cancel_reservation(self, name, location, day):
        command = f"cancel {name} {location} {day}"
        self.rdt.send(command, self.address)
        response, _ = self.rdt.receive()
        if response is not None:
            print(response)
