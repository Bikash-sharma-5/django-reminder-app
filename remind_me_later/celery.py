# remind_me_later/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default settings for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'remind_me_later.settings')

# Create Celery app
app = Celery('remind_me_later')

# Load config from Django settings, using `CELERY_` namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()
