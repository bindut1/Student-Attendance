from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime
from attendance.models import Account, Course
from courses.models import ClassSchedule
from django.shortcuts import get_object_or_404
from attendance.models import Attendance
from datetime import datetime, timedelta
from django.utils import timezone

@login_required
def student_schedule(request, account_id):
    student = get_object_or_404(Account, account_id=account_id)
    
    current_datetime = datetime.now()
    current_day_name = current_datetime.strftime('%A')
    current_date = current_datetime.date()
    current_time = current_datetime.time()
    # print(current_date)
    print(current_time)
    
    schedules = ClassSchedule.objects.filter(student=student)

    courses_today = []
    for schedule in schedules:
        course = schedule.course
        if current_day_name.lower() in course.weekdays.lower():
            is_attended = Attendance.objects.filter(
                student=student,
                course=course,
                check_in_date=current_date
            ).exists()
            
            start_time = datetime.strptime(str(course.start_time), '%H:%M:%S').time()
            end_time = datetime.strptime(str(course.end_time), '%H:%M:%S').time()
            
            can_attend = start_time <= current_time <= end_time and not is_attended
            # print(can_attend)
            courses_today.append({
                'course_id': course.course_id,
                'course_name': course.course_name,
                'start_time': course.start_time.strftime('%H:%M'),  
                'end_time': course.end_time.strftime('%H:%M'),      
                'room': course.room,
                'weekdays': course.weekdays,
                'is_attended': is_attended,
                'can_attend': can_attend
            })
    
    context = {
        'student': student,
        'courses_today': courses_today,
        'current_day': current_day_name
    }
    return render(request, 'student/schedule.html', context)

@login_required
def instructor_schedule(request, account_id):
    instructor = get_object_or_404(Account, account_id=account_id)
    current_day = datetime.now().strftime('%A')  

    schedules = Course.objects.filter(instructor=instructor)

    courses_today = []
    for schedule in schedules:
        if current_day.lower() in schedule.weekdays.lower():  
            courses_today.append({
                'course_id': schedule.course_id,
                'course_name': schedule.course_name,
                'start_time': schedule.start_time.strftime('%H:%M'),  
                'end_time': schedule.end_time.strftime('%H:%M'),      
                'room': schedule.room,
                'weekdays': schedule.weekdays
            })

    return render(request, 'instructor/schedule.html', {
        'instructor': instructor,
        'courses_today': courses_today,
        'current_day': current_day
    })


@login_required
def student_list_by_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    current_date = timezone.now().date()
    schedules = ClassSchedule.objects.filter(course=course).select_related('student')
    
    students_data = []
    attended_count = 0
    
    for schedule in schedules:
        student = schedule.student
        attendance = Attendance.objects.filter(
            student=student,
            course=course,
            check_in_date=current_date
        ).first()
        is_attended = attendance is not None
        if is_attended:
            attended_count += 1
        students_data.append({
            'student': student,
            'is_attended': is_attended,
            'attendance': attendance 
        })
    
    not_attended_count = len(students_data) - attended_count
    start_time = course.start_time.strftime('%H:%M')
    end_time = course.end_time.strftime('%H:%M')
    context = {
        'course': course,
        'start_time': start_time,
        'end_time': end_time,
        'students_data': students_data,
        'current_date': current_date,
        'attended_count': attended_count,
        'not_attended_count': not_attended_count
    }
    
    return render(request, 'instructor/student_list.html', context)