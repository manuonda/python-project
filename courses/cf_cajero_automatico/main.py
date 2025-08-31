from school import  Teacher , Student, Course, Grade

teacher = Teacher(1000,"Idiomas", 1990)
teacher.email = "manuonda@gmail.com"
teacher.name =" david garcia"


print(teacher.email)
print(teacher.getBasicDetails())
print(f"El profesor se puede retirar :{teacher.canRetire()}")

student = Student("carla", "35899", "Activo")
student.name = "Luis"

print(student.getBasicDetails())

student = Student()
student.name = "Pedro"

course = Course(1,"Ingles","Tener libro de ingles 2", 6)

grade = Grade(1,5,student, course)
