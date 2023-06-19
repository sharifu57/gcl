from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.db.models.query_utils import Q
from django.contrib.auth import authenticate, login
from django.core.validators import EmailValidator
from account.models import *

class AuthenticationForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    class Meta:
        model = User
        fields = ["username","email","password"]


    def clean(self):
        username = str(self.cleaned_data.get("username")).strip().replace(" ", "").lower()
        password = str(self.cleaned_data.get("password")).strip().replace(" ", "").lower()

        if User.objects.filter(Q(username=username)| Q(email=username) | Q(password = password)).exists():
            user_login = User.objects.filter(Q(username=username)|Q(email=username)).first()
            user = authenticate(username = user_login.username, password = password)
            if not user or not user.is_active:
                raise forms.ValidationError("username or password not active")
            
        else:
            raise forms.ValidationError("Invalid username or password")
            

    def login(self, request):
        username = str(self.cleaned_data.get("username")).strip().replace(" ", "").lower()
        password = str(self.cleaned_data.get("password")).strip().replace(" ", "").lower()
        
        if User.objects.filter(Q(username=username) | Q(email=username)).exists():
            user_obj = User.objects.filter(Q(username=username) | Q(email = username)).first()
            user = authenticate(username = user_obj.username, password=password)

        else:
            return None

        return user

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['password'].required = True 
        
        
class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['capital', 'office']
        
        
    def __init__(self, *args, **kwargs):
        super(BusinessForm, self).__init__(*args, **kwargs)
        # self.fields['cash_capital'].required = True
        # self.fields['float_capital'].required = False
        self.fields['office'].required = True
        self.fields['capital'].required = True
   
    
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['business','amount', 'amount_type','tag']
        
    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['amount'].required = True
        self.fields['amount_type'].required = True
        self.fields['tag'].required = True
    

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name']
        
    def __init__(self, *args, **kwargs):
        super(BranchForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        
class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        
        
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data['password1'])
    #     if commit:
    #         user.save()
    #     return user
        