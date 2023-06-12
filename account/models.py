from django.db import models
from django.contrib.auth.models import Group, User

# Create your models here.
class MainModel(models.Model):
    is_active = models.BooleanField(null=True, blank=True, default=True)
    is_deleted = models.BooleanField(null=True, blank=True, default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def softdelete(self):
        self.is_deleted = True
        self.is_active = False
        self.updated = pendulum.now()
        self.save()

    class Meta:
        abstract = True
        
class Business(MainModel):
    cash_capital = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    float_capital = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        
        return self.id
    
class Transaction(MainModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    