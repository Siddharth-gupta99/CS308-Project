"""attendance_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import accounts.views as accounts_views
import attendance.views as attendance_views
from accounts.forms import LoginForm
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', attendance_views.home, name='home'),
    path('teachers/course/<str:course_name>', attendance_views.teacher_course, name='teacher_course'),
    path('teachers/course/<str:course_name>/schedule', attendance_views.course_schedule, name='course_schedule'),
    path('teachers/course/<str:course_name>/lectures', attendance_views.course_lectures, name='course_lectures'),
    path('teachers/course/<str:course_name>/lectures/<int:pk>', attendance_views.course_lecture, name='course_lecture'),
    path('teachers/course/<str:course_name>/students', attendance_views.course_students, name='course_students'),
    path('teachers/course/<str:course_name>/students/<int:pk>', attendance_views.course_student, name='course_student'),    
    path('students/my_courses', attendance_views.my_courses, name='student_courses'),
    path('students/course/<str:course_name>', attendance_views.student_course, name='student_course'),
    path('admin/', admin.site.urls),
    path('signup/', accounts_views.signup , name='signup'),
    path('signup/student/', accounts_views.StudentSignUpView.as_view(), name='signup_student'),
    path('signup/teacher/', accounts_views.TeacherSignUpView.as_view(), name='signup_teacher'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
