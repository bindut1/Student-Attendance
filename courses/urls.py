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
        "student/<str:account_id>/schedule-week/",
        views.student_schedule_week,
        name="student_schedule_week",
    ),
    path(
        "instructor/<str:account_id>/schedule/",
        views.instructor_schedule,
        name="instructor_schedule",
    ),
    path(
        "instructor/<str:account_id>/schedule-week/",
        views.instructor_schedule_week,
        name="instructor_schedule_week",
    ),
    path(
        "<int:course_id>/students-list/",
        views.student_list_by_course,
        name="student_list_by_course",
    ),
    path(
        "<int:course_id>/export-attendance/",
        views.export_attendance,
        name="export_attendance",
    ),
]
