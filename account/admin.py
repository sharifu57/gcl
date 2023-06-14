from django.contrib import admin
from account.models import *

# Register your models here.
admin.site.register(Business)
admin.site.register(Transaction)
admin.site.register(Branch)
admin.site.register(Office)