from django.contrib import admin

# Register your models here.
from .models import Account, Attendance, ClassSchedule, Course, Image

# class CourseAdmin(admin.ModelAdmin):
#     list_display = []

admin.site.register(Account)
admin.site.register(Attendance)
admin.site.register(Course)
admin.site.register(ClassSchedule)