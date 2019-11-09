from rest_framework import serializers
from attendance.models import Lecture, Attendance
import datetime

class GETSerializer(serializers.ModelSerializer):
	class Meta:
		model=Lecture
		fields=('id', 'time')

class POSTSerializer(serializers.ModelSerializer):
	class Meta:
		model=Attendance
		fields=('student', 'lecture')
