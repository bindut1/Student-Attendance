from accounts.models import Account
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from attendance.models import Attendance
from courses.models import Course
from datetime import timedelta
import json

@login_required
def attendance_history(request, account_id):
    student = get_object_or_404(Account, account_id=account_id)
    courses = Course.objects.filter(classschedule__student=student).distinct()

    attendance_data = []
    for course in courses:
        start_date = course.start_date
        end_date = course.end_date
        weeks = []
        current_date = start_date
        while current_date <= end_date:
            weeks.append(current_date)
            current_date += timedelta(weeks=1)

        weekly_attendance = []
        for week_start in weeks:
            week_end = week_start + timedelta(days=6)
            attendance = Attendance.objects.filter(
                student=student,
                course=course,
                check_in_date__range=(week_start, week_end)
            ).first()

            if attendance:
                details_json = json.dumps({
                    'check_in_date': attendance.check_in_date.strftime('%Y-%m-%d'),
                    'check_in_time': attendance.check_in_time.strftime('%H:%M:%S') if attendance.check_in_time else "N/A",
                    'room': course.room or "N/A"
                }, ensure_ascii=False)

                weekly_attendance.append({
                    'details': details_json
                })
            else:
                weekly_attendance.append({
                    'details': None
                })

        attendance_data.append({
            'course_name': course.course_name,
            'weekly_attendance': weekly_attendance
        })

    context = {
        'student': student,
        'attendance_data': attendance_data
    }
    return render(request, 'student/history.html', context)