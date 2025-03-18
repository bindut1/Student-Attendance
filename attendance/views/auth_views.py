from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
def login_view(request):
    # Kiểm tra nếu người dùng đã đăng nhập
    if request.user.is_authenticated:
        if request.user.role == "instructor":
            return redirect("instructor_info")  # Chuyển hướng đến trang giảng viên
        elif request.user.role == "student":
            return redirect("student_info")  # Chuyển hướng đến trang sinh viên

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)  

        if user is not None:
            login(request, user)
            if user.role == "instructor":
                return redirect("instructor_info") 
            elif user.role == "student":
                return redirect("student_info")  
        else:
            messages.error(request, "Email hoặc mật khẩu không đúng")

    return render(request, "auth/login.html")
def logout_view(request):
    logout(request)
    return redirect("login")
