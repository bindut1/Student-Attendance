from django.http import Http404
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from attendance.models import Course, Account, ClassSchedule
from attendance.forms import FormHelper
from django.shortcuts import render, get_object_or_404, redirect
import cloudinary
import cloudinary.uploader

@login_required
def instructor_info(request):
    try:
        instructor = request.user
        if request.user.role != 'instructor':
            raise Http404("Không tìm thấy thông tin sinh viên")
        context = {
            'instructor': instructor,
            'message': 'Thông tin cá nhân của bạn'
        }
        return render(request, 'teacher/dashboard.html', context)
    except Http404 as e:
        return render(request, 'teacher/dashboard.html', {
            'error': str(e),
            'message': 'Lỗi truy xuất thông tin'
        })


@login_required
def instructor_edit(request, account_id):
    instructor = request.user

    if request.method == 'POST':
        form = FormHelper(request.POST, request.FILES, instance=instructor)
        if form.is_valid():
            if 'avatar' in request.FILES:
                avatar = request.FILES['avatar']
                cloudinary_response = cloudinary.uploader.upload(
                    avatar,
                    folder='instructor_avatars',
                    transformation=[
                        {'width': 300, 'height': 300, 'crop': 'fill'},
                        {'radius': 'max'}
                    ]
                )
                instructor.avatar = cloudinary_response['secure_url']

            instructor = form.save(commit=False)
            instructor.password = Account.objects.get(pk=instructor.pk).password
            instructor.save()
            return redirect('instructor_info')
    else:
        form = FormHelper(instance=instructor)

    return render(request, 'teacher/edit.html', {
        'form': form,
        'instructor': instructor
    })


@login_required
def instructor_search(request):
    query = request.GET.get('q')
    users = None
    if query:
        users = Account.objects.filter(full_name__icontains=query)

    return render(request, 'teacher/search.html', {
        'users': users,
        'query': query
    })


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

    return render(request, 'teacher/schedule.html', {
        'instructor': instructor,
        'courses_today': courses_today,
        'current_day': current_day
    })


@login_required
def student_list_by_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    students = ClassSchedule.objects.filter(course=course)

    return render(request, 'teacher/student_list.html', {
        'course': course,
        'students': students
    })
