from django.db import models
from accounts.models import User
import datetime as Datetime
from django.core.validators import MinValueValidator
from django.utils import timezone
# Create your models here.

class Course(models.Model):
    """This class represents a course 

    :param name: name the primary key for the model
    :param teacher: foreign key to refer the teacher of the course
    """
    name = models.CharField(max_length=255, primary_key=True)
    teacher = models.ForeignKey(User, related_name='courses', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    """This class represents an enrollment of a student in a course

    :param course: foreign key to refer the course
    :param student: foreign key to refer the student
    """
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE, null=False)
    student = models.ForeignKey(User, related_name='enrollments', on_delete=models.CASCADE, null=False)

class Lecture(models.Model):
    """This class represents a lecture

    :param course: foreign key to refer the course
    :param time: time for the lecture
    :param duration: duration of the lecture
    :param Class: the class for the lecture
    """
    course = models.ForeignKey(Course, related_name='lectures', on_delete=models.CASCADE, null=False)
    time = models.DateTimeField(null=False, default=timezone.localtime())
    duration = models.DurationField(null=False, default=Datetime.timedelta(days=0, hours=1),
                validators=[MinValueValidator(Datetime.timedelta(days=0, hours=1, minutes=0))])
    num_weeks = models.IntegerField(null=False, default=1)            
    Class = models.IntegerField(null=False,
        choices=(
        (1, "A10-1A"),
        (2, "A10-1B"),
        (3, "A10-1C"),
        (4, "A10-1D"),
        (5, "A13-3A"),
        (6, "A1-NKN")
    ))

class Attendance(models.Model):
    """This class represents an Attendance record for a student in a lecture

    :param student: foreign key to refer the student
    :param lecture: foreign key to refer the lecture
    """
    student = models.ForeignKey(User, related_name='attendances', on_delete=models.CASCADE, null=False)
    lecture = models.ForeignKey(Lecture, related_name='attendances', on_delete=models.CASCADE, null=False)

    class Meta:
        unique_together = (("student", "lecture"),) 
