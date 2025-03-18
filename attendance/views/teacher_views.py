from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from attendance.models import Course  
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from attendance.models import Course,Account,ClassSchedule
from attendance.forms import InstructorForm
from django.shortcuts import render, get_object_or_404, redirect
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
        form = InstructorForm(request.POST, request.FILES, instance=instructor)
        if form.is_valid():
            if 'avatar' in request.FILES:
                avatar = request.FILES['avatar']
                # cloudinary_response = cloudinary.uploader.upload(
                #     avatar,
                #     folder='instructor_avatars',
                #     transformation=[
                #         {'width': 300, 'height': 300, 'crop': 'fill'},
                #         {'radius': 'max'}
                #     ]
                # )
                # instructor.avatar = cloudinary_response['secure_url']

            instructor = form.save(commit=False)
            instructor.password = Account.objects.get(pk=instructor.pk).password  
            instructor.save()
            return redirect('instructor_info')
    else:
        form = InstructorForm(instance=instructor)

    return render(request, 'teacher/edit.html', {
        'form': form,
        'instructor': instructor
    })
@login_required
def instructor_search(request):
    query = request.GET.get('q')
    if query:
        instructors = Account.objects.filter(role='instructor').filter(full_name__icontains=query)
    else:
        instructors = Account.objects.filter(role='instructor')
    return render(request, 'teacher/search.html', {
        'instructors': instructors
    })
@login_required
def instructor_schedule(request, account_id):
    # Lấy thông tin giảng viên dựa trên account_id
    instructor = get_object_or_404(Account, account_id=account_id, role='instructor')

    current_day = datetime.now().strftime('%A')

    # Lấy lịch dạy của giảng viên
    schedules = ClassSchedule.objects.filter(
        course__instructor=instructor
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
        'instructor': instructor,
        'courses_today': courses_today,
        'current_day': current_day
    }
    return render(request, 'teacher/schedule.html', context)