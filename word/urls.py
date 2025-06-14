from django.urls import path, include
from word import views 
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', views.MainViewset, basename='actions')

urlpatterns = [
    path('', include(router.urls), name='api'),
]