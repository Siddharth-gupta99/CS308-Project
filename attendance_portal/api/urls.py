from rest_framework import  routers
from . import views 
from django.urls import path, include

# router=routers.DefaultRouter()
# router.register('l', views.ApiView)

urlpatterns = [
	# path('', include(router.urls))
	path('lecture/<int:classroom_id>/', views.ApiView),
	path('lecture/s', views.ApiView2)
	]