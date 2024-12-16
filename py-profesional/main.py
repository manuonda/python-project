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
print(
    courses.index("Python")
)


courses.remove("Python")
courses.pop() # ultimo elemento

copy_list = courses.copy();

courses.reverse()
courses.sort(reverse=True)


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