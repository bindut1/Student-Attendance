from django.db import models
from cloudinary.models import CloudinaryField

class Account(models.Model):
    account_id = models.CharField(max_length=50, primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, blank=True, null=True)
    gender = models.BooleanField(default=True)
    avatar = models.URLField(max_length=500, blank=True, null=True)
    faculty = models.CharField(max_length=100, blank=True, null=True)
    class_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    flag = models.BooleanField(default=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


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


class Attendance(models.Model):
    attendance_id = models.CharField(max_length=50, primary_key=True)
    student = models.ForeignKey(Account, on_delete=models.CASCADE)
    check_in_time = models.TimeField()
    check_in_date = models.DateField()
    status = models.BooleanField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Image(models.Model):
    image_id = models.CharField(max_length=50, primary_key=True)
    student = models.ForeignKey(Account, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=255)

class Feature(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    vector = models.TextField(500)