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
After cloning the repo, install all the requirements from the requirements.txt. After that to start the django server write:

   `python manage.py runserver`

 Go to provided link after running above command.
 Then, you will land up on a portal.
