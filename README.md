# Attendance via Face Recognition


----
## About
This project is to automate the attendence system in universites, schools and can be used in other organisation with few modifications.
The facial recognition system uses a camera for capturing images in a classroom that are sent over to a server using a Raspberry Pi. 
The identified students’ (name and roll number) is sent to a web portal system via provided API. The web portal for our system is made using Django (v2.2.6) Framework.

## Requriments
1. **Hardware**
  * Raspberry Pi Model 3B+
  * Camera

2. **Software**
  * Python 3.6.8
  * Pip 19.2.3
  * Django 2.2.6
  * Tensorflow 1.12.0
  * Keras 2.2.4

## Building & Running

**Clone the repo** (i.e. git clone https://github.com/Siddharth-gupta99/CS308-Project)

1. **Raspberry Pi**
  * Install Arch Linux ARMv8 on the Raspberry Pi.
Refer to:
[https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-3](https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-3)
  * Copy the scripts in the Raspberry Pi directory to the Pi and run them.

2. **Web Portal**
Instructions can be found on [https://github.com/Siddharth-gupta99/CS308-Project/blob/master/installation.md](https://github.com/Siddharth-gupta99/CS308-Project/blob/master/installation.md).

## Usage

### Web Portal
#### Teachers
Signup as a teacher and login. You can schedule a lecture, get attendance as excel, query for attendance. You can also see student-wise & lecture-wise attendance.
#### Students
Signup as a student and login. You can enroll for courses, see your attendance for every course (lecture-wise).
#### Admin
1. Create a superuser.
	1. >   python manage.py createsuperuser
	2. >   python manage.py runserver
2. Go to admin url (host/admin) and login.

# Documentation

## Web Portal
The dev documentation for Web Portal can be found by opening [this](https://github.com/Siddharth-gupta99/CS308-Project/blob/master/attendance_portal/docs/_build/html/index.html) file in a web browser when the code is at your local machine.

## User & Face Recognition (Developer) Documentation
The dev documentation for Face Detection can be found by opening [this](https://github.com/Siddharth-gupta99/CS308-Project/blob/master/MicrosoftAPI/FaceRecognition_Documentation/docs/_build/html/index.html) file in a web browser when the code is at your local machine.
