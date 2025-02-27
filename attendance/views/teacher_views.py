

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from attendance.models import Course  

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from attendance.models import Course

@login_required
def teacher_dashboard(request):
    if request.user.role == 'instructor':
        today = date.today()
        current_weekday = today.strftime('%A').lower() 

        instructor_courses_today = Course.objects.filter(
            instructor=request.user,
            weekdays__icontains=current_weekday
        ).order_by('start_time')

        context = {
            'message': 'Chào mừng bạn đến với trang giáo viên!',
            'username': request.user.full_name,
            'instructor_courses_today': instructor_courses_today, 
            'today': today
        }
        
        return render(request, 'teacher/dashboard.html', context)
    else:
        return render(request, 'error.html', {'message': 'Bạn không có quyền truy cập vào trang này.'})

