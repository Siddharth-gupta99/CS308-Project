from rest_framework import  routers
from . import views 
from django.urls import path, include

urlpatterns = [
	path('lecture/<int:classroom_id>/', views.ApiView),
	path('lecture/s', views.ApiView2),
	path('lecture/current-time', views.currentTimeView)
	]