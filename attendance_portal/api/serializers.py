# from rest_framework import serializers

# class apiSerializer(serializers.ModelSerializer):
# 	# class Meta:
# 	# 	# models=
# 	# 	# fields=
# 	pass
  
from rest_framework import serializers
# from .models import Language
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
