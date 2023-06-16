from celery.task import periodic_task
from datetime import timedelta
from account.models import *
from django.db.models import User
from celery import shared_task
import pendulum 
import time

@shared_task
def assign_default_office():
    users = User.objects.all()
    
    for user in users:
        if not Office.objects.filter(user=user).exists():
            default_office = Office.objects.create(user=user,office="1")
            print("--------default office")
            print(default_office)
            default_office.save()
        else:
            pass
    