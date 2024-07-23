class ClientCommands:
    def __init__(self, rdt, username, address):
        self.rdt = rdt
        self.username = username
        self.address = address

    def login(self):
        command = f"login {self.username}"
        self.rdt.send(command.encode(), self.address)

    def logout(self):
        command = "logout"
        self.rdt.send(command.encode(), self.address)

    def list_my_accommodations(self):
        command = "list:myacmd"
        self.rdt.send(command.encode(), self.address)

    def list_accommodations(self):
        command = "list:acmd"
        self.rdt.send(command.encode(), self.address)

    def list_my_reservations(self):
        command = "list:myrsv"
        self.rdt.send(command.encode(), self.address)

    def create_accommodation(self, name, location, description):
        command = f"create {name} {location} {description}"
        self.rdt.send(command.encode(), self.address)

    def book_accommodation(self, owner, name, location, day, room):
        command = f"book {owner} {name} {location} {day} {room}"
        self.rdt.send(command.encode(), self.address)

    def cancel_reservation(self, owner, name, location, day):
        command = f"cancel {owner} {name} {location} {day}"
        self.rdt.send(command.encode(), self.address)
