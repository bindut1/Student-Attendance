from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='layouts/home.html'), name='home'),
    path('accounts/', include('accounts.urls')),
    path('courses/', include('courses.urls')),
    path('face_recognition/', include('face_recognition.urls')),
    path('attendance/', include('attendance.urls')),
    path('admin/', admin.site.urls),
]
