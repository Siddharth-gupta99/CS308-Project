from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
# from .models import Course, Enrollment, Lecture, Attendance
# from rest_framework import viewsets
from rest_framework.views import APIView
from attendance.models import Lecture, Course, Attendance, Enrollment
# from .models import Language
# Create your views here.

# from django.shortcuts import render
from rest_framework import viewsets
# from .models import Language
from .serializers import  GETSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.utils import timezone
from accounts.models import User
# from 
# from django.shortcuts import render, HttpResponse
import datetime
# from django.db.models.functions import Length


# class ApiView(APIView):
	# def get(self, request, format=None):
		# now = datetime.now()
		# print(now) 
		# current_time = now.strftime("%H:%M:%S")
		# print("Current Time =", current_time)
		# queryset=Lecture.objects.all()
		# serializer=ApiSerializer(queryset)
		# # return
		# print("hello")
		# return HttpResponse("IT IS NOW")
	# pass


# class ApiView(viewsets.ModelViewSet):
# 	# pass
# 	# now = datetime.now()
# 	# print(now) 
# 	# current_time = now.strftime("%H:%M:%S")
# 	print("Current Time =", current_time)
# 	def check(self):
# 		print("hailhydra")
# 		return HttpResponse("IT IS NOW")
# 	queryset=Lecture.objects.all()
# 	serializer_class=ApiSerializer


# def apiView(viewsets.ModelViewSet, lec_num):
# 	query_set=Lecture.objects.all()
	# serializer_class=apiSerializer()k

# def api_func(request, lec_num):
# 		lec_num
# 		return HttpResponse("It is now")

# a = ApiView()
# a.check()

@api_view(['GET'])
@permission_classes((AllowAny,))
def ApiView(request, classroom_id):
	if request.method == 'GET':
		print("joe")
		now = datetime.datetime.now()
		# print(now) 
		# current_time = now.strftime("%H:%M:%S")
		# print("Current Time =", current_time)
		t1 = now + datetime.timedelta(hours=1)
		# print(t1)
		# t2 = now - datetime.timedelta(minutes=12)
		# print(datetime.datetime.time(now))
		# posts = Language.objects.filter(time__gte=datetime.datetime.time(now),
								# time__lte=datetime.datetime.time(t1))
		# posts = Language.objects.filter(name={'C', 'C++'})

		lec = Lecture.objects.filter(time__gte=now, time__lte=t1)
		lec = lec.filter(Class=classroom_id)
		lec = lec.order_by('time').first()
		# lec = Lecture.objects.all()
		response_data = GETSerializer(lec, many=False).data
		response_data['current_time'] = timezone.now()
		return Response(response_data)
		# return HttpResponse("Yo")
		# pass

# @api_view(['GET', 'POST'])
# @permission_classes((AllowAny,))
# def ApiView2(request):
#     if request.method=='POST':
#        return HttpResponse("YO")
#     return HttpResponse("yooo")
	# elif request.method=='POST':
	#     return HttpResponse("YOO")

@api_view(['POST'])
@permission_classes((AllowAny,))
def ApiView2(request):
	# if request.method == 'GET':
	#     posts = Post.objects.all()
	#     serializer = PostSerializer(posts, many=True)
	#     return Response(serializer.data)
		# return HttpResponse("Yo")
	if request.method == 'POST':
		attendanceData = request.data
		student = get_object_or_404(User, username=attendanceData["roll_number"])
		lecture = get_object_or_404(Lecture, pk=attendanceData["lecture_id"])
		# course = lecture.
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


# if request.method == 'GET':
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         data = {'text': request.DATA.get('the_post'), 'author': request.user.pk}
#         serializer = PostSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)