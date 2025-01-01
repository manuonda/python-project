def say_hello():
    print("hola mindo")


def count_to(number):
    for i in range(1,number):
        print(i)

def multiply(number1, number2):
    result = number1 * number2
    print(f'El resultaod es {result}')

def full_name(first_name , last_name):
    full_name = first_name + last_name
    print(f'El full_name es : {full_name}')

count_to(10)
multiply(1,2)
full_name('David','Garcia')


def foo():
    return 1, 'david garcia',45


print(type(foo()))
numero, nombre, edad = foo()
print(numero, nombre, edad)

def calculate_total(price, tax = 0.0 , discount = 0):
    total = price + (price * tax) - discount
    return total

total = calculate_total(100,0.0,10)
print(total)

total = calculate_total(23,3)
print(total)


def show_info(username, email, *scopes):
    print(username)
    print(email)

    average = sum(scopes) /len(scopes)
    print(average)

show_info(
    "cody","manuonda@gmail.com",
    10,10,10,23
)


""" lambda parametros <body> siempre retorn un valor """
add = lambda numero1 , numero2=0: numero1+numero2 # return
print(add(10))
print(add(numero1 = 10, numero2=20))

suma = lambda *args: sum(args)

print(suma(1,2,3,4,5,6))

def handle_operation(callback, *args, **kwargs):
    print("function de orden superior")
    result = callback(*args,**kwargs)
    print(result)


def add(a,b):
    return a+b

handle_operation(add,5,3)


def factory_operation(option):
    def deposit(balance, amount=0):
        return balance + amount
    
    def withdraw(balance, amount=0):
        if amount > balance:
            return None
        
        return balance - amount

    default = lambda *args, **kwargs: '>>> Lo sentimos, opcion No valida'

    if option == 'deposit':
        return deposit
    elif option == 'withdraw':
         return withdraw 
    else:
        return default
    
option = input('Ingresa una opcion')
func = factory_operation(option)

print(func(100,20))
print(type(func))

#Closures
def multiply(number1):
    def operation(number2):
        return number1 * number2
    return operation
    
func_operation = multiply(10)
print('El resultado es: ')
result = func_operation(3)
print(result)

def my_decorator(func):
    def wrapper(*args,**kwargs):
        print("Algo se esta haciendo antes de la funcion")
        result = func(*args,**kwargs)
        print("Algo se esta haciendo despues de la funcion")
        return result
    return wrapper


@my_decorator
def say_hello():
    print("Hola mundo!")

say_hello()


@my_decorator
def suma(numer1, number2):
    return numer1 + number2

print(suma(10,20))


def full_name(first_name, last_name):
    """ Permite generar un nombre completo 
        Args:
           - first_name (String)
           - last_name  (String)

        Return:
           String
    """
    return f"{first_name}{last_name}"

print(
    full_name.__doc__
)


def palindromo(sentence):
    """ Permite conocer si un String es o no un palindromo
     
       Args:
        - sentence (String) 

        Return 
         - bool

        Examples:
        >>> palindromo('oso')
        True

        >>> palindromo('hello')
        False

    """

    sentence = sentence.lower().replace(' ','')
    return sentence == sentence[::-1]
