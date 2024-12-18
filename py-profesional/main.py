print("hola mundo")

"""
<variables> = <valor>
"""

name ="codigo facilito" #str

print(name)
print(type(name))

""" 
listas
"""
print("listas")
my_list = ["1",1,2,"info",[1,2,3]]
print(my_list)

"""
sub listas
"""
print("sub listas")
new_list = my_list[0:3]
print(new_list)

new_list_2=my_list[:4]
print(new_list_2)

courses_copy =  my_list[:]
print(courses_copy)

# [start:end:skip]
courses_copy_2 = my_list[::2]
print(courses_copy_2)

## list inverse
courses_copy_3 = my_list[::-1]
print(courses_copy_3)


courses = my_list[:]
# append 
print("method append")
courses.append("Ruby on rails")
print("add index")
#insert
courses.insert(1,"Java")
print(courses)

#extends: add other list
print("extend")
new_courses = ["ruby","python"]
courses.extend(new_courses)
print(courses)

print("Vue" in courses)
# print(
#     courses.index("Python")
# )


#courses.remove("Python")
#courses.pop() # ultimo elemento

copy_list = courses.copy();

# courses.reverse()
# courses.sort(reverse=True)


numbers = [1, 2, 3, 4, 5]  # Define a list of N integers
total_sum = sum(numbers)  # Calculate the sum of all elements
print("Sum of all elements:", total_sum)  # Print the sum

strings_list = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
sub_list = strings_list[:3] + strings_list[-3:]
print(sub_list)

matrix = [
    [2, 5, 7],
    [4, 8, 6],
    [10, 3, 1]
]

# Check if the first element of each row is even
result = all(row[0] % 2 == 0 for row in matrix)
print(result)

print("tuplas ")
courses_tuples = (
    "python","java","c","c++"
)

# _ omite los valores
var1, _ ,var3,var4 =  courses_tuples
print(
    var1,var3,var4
)


var_python,var_java, *sub_courses = courses_tuples
print(sub_courses)

#zip : une diferentes valores
print("zip")
users = ["user1","user2","user3"]
courses = ("Python","Django","Rails")

response = zip(users,courses)
print(list(response))

print("functios tuples")
numbers = (
    1,2,3,4,5,33,7,2,10
)

print(len(numbers))

print(
    sorted(numbers, reverse=True) #list default(asc)
)

print(numbers.count(5))

my_tuple=(1,2,3)

print(my_tuple[2])

my_tuple=(1,2,3,4,5)

first, *_, penultimate, last = my_tuple 

print(first)

print(penultimate)

print(last)

my_tuple=(1,2,3,4,5)

first, *_, penultimate, last = my_tuple

print(first)
print(penultimate)
print(last)

lista = [1,2,3,4,5,6,7,8,9,10]
pares = tuple(num for num in lista if num % 2 == 0 )

print(pares)

message = 'Hola mundo'
print(message)
print(type(message))
print(len(message))

print('?' in message)
#print(message.index('!'))
#print(message[-3 ])

message2= message[1:]
print(message2)

courses_strings = "Pytho, Java, Ruby, C++"
messages_courses = courses_strings.split(',')
messages_courses2 = ','.join(messages_courses)

print(messages_courses)
print(messages_courses2)
name = 'Eduardo'
last_name = 'Garcia'

full_name = name + ' ' + last_name
print(full_name)

full_name_2 = ' '.join([name, last_name])
print(full_name_2)

full_name_3 = name + ' ' + full_name + str(30)
print(full_name_3)

print("format")
base = 'El nombre complet es : {} {} . Su edad es {}'
full_name_format = base.format(name, last_name, 30)
print(full_name_format)

base_format_2 = 'El nombre completo es : {name} {last_name}'
full_name_format_2 = base_format_2.format(
    name=name,
    last_name=last_name
)
print(full_name_format_2)

full_name_withf = f'El nombre completo es : {name} {full_name}'
print(full_name_withf)

print( 'curso' in full_name)

print( full_name.count('Python'))

print(full_name.startswith('david'))

name="radar"
print(name == name[::-1])

name='Python Profesional'
formatted_name = name.capitalize()
print(formatted_name)

vowels = 'aeiouAEIOU'
print(name[0] in vowels or name[-1] in vowels)

name, age, course = 'Cody', 12, 'Python'
print(f'{name}-{age}-{course}')