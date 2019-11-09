from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Enrollment, Lecture, Attendance
from .decorators import student_required, teacher_required
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import NewLectureForm, QueryForm
from accounts.models import User
import csv
from django.http import HttpResponse
from django.utils import timezone
import datetime


def home(request):
    """Renders a homepage for every type of user.

        :param request:
        """
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
    """Renders the form for scheduling a lecture for a course and schedules it
        
        :param request:
        :param course_name: The name of course
        :type course_name: str
        """
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

            for i in range(lecture.num_weeks):
                lecture.time += (i * datetime.timedelta(days = 7))
                lecture.save()
                
            return redirect('home')

    else:
        form = NewLectureForm()

    return render(request, 'attendance/new_lecture.html', {'form': form, 'course': course})            

def attendance_query(request, form, course):
    """Renders the data about students with attendance greater/lesser than a value
        
        :param request:
        :param form: The form used for requesting information
        :type form: QueryForm
        :param course: relevant course
        :type course: Course
        """
    students = course.enrollments.values('student')
    lectures = course.lectures.all().filter(time__lte=timezone.localtime())
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
def export_as_csv(request, course_name):
    """Returns the CSV file for the attendance in course
        
        :param request:
        :param course_name: The name of course
        :type course_name: str
        """
    course = get_object_or_404(Course, name=course_name)
    
    if (request.user != course.teacher):
        raise PermissionDenied

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + course.name +'.csv"'
    writer = csv.writer(response)

    students = course.enrollments.values('student')
    lectures = course.lectures.all().order_by('time')
    row1 = ['Students']
    cnt = 0

    for lecture in lectures:
        cnt += 1
        row1.append('Lecture ' + str(cnt))

    writer.writerow(row1)    


    for student_ in students:
        student = get_object_or_404(User, pk=student_['student'])
        row = []
        row.append(student.username)

        for lecture in lectures:
            attended = Attendance.objects.filter(lecture=lecture).filter(student=student).exists()

            if attended:
                row.append(1)
            else:
                row.append(0)    
                
        writer.writerow(row)

    return response        

@login_required
@teacher_required
def course_lectures(request, course_name):
    """Renders all the lectures for a course along with attendance status
        
        :param request:
        :param course_name: The name of course
        :type course_name: str
        """
    course = get_object_or_404(Course, name=course_name)
    
    if (request.user != course.teacher):
        raise PermissionDenied
    
    students = course.enrollments.values('student')
    lectures = course.lectures.all().order_by('time')
    total = len(students)
    attendances = []
    cnt = 0

    for lecture in lectures:
        cnt += 1
        total_attended = 0

        for student_ in students:
            student = get_object_or_404(User, pk=student_['student'])
            attended = Attendance.objects.filter(lecture=lecture).filter(student=student).exists()

            if attended:
                total_attended += 1

        if (total > 0):
            total_attended /= total
            total_attended *= 100
        else:    
            total_attended = 100    
        
        attendances.append({
            'time': lecture.time,
            'lecture': lecture.pk,
            'percent': total_attended,
            'cnt': cnt
        })          

    return render(request, 'attendance/course_lectures.html', {'course': course, 'lectures': attendances})            

@login_required
@teacher_required
def course_lecture(request, course_name, pk):
    """Renders the attendance info for all the students corresponding to a lecture
        
        :param request:
        :param course_name: The name of course
        :type course_name: str
        :param pk: The primary key for the lecture
        :type pk: int
        """
    course = get_object_or_404(Course, name=course_name)
    
    if (request.user != course.teacher):
        raise PermissionDenied
    
    students = course.enrollments.values('student')
    lecture = get_object_or_404(Lecture, pk=pk)
    total = len(students)
    attendances = []
    total_attended = 0

    for student_ in students:
        student = get_object_or_404(User, pk=student_['student'])
        attended = Attendance.objects.filter(lecture=lecture).filter(student=student).exists()

        if attended:
            total_attended += 1

        attendances.append({
        'name': student.first_name,
        'pk': student.pk,
        'attended': attended
        })     

    if (total > 0):
        total_attended /= total
        total_attended *= 100
    else:    
        total_attended = 100             

    return render(request, 'attendance/course_lecture.html', {'attendance': total_attended, 'course': course, 'lecture': lecture, 'students': attendances})            


@login_required
@teacher_required
def course_students(request, course_name):
    """Renders the attendance info for all the students in the course
        
        :param request:
        :param course_name: The name of course
        :type course_name: str
        """
    course = get_object_or_404(Course, name=course_name)
    
    if (request.user != course.teacher):
        raise PermissionDenied
    
    students = course.enrollments.values('student')
    lectures = course.lectures.all().filter(time__lte=timezone.localtime())
    total = len(lectures)
    attendances = []

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
        
        attendances.append({
            'student': student.first_name,
            'percent': total_attended,
            'student_pk': student.pk
        })          

    return render(request, 'attendance/course_students.html', {'course': course, 'attendances': attendances})            

@login_required
@teacher_required
def course_student(request, course_name, pk):
    """Renders the attendance info for a student in a course
        
        :param request:
        :param course_name: The name of course
        :type course_name: str
        :param pk: The primary key for the student
        :type pk: int
        """
    course = get_object_or_404(Course, name=course_name)
    
    if (request.user != course.teacher):
        raise PermissionDenied

    lectures = course.lectures.all().order_by('time').filter(time__lte=timezone.localtime())
    total = len(lectures)
    attendances = []
    student = get_object_or_404(User, pk=pk)
    total_attended = 0
    cnt = 0

    for lecture in lectures:
        cnt += 1
        attended = Attendance.objects.filter(lecture=lecture).filter(student=student).exists()

        if attended:
            total_attended += 1

        attendances.append({
        'time': lecture.time,
        'present': attended,
        'lecture': lecture.pk,
        'cnt': cnt
        })     

    if (total > 0):
        total_attended /= total
        total_attended *= 100
    else:    
        total_attended = 100             

    return render(request, 'attendance/course_student.html', {'attendance': total_attended, 'course': course, 'lectures': attendances, 'student': student})            

@login_required
@teacher_required
def teacher_course(request, course_name):
    """Renders the homepage for a course
        
        :param request:
        :param course_name: The name of course
        :type course_name: str
        """
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
    """Renders all the courses in which the student has enrolled
        
        :param request:
        """
    enrolled = request.user.enrollments.values('course')
    enrolled = [item['course'] for item in enrolled]
    return render(request, 'attendance/student_my_courses.html', {'courses': enrolled})

@login_required
@student_required
def student_course(request, course_name):
    """Renders the lecture-wise attendance info for a student
    
    :param request:
    :param course_name: The name of course
    :type course_name: str
    """
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
        alllectures = Lecture.objects.filter(course=course).filter(time__lte=timezone.localtime()).order_by('time')  
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