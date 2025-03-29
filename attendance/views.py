from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from .models import Attendance


@login_required
def attendance_history(request, account_id):
    student = get_object_or_404(Account, account_id=account_id)

    attendance_records = (
        Attendance.objects.filter(student=student)
        .select_related("course")
        .order_by("-check_in_date", "-check_in_time")
    )

    context = {"student": student, "attendance_records": attendance_records}

    return render(request, "student/history.html", context)
