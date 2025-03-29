from django import forms
from attendance.models import Account

class FormHelper(forms.ModelForm):
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )

    class Meta:
        model = Account
        fields = ['full_name', 'gender', 'faculty', 'class_name', 'email', 'phone_number']