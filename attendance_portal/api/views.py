from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
# from .models import Course, Enrollment, Lecture, Attendance
# from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import ApiSerializer
from attendance.models import Lecture
# from .models import Language
# Create your views here.

# from django.shortcuts import render
from rest_framework import viewsets
# from .models import Language
from .serializers import  ApiSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

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
def ApiView(request):
    if request.method == 'GET':
        # print("joe")
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
        # posts = Language.objects.all()
        # print(posts)
        lec = lec.order_by('time')
        # print(posts)
        # print(now)
        # print(obj)
        serializer = ApiSerializer(lec, many=True)
        return Response(serializer.data)