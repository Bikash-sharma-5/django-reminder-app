# reminder/models.py
from django.db import models
from django.contrib.auth.models import User

class Reminder(models.Model):
    MESSAGE_CHOICES = [
        ('SMS', 'SMS'),
        ('Email', 'Email'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    remind_at = models.DateTimeField()
    remind_via = models.CharField(max_length=5, choices=MESSAGE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.message} at {self.remind_at}"
