from django.db import models
from django.contrib.auth.models import Group, User

# Create your models here.
class MainModel(models.Model):
    is_active = models.BooleanField(null=True, blank=True, default=True)
    is_deleted = models.BooleanField(null=True, blank=True, default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def softdelete(self):
        self.is_deleted = True
        self.is_active = False
        self.updated = pendulum.now()
        self.save()

    class Meta:
        abstract = True
        
class Branch(MainModel):
    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    code = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        
        return self.name
        
class Business(MainModel):
    office = models.ForeignKey("account.Office", on_delete=models.CASCADE, null=True, blank=True)
    cash_capital = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    float_capital = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    capital = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        
        return self.user.username
    

class Office(MainModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    staff = models.ManyToManyField(User, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    code = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        
        return self.name
    

AMOUNT_TYPE = (
    (0, 'CASH ON HAND'),
    (1, 'M-PESA SUPER'), 
    (2, 'M-PESA MINOR'),
    (3, 'TIGO-PESA SUPER'),
    (4, 'TIGO-PESA MINOR'),
    (5, 'AIRTEL MONEY SUPER'),
    (6, 'AIRTEL MONEY MINOR'),
    (7, 'HALO PESA SUPER'),
    (8, 'HALO PESA MINOR'),
    (9, 'PBZ'),
    (10, 'NMB'),
    (11, 'CRDB'),
)

class Transaction(MainModel):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount_type = models.IntegerField(choices=AMOUNT_TYPE, null=True, blank=True, default=None)
    tag = models.IntegerField(choices=((1, 'IN'), (2, 'OUT')), null=True, blank=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        
        return self.staff.id
    