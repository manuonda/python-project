class ClaseA():
    def say_hello(self):
        print("Hello, I'm an Alumno Class A ")
    ...

class ClaseB():
    def say_goodbye(self):
        print("Goodbye, I'm an Alumno Class B")

class ClaseC(ClaseA, ClaseB):
    ...


c  = ClaseC()
c.say_hello()
c.say_goodbye()
