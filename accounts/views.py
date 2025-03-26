from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404
from core.helpers.formHelper import FormHelper
from django.db import models
from attendance.models import Account
import cloudinary
import cloudinary.uploader


def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == "instructor":
            return redirect("accounts:instructor_info")
        elif request.user.role == "student":
            return redirect("accounts:student_info")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            if user.role == "instructor":
                return redirect("accounts:instructor_info")
            elif user.role == "student":
                return redirect("accounts:student_info")
        else:
            messages.error(request, "Email hoặc mật khẩu không đúng")

    return render(request, "defaults/login.html")


def logout_view(request):
    logout(request)
    return redirect("accounts:login")


@login_required
def student_info(request):
    try:
        student = request.user
        if request.user.role != "student":
            raise Http404("Không tìm thấy thông tin sinh viên")
        context = {"student": student, "message": "Thông tin cá nhân của bạn"}
        return render(request, "student/dashboard.html", context)
    except Http404 as e:
        return render(
            request,
            "student/dashboard.html",
            {"error": str(e), "message": "Lỗi truy xuất thông tin"},
        )


@login_required
def student_edit(request, account_id):
    student = request.user

    if request.method == "POST":
        form = FormHelper(request.POST, request.FILES, instance=student)
        if form.is_valid():
            if "avatar" in request.FILES:
                avatar = request.FILES["avatar"]
                cloudinary_response = cloudinary.uploader.upload(
                    avatar,
                    folder="student_avatars",
                    transformation=[
                        {"width": 300, "height": 300, "crop": "fill"},
                        {"radius": "max"},
                    ],
                )
                student.avatar = cloudinary_response["secure_url"]

            student = form.save(commit=False)
            student.password = Account.objects.get(pk=student.pk).password
            student.save()
            return redirect("accounts:student_info")
    else:
        form = FormHelper(instance=student)

    return render(
        request, "student/edit.html", {"form": form, "student": student}
    )


@login_required
def student_search(request):
    query = request.GET.get("q", "").strip()
    students = Account.objects.filter(role="student")

    if query:
        students = students.filter(
            models.Q(email__icontains=query) | models.Q(full_name__icontains=query)
        )

    return render(
        request, "student/search.html", {"students": students, "query": query}
    )


@login_required
def instructor_info(request):
    try:
        instructor = request.user
        if request.user.role != "instructor":
            raise Http404("Không tìm thấy thông tin sinh viên")
        context = {"instructor": instructor, "message": "Thông tin cá nhân của bạn"}
        return render(request, "instructor/dashboard.html", context)
    except Http404 as e:
        return render(
            request,
            "instructor/dashboard.html",
            {"error": str(e), "message": "Lỗi truy xuất thông tin"},
        )


@login_required
def instructor_edit(request, account_id):
    instructor = request.user

    if request.method == "POST":
        form = FormHelper(request.POST, request.FILES, instance=instructor)
        if form.is_valid():
            if "avatar" in request.FILES:
                avatar = request.FILES["avatar"]
                cloudinary_response = cloudinary.uploader.upload(
                    avatar,
                    folder="instructor_avatars",
                    transformation=[
                        {"width": 300, "height": 300, "crop": "fill"},
                        {"radius": "max"},
                    ],
                )
                instructor.avatar = cloudinary_response["secure_url"]

            instructor = form.save(commit=False)
            instructor.password = Account.objects.get(pk=instructor.pk).password
            instructor.save()
            return redirect("accounts:instructor_info")
    else:
        form = FormHelper(instance=instructor)

    return render(
        request,
        "instructor/edit.html",
        {"form": form, "instructor": instructor},
    )


@login_required
def instructor_search(request):
    query = request.GET.get("q")
    users = None
    if query:
        users = Account.objects.filter(full_name__icontains=query)

    return render(
        request, "instructor/search.html", {"users": users, "query": query}
    )
