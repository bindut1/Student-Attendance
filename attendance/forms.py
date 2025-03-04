from django import forms
from attendance.models import Account

class StudentForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['full_name', 'gender', 'faculty', 'class_name', 'email', 'phone_number']
