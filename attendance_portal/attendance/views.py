from django.shortcuts import render
from .models import Course, Enrollment, Lecture, Attendance

def home(request):

    if request.user.is_authenticated:
        if request.user.is_student:
            courses = Course.objects.all()
            print(request.user.enrollments.values('course'))
            return render(request, 'attendance/student_home.html', {'courses': courses})

    return render(request, 'base.html')
