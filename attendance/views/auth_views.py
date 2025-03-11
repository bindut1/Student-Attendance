from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)  

        if user is not None:
            login(request, user)
            if user.role == "instructor":
                return redirect("teacher_dashboard") 
            elif user.role == "student":
                return redirect("student_info")  
        else:
            messages.error(request, "Email hoặc mật khẩu không đúng")

    return render(request, "auth/login.html")  
def logout_view(request):
    logout(request)
    return redirect("login")
