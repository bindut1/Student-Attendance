from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path(
        "student/<str:account_id>/schedule/",
        views.student_schedule,
        name="student_schedule",
    ),
    path(
        "instructor/<str:account_id>/schedule/",
        views.instructor_schedule,
        name="instructor_schedule",
    ),
    path(
        "<int:course_id>/students-list/",
        views.student_list_by_course,
        name="student_list_by_course",
    ),
]
