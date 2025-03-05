from django.http import Http404
from django.db import models
from attendance.models import Account, ClassSchedule
from django.shortcuts import render, get_object_or_404, redirect
from attendance.forms import StudentForm
from datetime import datetime

def student_info(request):
    try:
        student = Account.objects.filter(role='student').first()  # Lấy sinh viên đầu tiên
        if not student:
            raise Http404("Không tìm thấy thông tin sinh viên")
        context = {
            'student': student,
            'message': 'Thông tin cá nhân của bạn'
        }
        return render(request, 'student/dashboard.html', context)
    except Http404 as e:
        return render(request, 'student/dashboard.html', {
            'error': str(e),
            'message': 'Lỗi truy xuất thông tin'
        })


def student_edit(request, account_id):
    student = get_object_or_404(Account, account_id=account_id, role='student')

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_info')
    else:
        form = StudentForm(instance=student)

    return render(request, 'student/edit.html', {'form': form, 'student': student})


def student_search(request):
    query = request.GET.get('q', '').strip()  # Lấy giá trị tìm kiếm từ URL
    students = Account.objects.all()

    if query:
        students = students.filter(
            models.Q(email__icontains=query) |
            models.Q(full_name__icontains=query) |
            models.Q(phone_number__icontains=query)
        )

    return render(request, 'student/search.html', {'students': students, 'query': query})


def student_schedule(request, account_id):
    # Get student information
    student = get_object_or_404(Account, account_id=account_id, role='student')

    # Get current day of the week
    current_day = datetime.now().strftime('%A')

    # Lay luon du lieu cua FK, tranh truy van nhieu lan
    schedules = ClassSchedule.objects.filter(
        student_id=student.account_id
    ).select_related('course')

    # Filter courses based on the current day of the week
    courses_today = []
    for schedule in schedules:
        course = schedule.course
        # Check if the current day is in the course's weekdays
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