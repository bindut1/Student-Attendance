from django.contrib import admin
from django.urls import path
from .views import student_views, teacher_views, views

urlpatterns = [
    path('', views.home, name='home'),
    path('student/dashboard/', student_views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', teacher_views.teacher_dashboard, name='teacher_dashboard'),
]