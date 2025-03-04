from django.http import Http404
from django.db import models
from attendance.models import Account
from django.shortcuts import render, get_object_or_404, redirect
from attendance.forms import StudentForm

def student_info(request):
    try:
        student = Account.objects.filter(role='Student').first()  # Lấy sinh viên đầu tiên
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
    student = get_object_or_404(Account, account_id=account_id)

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