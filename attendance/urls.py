from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('history/<str:account_id>/', views.attendance_history, name='history'),
]