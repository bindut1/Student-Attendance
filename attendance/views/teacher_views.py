from django.shortcuts import render

def teacher_dashboard(request):
    context = {
        'message': 'Chào mừng bạn đến với trang giáo vien!',
        'username': 'Teacher',
    }
    return render(request, 'teacher/dashboard.html', context)
