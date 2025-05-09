from accounts.models import Account
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from attendance.models import Attendance
from courses.models import Course
from datetime import timedelta
import json
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect


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

@login_required
def attendance_statistic(request, account_id):
    instructor = get_object_or_404(Account, account_id=account_id, role='instructor')
    courses = Course.objects.filter(instructor=instructor)

    statistics_data = [{'course_name': course.course_name, 'course_id': course.course_id} for course in courses]

    context = {
        'instructor': instructor,
        'statistics_data': statistics_data
    }
    return render(request, 'instructor/statistic.html', context)


@login_required
def attendance_statistic_detail(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    start_date = course.start_date
    end_date = course.end_date
    weeks = []
    current_date = start_date
    while current_date <= end_date:
        weeks.append(current_date)
        current_date += timedelta(weeks=1)

    students = Account.objects.filter(classschedule__course=course, role='student').distinct()
    student_data = []
    for student in students:
        weekly_attendance = []
        absent_count = 0
        for week_start in weeks:
            week_end = week_start + timedelta(days=6)
            attendance = Attendance.objects.filter(
                student=student,
                course=course,
                check_in_date__range=(week_start, week_end)
            ).first()

            if attendance:
                weekly_attendance.append({
                    'details': json.dumps({
                        'check_in_date': attendance.check_in_date.strftime('%Y-%m-%d'),
                        'check_in_time': attendance.check_in_time.strftime('%H:%M:%S') if attendance.check_in_time else "N/A",
                        'room': course.room or "N/A"
                    }, ensure_ascii=False)
                })
            else:
                weekly_attendance.append({'details': None})
                absent_count += 1

        student_data.append({
            'student': student,
            'weekly_attendance': weekly_attendance,
            'absent_count': absent_count,
            'can_warn': absent_count > 3
        })

    context = {
        'course': course,
        'weeks': weeks,
        'student_data': student_data
    }
    return render(request, 'instructor/statistic_detail.html', context)

@login_required
def send_warning_email(request, student_id, course_id):
    student = get_object_or_404(Account, account_id=student_id, role='student')
    course = get_object_or_404(Course, course_id=course_id)

    subject = f"Cảnh cáo vắng mặt môn học {course.course_name}"
    message = f"Chào {student.full_name},\n\nBạn đã vắng mặt quá 3 buổi học trong môn {course.course_name}. Vui lòng liên hệ giảng viên để giải quyết.\n\nTrân trọng."
    recipient_list = [student.email]

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    messages.success(request, f"Đã gửi email cảnh cáo đến {student.full_name}.")
    return redirect('attendance:statistic', account_id=request.user.account_id)