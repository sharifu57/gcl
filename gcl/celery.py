# celery.py

import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gcl.settings')

app = Celery('gcl')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
