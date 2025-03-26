from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime
from attendance.models import Account, Course
from courses.models import ClassSchedule
from django.shortcuts import get_object_or_404
    
@login_required
def student_schedule(request, account_id):
    student = request.user

    current_day = datetime.now().strftime('%A')

    # Lay luon du lieu cua FK, tranh truy van nhieu lan
    schedules = ClassSchedule.objects.filter(
        student_id=student.account_id
    ).select_related('course')

    courses_today = []
    for schedule in schedules:
        course = schedule.course
        if current_day.lower() in course.weekdays.lower():
            courses_today.append({
                'course_name': course.course_name,
                'start_time': course.start_time,
                'end_time': course.end_time,
                'room': course.room,
                'weekdays': course.weekdays
            })
    context = {
        'student': student,
        'courses_today': courses_today,
        'current_day': current_day
    }
    return render(request, 'student/schedule.html', context)

@login_required
def instructor_schedule(request, account_id):
    instructor = get_object_or_404(Account, account_id=account_id)
    current_day = datetime.now().strftime('%A')  # ví dụ: 'Monday'

    schedules = Course.objects.filter(instructor=instructor)

    courses_today = []
    for schedule in schedules:
        if current_day.lower() in schedule.weekdays.lower():  # weekdays là "Monday, Wednesday"
            courses_today.append({
                'course_id': schedule.course_id,
                'course_name': schedule.course_name,
                'start_time': schedule.start_time,
                'end_time': schedule.end_time,
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
    students = ClassSchedule.objects.filter(course=course)
    return render(request, 'templates/instructor/student_list.html', {
        'course': course,
        'students': students
    })