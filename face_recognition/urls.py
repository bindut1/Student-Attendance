from django.urls import path
from . import views

app_name = "face_recognition"

urlpatterns = [
    path(
        "student/<str:account_id>/upload-images/",
        views.upload_and_send,
        name="student_upload_images",
    ),
]
