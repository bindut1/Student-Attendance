from django.contrib import admin
from django.urls import path
from .views import student_views, teacher_views, views

urlpatterns = [
    path('student/info/', student_views.student_info, name='student_info'),
    path('student/edit/<str:account_id>/', student_views.student_edit, name='student_edit'),
    path('student/search/', student_views.student_search, name='student_search'),
    path('teacher/dashboard/', teacher_views.teacher_dashboard, name='teacher_dashboard'),
]