from django.shortcuts import render

def student_dashboard(request):
    context = {
        'message': 'Chào mừng bạn đến với trang học sinh!',
        'username': 'Student',
    }
    return render(request, 'student/dashboard.html', context)
