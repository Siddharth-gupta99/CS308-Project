from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment, Lecture, Attendance
from .decorators import student_required, teacher_required
from django.contrib.auth.decorators import login_required

def home(request):

    if request.user.is_authenticated:
        if request.user.is_student:
            courses = Course.objects.all().values()
            enrolled = request.user.enrollments.values('course')
            courses = [item['name'] for item in courses]
            enrolled = [item['course'] for item in enrolled]
            courses = set(courses).difference(enrolled)
            # print(courses)
           # print(type(request.user.enrollments.values('course')), type(courses))
            return render(request, 'attendance/student_home.html', {'courses': courses})

    return render(request, 'base.html')

@login_required
@student_required
def my_courses(request):
    enrolled = request.user.enrollments.values('course')
    enrolled = [item['course'] for item in enrolled]
    return render(request, 'attendance/student_my_courses.html', {'courses': enrolled})

@login_required
@student_required
def student_course(request, course_name):
    course = get_object_or_404(Course, pk=course_name)
    enrolled = request.user.enrollments.values('course')
    is_enrolled =  course.name in [item['course'] for item in enrolled]
    # print(course, enrolled, is_enrolled)

    if not is_enrolled:
        if request.method == 'POST':
            user = request.user
            enrollment = Enrollment(student = user, course = course)
            enrollment.save()
            return redirect('student_course', course_name)

    return render(request, 'attendance/student_course.html', {'is_enrolled': is_enrolled, 'course': course})