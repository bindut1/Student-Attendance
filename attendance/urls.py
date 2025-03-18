from django.contrib import admin
from django.urls import path
from .views import student_views, teacher_views, views,auth_views

urlpatterns = [
    path('',views.home ,name='home'),
    path("login/", auth_views.login_view, name="login"),
    path("logout/", auth_views.logout_view, name="logout"),
    path('student/info/', student_views.student_info, name='student_info'),
    path('student/edit/<str:account_id>/', student_views.student_edit, name='student_edit'),
    path('student/search/', student_views.student_search, name='student_search'),    
    path('student/<str:account_id>/schedule/', student_views.student_schedule, name='student_schedule'),
    path('instructor/info/', teacher_views.instructor_info, name='instructor_info'),
    path('instructor/edit/<str:account_id>/', teacher_views.instructor_edit, name='instructor_edit'),
    path('instructor/<str:account_id>/schedule/', teacher_views.instructor_schedule, name='instructor_schedule'),
    path('instructor/search/', teacher_views.instructor_search, name='instructor_search'),
    path('student/<str:account_id>/upload-images/', student_views.upload_and_send, name='student_upload_images'),
]