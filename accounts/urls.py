from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("student/info/", views.student_info, name="student_info"),
    path("student/edit/<str:account_id>/", views.student_edit, name="student_edit"),
    path("student/search/", views.student_search, name="student_search"),
    path("instructor/info/", views.instructor_info, name="instructor_info"),
    path(
        "instructor/edit/<str:account_id>/",
        views.instructor_edit,
        name="instructor_edit",
    ),
    path("instructor/search/", views.instructor_search, name="instructor_search"),
]
