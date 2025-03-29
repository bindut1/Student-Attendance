from django.urls import path
from . import views

app_name = "face_recognition"

urlpatterns = [
    path(
        "student/<int:account_id>/upload-images/",
        views.upload_training_images,
        name="student_upload_images",
    ),
    path(
        "api/facial_recognition/",
        views.verify_face_for_attendance,
        name="facial_recognition_api",
    ),
]
