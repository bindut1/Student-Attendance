from django.db import models
from accounts.models import Account

class Course(models.Model):
    course_id = models.CharField(max_length=50, primary_key=True)
    course_name = models.CharField(max_length=100)
    instructor = models.ForeignKey(Account, on_delete=models.CASCADE)
    student_count = models.IntegerField()
    weekdays = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    room = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class ClassSchedule(models.Model):
    schedule_id = models.CharField(max_length=50, primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Account, on_delete=models.CASCADE)
