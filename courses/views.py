from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime
from attendance.models import Account, Course
from courses.models import ClassSchedule
from django.shortcuts import get_object_or_404
from attendance.models import Attendance
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponse
import xlwt  # You may need to install this package: pip install xlwt

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

@login_required
def export_attendance(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    current_date = timezone.now().date()
    schedules = ClassSchedule.objects.filter(course=course).select_related('student')
    
    wb = xlwt.Workbook(encoding='utf-8')
    
    worksheet_name = f'Attendance-{course.course_id}' 
    ws = wb.add_sheet(worksheet_name)
    
    title_style = xlwt.easyxf('font: bold on, height 280; align: wrap on, vert centre, horiz center;')
    ws.write_merge(0, 0, 0, 4, f"Attendance for: {course.course_name}", title_style)
    
    header_style = xlwt.easyxf('font: bold on; align: wrap on, vert centre, horiz center; pattern: pattern solid, fore_color light_blue;')
    date_style = xlwt.easyxf(num_format_str='DD-MM-YYYY')
    time_style = xlwt.easyxf(num_format_str='HH:MM:SS')
    attended_style = xlwt.easyxf('pattern: pattern solid, fore_color light_green;')
    not_attended_style = xlwt.easyxf('pattern: pattern solid, fore_color light_yellow;')
    
    headers = ['STT', 'Student ID', 'Full Name', 'Status', 'Check-in Time']
    col_width = [1500, 4000, 8000, 4000, 4000]
    
    for i, width in enumerate(col_width):
        ws.col(i).width = width
    
    for col, header in enumerate(headers):
        ws.write(1, col, header, header_style)
    
    row = 2
    for schedule in schedules:
        student = schedule.student
        attendance = Attendance.objects.filter(
            student=student,
            course=course,
            check_in_date=current_date
        ).first()
        
        is_attended = attendance is not None
        status = 'Đã điểm danh' if is_attended else 'Chưa điểm danh'
        
        ws.write(row, 0, row-1)  
        ws.write(row, 1, student.account_id)
        
        if hasattr(student, 'name'):
            student_name = student.name
        elif hasattr(student, 'full_name'):
            student_name = student.full_name
        elif hasattr(student, 'username'):
            student_name = student.username
        else:
            student_name = f"Student {student.account_id}"
        
        ws.write(row, 2, student_name)
        
        if is_attended:
            ws.write(row, 3, status, attended_style)
            ws.write(row, 4, attendance.check_in_time.strftime('%H:%M:%S'), time_style)
        else:
            ws.write(row, 3, status, not_attended_style)
            ws.write(row, 4, '')
        
        row += 1
    
    attended_count = Attendance.objects.filter(
        course=course,
        check_in_date=current_date
    ).count()
    
    total_students = schedules.count()
    not_attended_count = total_students - attended_count
    
    row += 1
    ws.write(row, 0, 'Summary', header_style)
    ws.write(row, 1, f'Total: {total_students}')
    ws.write(row, 2, f'Attended: {attended_count}', attended_style)
    ws.write(row, 3, f'Absent: {not_attended_count}', not_attended_style)
    
    row += 1
    ws.write(row, 0, 'Date:', header_style)
    ws.write(row, 1, current_date.strftime('%Y-%m-%d'), date_style)
    
    response = HttpResponse(content_type='application/ms-excel')
    filename = f'attendance_{course.course_id}_{current_date.strftime("%Y-%m-%d")}.xls'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)
    
    return response

@login_required
def student_schedule_week(request, account_id):
    student = get_object_or_404(Account, account_id=account_id)
    current_date = timezone.now().date()
    # lấy thứ 2 của tuần hiện tại
    start_of_week = current_date - timedelta(days=current_date.weekday()) 
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]  

    schedules = ClassSchedule.objects.filter(student=student).select_related('course')
    weekly_schedule = []

    for date in week_dates:
        day_name = date.strftime('%A')
        daily_courses = []
        for schedule in schedules:
            course = schedule.course
            if day_name.lower() in course.weekdays.lower():
                daily_courses.append({
                    'course_id': course.course_id,
                    'course_name': course.course_name,
                    'start_time': course.start_time.strftime('%H:%M'),
                    'end_time': course.end_time.strftime('%H:%M'),
                    'room': course.room,
                    'weekdays': course.weekdays,
                })
        weekly_schedule.append({'date': date, 'day_name': day_name, 'courses': daily_courses})

    context = {
        'student': student,
        'weekly_schedule': weekly_schedule,
    }
    return render(request, 'student/schedule_week.html', context)


@login_required
def instructor_schedule_week(request, account_id):
    instructor = get_object_or_404(Account, account_id=account_id)
    current_date = timezone.now().date()
    start_of_week = current_date - timedelta(days=current_date.weekday()) 
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]  

    schedules = Course.objects.filter(instructor=instructor)
    weekly_schedule = []

    for date in week_dates:
        day_name = date.strftime('%A')
        daily_courses = []
        for schedule in schedules:
            if day_name.lower() in schedule.weekdays.lower():
                daily_courses.append({
                    'course_id': schedule.course_id,
                    'course_name': schedule.course_name,
                    'start_time': schedule.start_time.strftime('%H:%M'),
                    'end_time': schedule.end_time.strftime('%H:%M'),
                    'room': schedule.room,
                    'weekdays': schedule.weekdays,
                })
        weekly_schedule.append({'date': date, 'day_name': day_name, 'courses': daily_courses})

    context = {
        'instructor': instructor,
        'weekly_schedule': weekly_schedule,
    }
    return render(request, 'instructor/schedule_week.html', context)