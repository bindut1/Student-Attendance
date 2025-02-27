from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from attendance.models import ClassSchedule, Course

@login_required
def student_dashboard(request):
    if request.user.role == 'student':
        today = date.today()
        current_weekday = today.strftime('%A').lower() 

        student_classes_today = ClassSchedule.objects.filter(
            student=request.user,
            course__weekdays__icontains=current_weekday,  
            course__start_date__lte=today,  
            course__end_date__gte=today,   
        ).order_by('course__start_time')  

        context = {
            'message': 'Chào mừng bạn đến với trang học sinh!',
            'username': request.user.full_name,
            'student_classes_today': student_classes_today, 
            'today': today
        }
        
        return render(request, 'student/dashboard.html', context)
    else:
        return render(request, 'error.html', {'message': 'Bạn không có quyền truy cập vào trang này.'})
