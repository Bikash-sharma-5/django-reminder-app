# reminder/forms.py

from django import forms
from django.contrib.auth.models import User


from .models import Reminder

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['message', 'remind_at', 'remind_via', 'phone_number', 'email']
class RegistrationForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
