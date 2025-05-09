from django.db import models
from accounts.models import Account      
from courses.models import Course

class Attendance(models.Model):
    attendance_id = models.CharField(max_length=50, primary_key=True)
    student = models.ForeignKey(Account, on_delete=models.CASCADE)
    check_in_time = models.TimeField()
    check_in_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    check_in_latitude = models.FloatField(null=True, blank=True)
    check_in_longitude = models.FloatField(null=True, blank=True)