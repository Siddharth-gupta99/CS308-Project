from accounts.models import User
from attendance.models import Course, Enrollment

users = [
    {'username':'Rohit', 'password':'Rohitpassword', 'name':'Rohit', 'is_student': True, 'is_teacher': False},
    {'username':'Siddharth', 'password':'Siddharthpassword', 'name':'Siddharth', 'is_student': True, 'is_teacher': False},
    {'username':'Shreyansh', 'password':'Shreyanshpassword', 'name':'Shreyansh', 'is_student': True, 'is_teacher': False},
    {'username':'B17059', 'password':'B17059password', 'name':'Saurabh', 'is_student': True, 'is_teacher': False},
    {'username':'teacher1', 'password':'teacher1password', 'name':'Teacher 1', 'is_student': False, 'is_teacher': True},    
    {'username':'teacher2', 'password':'teacher2password', 'name':'Teacher 2', 'is_student': False, 'is_teacher': True},    
]

numUsers = len(users)

for i in range(numUsers):
    user = User.objects.create_user(users[i]['username'], password=users[i]['password'], first_name=users[i]['name'])
    user.is_superuser = False
    user.is_staff = False
    user.is_student = users[i]['is_student']
    user.is_teacher = users[i]['is_teacher']
    user.save()



numCourses = 5
teacher = User.objects.all().filter(is_teacher=True)[0]

for i in range(numCourses):
    course = Course(name='IC10' + str(i), teacher=teacher)
    course.save()

course = Course.objects.all()[0]
students = User.objects.all().filter(is_student=True)
numStudents = len(students)

for i in range(numStudents):
    enrollment = Enrollment(course=course, student=students[i])
    enrollment.save()
