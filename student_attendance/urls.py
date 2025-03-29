from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('courses/', include('courses.urls')),
    path('face_recognition/', include('face_recognition.urls')),
    path('attendance/', include('attendance.urls')),
    path('admin/', admin.site.urls),
]
