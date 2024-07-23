class ServerCommands:
    def __init__(self, rdt):
        self.rdt = rdt
        self.users = {}  
        self.accommodations = {}  

    def handle_login(self, address, username):
        pass

    def handle_logout(self, address, username):
        pass

    def handle_create_accommodation(self, address, username, name, location, description):
        pass

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
        pass
