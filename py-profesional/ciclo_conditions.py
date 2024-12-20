user = None #Null - Nil
print(user)

### if
number1 = 20
number2 = 30 
if number1 == number2 : 
    print("La condicion es true")
elif number1 > number2:
    print("number1 > number2")
else:
    print("no es correct conditions")


match number1 :
    case 10 : print("hola 10")
    case 11 : print("")
    case _ : print("default valuel ")


numbers = [1,2,3,4,5,6]
for i in numbers:
    print(i)


user = {
    'name':'DAVID',
    'last_name':'Garcia',
    'age':23
}

for key, value in user.items():
    print("La llave : ", key, " value : ", value)

number1=1 
while number1 < 10 : 
    number1 +=1
    print(number1)

var  = None 
if var == None:
    pass