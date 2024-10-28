# your_project/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventpr.settings')

# Create a Celery application instance
app = Celery('eventpr')

# Load any custom configuration from your Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in the 'tasks.py' file of installed apps
app.autodiscover_tasks()
