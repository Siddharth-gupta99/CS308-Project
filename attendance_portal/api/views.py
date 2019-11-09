from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from rest_framework.views import APIView
from attendance.models import Lecture, Course, Attendance, Enrollment

from rest_framework import viewsets
from .serializers import  GETSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.utils import timezone
from accounts.models import User
import datetime

@api_view(['GET'])
@permission_classes((AllowAny,))
def ApiView(request, classroom_id):
	if request.method == 'GET':
		print("joe")
		now = datetime.datetime.now()
		t1 = now + datetime.timedelta(hours=1)
		lec = Lecture.objects.filter(time__gte=now, time__lte=t1)
		lec = lec.filter(Class=classroom_id)
		lec = lec.order_by('time').first()
		response_data = GETSerializer(lec, many=False).data
		return Response(response_data)

@api_view(['POST'])
@permission_classes((AllowAny,))
def ApiView2(request):
	if request.method == 'POST':
		attendanceData = request.data
		print(attendanceData)
		student = get_object_or_404(User, username=attendanceData["roll_number"])
		lecture = get_object_or_404(Lecture, pk=attendanceData["lecture_id"])
		print("pk =",lecture.pk, "LectureC", lecture.course)
		test = Enrollment.objects.all()
		print(test)
		kull = Enrollment.objects.filter(course=lecture.course, student=student.pk)
		print(kull)

		if kull:
			Attendance.objects.create(
				student=student,
				lecture=lecture)
			return Response({"Response":"Data is received and saved (I guess!)"})
		else:
			return Response({"Response":"Erooooooooooor Bro!"})


@api_view(['GET'])
@permission_classes((AllowAny,))
def currentTimeView(request):
	if request.method == 'GET':
		print("Accessed currentTimeView.")
		now = datetime.datetime.now()
		return Response({"current_time":now})
