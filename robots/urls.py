from django.urls import path
from .views import create_robot, generate_robot_report


urlpatterns = [
    path('create_robot/', create_robot, name='create_robot'),
    path('generate_robot_report/', generate_robot_report, name='generate_robot_report'),
]