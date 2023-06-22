from django.contrib.auth.models import User
from account.models import *

class AccountManager:
    def get_user_details(self, user_id):
        if user_id:
            office = Office.objects.filter(
                staff=user_id,
                is_active=True, 
                is_deleted=False
            ).first()
            
            if office:
                return office
            else:
                return None
        else:
            return None
            