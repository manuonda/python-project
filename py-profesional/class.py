class Alumno:
    def __init__(self, username, password, email, rol = 'Organizer'): 
        self.username = username
        self.password = password
        self.email = email
        self._direction ='Direction one'
        self.__directionTwo = 'Direction two'
    
        self.rol = rol

    # def say_hello(self):
    #     print("Hello, I'm an Alumno")

    @property
    def password(self): # Lectura
        if self.rol == 'Admin':
            return self.__password
        return None
    
    @password.setter  ## Escritura
    def password(self, value):
        if self.rol == 'Admin':
           self.__password = value
    


    def login(self, username, password):
        print(self.username)
        print(self.password)
        if self.username == username and self.password == password:
            self.say_hello()
            return True
        return False

alumno = Alumno('dgarcia','123456','manuonda@gmail.com')
print(alumno.username)
print(alumno.password)
print(alumno.email)

# add dynamic attributes
alumno.edad = 30
print(alumno.edad)
print(alumno.say_hello())

alumno.login('dgarcia','123456')

print(alumno._direction)
print(alumno._Alumno__directionTwo)

alumno.password = 'New Password!!'