from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment, Lecture, Attendance
from .decorators import student_required, teacher_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import NewLectureForm, QueryForm
from accounts.models import User


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
        
        if request.user.is_teacher:
           courses = Course.objects.all().filter(teacher = request.user)
           return render(request, 'attendance/teachers_home.html', {'courses': courses})

    return render(request, 'base.html')

@login_required
@teacher_required
def course_schedule(request, course_name):
    course = get_object_or_404(Course, name=course_name)
    
    if (request.user != course.teacher):
        raise PermissionDenied

    if request.method == 'POST':
        post = request.POST.copy()
        d = request.POST['time']
        d = d.replace("T", " ")
        d = d + ":00"
        post['time'] = d;
        form = NewLectureForm(post) 

        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.course = course
            lecture.save()
            return redirect('home')

    else:
        form = NewLectureForm()

    return render(request, 'attendance/new_lecture.html', {'form': form, 'course': course})            

def attendance_query(request, form, course):
    students = course.enrollments.values('student')
    lectures = course.lectures.all()
    total = len(lectures)
    attendances = []
    form = form.__dict__

    for student_ in students:
        student = get_object_or_404(User, pk=student_['student'])
        total_attended = 0

        for lecture in lectures:
            attended = Attendance.objects.filter(lecture=lecture).filter(student=student).exists()

            if attended:
                total_attended += 1

        if (total > 0):
            total_attended /= total
            total_attended *= 100
        else:    
            total_attended = 100    

        if((form['cleaned_data']['category'] == '1') and (total_attended >= form['cleaned_data']['attendance'])):
            attendances.append({
                'student': student.first_name,
                'percent': total_attended,
                'student_pk': student.pk
            }) 

        if((form['cleaned_data']['category'] == '2') and (total_attended <= form['cleaned_data']['attendance'])):
            attendances.append({
                'student': student.first_name,
                'percent': total_attended,
                'student_pk': student.pk
            })            

    return render(request, 'attendance/attendance_query.html', {'form': form, 'course': course, 'attendances': attendances})            

@login_required
@teacher_required
def teacher_course(request, course_name):
    course = get_object_or_404(Course, name=course_name)
    
    if (request.user != course.teacher):
        raise PermissionDenied

    if request.method == 'POST':
        form = QueryForm(request.POST)

        if form.is_valid():
            return attendance_query(request, form, course)
    else:
        form = QueryForm(initial={'category': '2'})        

    return render(request, 'attendance/teacher_course.html', {'course': course, 'form': form})   

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
    lectures = []
    attendance_per = 1

    if not is_enrolled:
        if request.method == 'POST':
            user = request.user
            enrollment = Enrollment(student = user, course = course)
            enrollment.save()
            return redirect('student_course', course_name)

    else:
        alllectures = Lecture.objects.filter(course=course).order_by('time')  
        lecno = 0  
        user = request.user
        num_attendend = 0

        for lecture in alllectures:
            lecno += 1
            time = lecture.time
            attended = Attendance.objects.filter(lecture=lecture).filter(student=user).exists()
            
            if attended:
                num_attendend += 1

            lectures.append({
                'lecno': lecno,
                'time': time,
                'attended': attended
            })

            
        if lecno:
            attendance_per = num_attendend / lecno
        attendance_per *= 100


    # print(lectures)
    return render(request, 'attendance/student_course.html', {
        'is_enrolled': is_enrolled, 'course': course, 'lectures': lectures, 'attendance_per': attendance_per})