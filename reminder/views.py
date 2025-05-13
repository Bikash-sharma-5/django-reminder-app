

from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from .models import Reminder
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm, LoginForm,ReminderForm
from django.contrib import messages
from .serializers import ReminderSerializer
from .tasks import send_reminder_message 
from django.utils.timezone import make_aware

from django.utils.timezone import is_naive
from django.utils import timezone
from datetime import timezone as dt_timezone
from django.contrib.auth import logout


from django.utils.timezone import now
from datetime import timedelta
import logging

# Configure logging
logger = logging.getLogger('reminder')

@login_required
def home(request):
    user_reminders = Reminder.objects.filter(user=request.user)
    return render(request, 'home.html', {'reminders': user_reminders})

def custom_logout_view(request):
    logout(request)
    return redirect('login')  # or any other page
@login_required
def create_reminder(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            # Save but don't commit yet (so we can attach user and process datetime)
            reminder = form.save(commit=False)
            reminder.user = request.user

            # Get raw remind_at from form
            raw_remind_at = form.cleaned_data['remind_at']
            logger.info(f"Raw remind_at from form: {raw_remind_at}")

            # Ensure datetime is aware
            if timezone.is_naive(raw_remind_at):
                logger.debug("Datetime is naive, converting using current timezone.")
                aware_time = timezone.make_aware(raw_remind_at, timezone.get_current_timezone())
            else:
                aware_time = raw_remind_at
            logger.info(f"Reminder saved: {reminder.id}, scheduled for {reminder.remind_at}")
            # Convert to UTC for Celery eta
            reminder_time = aware_time.astimezone(dt_timezone.utc)
            reminder.remind_at = aware_time  # Save in your local time zone if preferred

            # Optional: Don't allow scheduling too close in the past
            if reminder_time < timezone.now() + timedelta(seconds=5):
                logger.warning("Reminder time too close to now. Adjusting by +10 seconds.")
                reminder_time = timezone.now() + timedelta(seconds=10)
                aware_time = reminder_time.astimezone(timezone.get_current_timezone())
                reminder.remind_at = aware_time

            # Save the reminder object
            reminder.save()

            # Log for debugging
            logger.info(f"Reminder saved: {reminder.id}, scheduled for {reminder.remind_at}")
            print("reminder_time (UTC):", reminder_time)
            print("timezone.now() (UTC):", timezone.now())
            print("Seconds until scheduled time:", (reminder_time - timezone.now()).total_seconds())

            # Schedule Celery task
            send_reminder_message.apply_async(
                args=[reminder.id],
                eta=reminder_time
            )

            return redirect('home')
    else:
        form = ReminderForm()

    return render(request, 'create_reminder.html', {'form': form})
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save the user and get the user instance
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})