class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self, username, password):
        if self.username == username and self.password == password:
            return True
        return False

class Admin(User):
    def __init__(self, username, password, email):
        super().__init__(username, password)
        self.rol = 'Admin'

    def login(self, username, password):
         if super().login(username, password):
             print("Login as Admin")
             return True
         return False
    
    
class Organizer(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.rol = 'Organizer'


admin = Admin('dgarcia', '123456','manuonda@gmail.com')
print("=== ADMIN ====")
print(admin.username)
print(admin.password)
print(admin.rol)
print(admin.login('dgarcia', '123456'))

organizer = Organizer('dgarcia2', '123456')
print("=== ORGANIZER ====")
print(organizer.username)
print(organizer.password)
print(organizer.rol)
print(organizer.login('dgarcia2', '123456'))