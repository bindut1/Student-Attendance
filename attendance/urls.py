from django.contrib import admin
from django.urls import path
from .views import student_views, teacher_views, views,auth_views

urlpatterns = [
    path('', student_views.student_info, name='home'),
    path("login/", auth_views.login_view, name="login"),
    path("logout/", auth_views.logout_view, name="logout"),
    path('student/info/', student_views.student_info, name='student_info'),
    path('student/edit/<str:account_id>/', student_views.student_edit, name='student_edit'),
    path('student/search/', student_views.student_search, name='student_search'),    
    path('student/<str:account_id>/schedule/', student_views.student_schedule, name='student_schedule'),
    path('teacher/dashboard/', teacher_views.teacher_dashboard, name='teacher_dashboard'),
    path('student/<str:account_id>/upload-images/', student_views.upload_and_send, name='student_upload_images'),
]