from django.contrib import admin
from django.urls import path
from .views import student_views, teacher_views, views,auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path("login/", auth_views.login_view, name="login"),
    path("logout/", auth_views.logout_view, name="logout"),
    path('student/dashboard/', student_views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', teacher_views.teacher_dashboard, name='teacher_dashboard'),
]