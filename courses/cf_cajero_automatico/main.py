from school import  Teacher , Student, Course, Grade
from post import PostRepository, Post

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
repo = PostRepository()
repo.add(Post(0, "Title one","Java es un lenguaje de programacion"))
repo.add(Post(1, "Java","Java is good"))
all_post = repo.get_all();
print(f"Total posts : {len(all_post)}")

updated_post = Post(1, "Titulo actualizado ","Contenido actualizado")
repo.update(1, updated_post)

#eleiminar post 
repo.delete(2)