# {} clave: valor  => key:value
# String , tuplas, int, float, booleans : inumtables objects
# keys, values, items
user = {
    'name':'User1',
    'age':10,
    'courses':[
        "Python","Java","Django","Redis"
    ]
}

print(user)

user_name = user.get('name')
print(user_name)
user['last_name'] = 'information'
print(user_name)

print(user.keys())
print(list(user.keys()))
print(list(user.values()))
print(user.items())

print(tuple(user.keys()))

## actualizacion dictionarys
user.update({
    'name':'codigo',
    'last_name':0,
    'numero':23
})
print(user)

del user['name']
print(user)

user.clear()
print(user)


my_dictionary = {'name':  'Cody', 'age': 12, 'course': 'python'}
keys_string = '-'.join(my_dictionary.keys())
print(keys_string)