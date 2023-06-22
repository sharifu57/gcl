from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from account.forms import *
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import json
import pendulum
from datetime import datetime
import datetime
from django.db.models import Sum
from django.db.models import Q
from account.manager.account_manager import *
import pendulum
import random
from account.models import *
from django.conf import settings
from django.core.mail import send_mail
import string


# Create your views here.
class MainView(View):
    @method_decorator(never_cache)
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
class LogoutView(MainView):
    def get(self, request):
        # Do some stuff
        logout(request)
        # Redirect to some page
        return redirect('login')
    
class AuthenticationView(View):
    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        
        context = {
            'form': form
        }
        return render(request, 'authentication/login.html', context)
    
    
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request.POST)

        if form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                return redirect('dashboard')
                
            else:
                messages.error(request, 'failed')
                return redirect('login')
                
        else:
            messages.error(request, 'failed to Login')
        
            context = {
                'form': form,
                'messages': messages
            }
            return render(request,'authentication/login.html', context)
        
        
class DashboardView(MainView):
    def get(self, request, *args, **kwargs):
        now = pendulum.now()
        start_date = now.start_of('day').date()
        end_date = now.end_of('day').date()
        user = request.user
        office = AccountManager().get_user_details(user)
        business = None
        capital = None
        balance = 0
        
        if office:
            business = Business.objects.filter(
                is_active=True,
                is_deleted=False,
                office=office
                # created__date__range=[start_date, end_date]
            )
        
        else:
            office = Office.objects.get(id=1)
            business = Business.objects.filter(
                is_active=True,
                is_deleted=False,
                office=office
                # created__date__range=[start_date, end_date]
            )
            

        business_id = business.last().id if business else None
        
        cash_amount = business.aggregate(total=Sum('cash_capital'))['total'] if business else 0
        float_amount = business.aggregate(total=Sum('float_capital'))['total'] if business else 0
        
        cash_total = cash_amount or 0
        float_total = float_amount or 0
        result = business.last()
        
        if result is not None:
            capital = result.capital
            
        else:
            capital = 0
        
        transactions = Transaction.objects.filter(
            is_active=True,
            is_deleted=False,
            business=business_id,
            office=office,
            created__date__range=[start_date, end_date]
        ).exclude(
            amount_type = 0
        ).order_by('-created')
        
        total_transactions = transactions.aggregate(total=Sum('amount'))
        
        cash_in_hand = Transaction.objects.filter(
            is_active=True,
            is_deleted=False,
            business=business_id,
            amount_type = 0
        )
        total_cash_in_hand = cash_in_hand.aggregate(total=Sum('amount'))
        
        calculated_cash_amount = total_transactions['total']
        calculated_float_amount = total_cash_in_hand['total']
        if calculated_cash_amount is not None and calculated_float_amount is not None:
            balance = calculated_cash_amount + calculated_float_amount
        
        close_balance = capital - balance
        
      
        context = {
            'cash':cash_amount,
            'float':float_amount,
            'capital':capital,
            'transactions':transactions,
            'business': business_id,
            'total_transactions':total_transactions,
            'office': office,
            'cash_in_hand': total_cash_in_hand,
            'balance': balance,
            "close_balance": close_balance
        }
        return render(request, 'pages/dashboard.html', context)

    
class AddCapitalView(MainView):
    def get(self, request, *args, **kwargs):
        form = BusinessForm()
        
        context = {
            'form': form
        }
        return render(request, 'pages/new_capital.html', context)
    
    def post(self, request, *args):
        context = list()
        form = BusinessForm(request.POST)
        office = Office.objects.filter(
            is_active=True, 
            is_deleted=False,
            staff=request.user.id
        ).first()
        
        if form.is_valid():
            business = Business()
            business.capital = request.POST['capital']
            business.office = office if office else None
            business.user = request.user
            business.save()
            business.refresh_from_db()
            
            info = {
                'status': True, 
                'message': "Uploaded Successfully"
            }
            
            context.append(info)
            return HttpResponse(json.dumps(info))

        else:
            info = {
                'status': False,
                'message': "Failed to Create"
            }
            context.append(info)
            return HttpResponse(json.dumps(info)) 
        

class EditCapitalView(MainView):
    def get(self, request, *args, **kwargs):
        business_id=self.kwargs.get("business")
        business = Business.objects.filter(id=business_id).first()
        form = BusinessForm(instance=business)
        
        context = {
            'form':form,
            'business':business
        }
        return render(request,'pages/edit_capital.html', context)
        
        
    def post(self, request, *args, **kwargs):
        context = list()
        business_id=self.kwargs.get("business")
        business = Business.objects.filter(id=business_id).first()
        
        form = BusinessForm(request.POST, instance=business)
        
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': "Successfully Updated"
            }
            context.append(info)
            return HttpResponse(json.dumps(info))
        
        else:
            info = {
                'status': False,
                'message': "Failed to Update, Please fill the empty fields"
            }
            context.append(info)
            return HttpResponse(json.dumps(info))
        
        
class RemoveCapitalView(MainView):
    def get(self, request, *args, **kwargs):
        business_id=self.kwargs.get("business")
        business = Business.objects.filter(id=business_id).first()
        business.is_active=False
        business.save()
        info = {
            'status': True,
            'message': "Successfully Removed"
        }
        return HttpResponse(json.dumps(info))
        
class AddNewTransaction(MainView):
    def get(self, request, *args, **kwargs):
        form = TransactionForm()
        business = self.kwargs.get('business')
        context = {
            'form': form,
            'business': business
        }
        return render(request, 'pages/add_transaction.html', context)
    
    def post(self, request, *args, **kwargs):
        context = list()
        form = TransactionForm(request.POST)
        business = self.kwargs.get('business')
        
        if business:
            business_id = Business.objects.filter(id=business).first()
        else:
            business_id = None
            
        office = Office.objects.filter(
            is_active=True, 
            is_deleted=False,
            staff=request.user.id
        ).first()
        
        if form.is_valid():
            transaction = Transaction()
            transaction.amount = request.POST['amount']
            transaction.amount_type = request.POST['amount_type']
            # transaction.tag = request.POST['tag']
            transaction.business = business_id
            transaction.staff = request.user
            transaction.office = office if office else None
            transaction.save()
            transaction.refresh_from_db()
            
            info = {
                'status': True, 
                'message': "Success"
            }
            context.append(context)
            return HttpResponse(json.dumps(info))
    
        else:
            info = {
                'status': False,
                'message': "Failed to create"
            }
            
            context.append(context)
            return HttpResponse(json.dumps(info))
        
class BranchesView(MainView):
    def get(self, request):
        branches = Branch.objects.filter(
            is_active=True,
            is_deleted=False
        )
        
        offices = Office.objects.filter(
            is_active=True,
            is_deleted=False
        ).order_by(
            'created'
        )
        
        context = {
            'branches': branches,
            'offices':offices
        }
        return render(request, 'pages/branches.html', context)
    

def generate_branch_code():
    return random.randint(10000,99999)

class NewBranchView(MainView):
    def get(self, request, *args, **kwargs):
        form = BranchForm()
        context = {
            'form': form
        }
        return render(request, 'pages/add_new_branch.html', context)
    
    def post(self, request, *args, **kwargs):
        context = list()
        form = BranchForm(request.POST)
        if form.is_valid():
            branch = Branch()
            branch.name = request.POST['name']
            branch.code = generate_branch_code()
            branch.save()
            branch.refresh_from_db()

            info = {
                'status': True, 
                'message': "Created Successfully"
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        else:
            info = {
                'status': False,
                'message': "Failed to create"
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        
    
class ReportBaseView(MainView):
    def get(self, request, *args, **kwargs):
        
        transactions = Transaction.objects.filter(
            is_active=True, 
            is_deleted=False
        )
        
        context = {
            'transactions': transactions,
            "system_path": settings.DOCUMENT_SYSTEM_IP,
        }
        return render(request, 'reports/index.html', context)
    

class TransactionsMadeView(MainView):
    def get(self, request, *args, **kwargs):
        
        return render(request, 'pages/transactions.html')
    

class GetTransactionsView(MainView):
    def get(self, request, *args, **kwargs):
        user = request.user

        start_date = request.GET.get("start")
        end_date = request.GET.get("end")

        try:
            if start_date:
                start_date = datetime.datetime.strptime(start_date, '%d %B, %Y').date()
            else:
                start_date = pendulum.today().start_of('month').date()

            if end_date:
                end_date = datetime.datetime.strptime(end_date, '%d %B, %Y').date()
            else:
                end_date = pendulum.today().end_of('month').date()
        except ValueError:
            # Handle the invalid date format here
            print("Invalid date format provided")
            start_date = pendulum.today().start_of('month').date()
            end_date = pendulum.today().end_of('month').date()

        transactions = Transaction.objects.filter(
            is_active=True,
            is_deleted=False,
            staff=user,
            created__date__range=[start_date, end_date]
        )

        context = {
            'transactions': transactions,
            'start_date': start_date,
            'end_date': end_date
        }

        return render(request, 'common/getTransactions.html', context)
    
class CapitalBusinessView(MainView):
    def get(self, request, *args, **kwargs):
        businesses = Business.objects.filter(
            is_active=True,
            is_deleted=False,
        ).order_by('-created')[:10]
        
        context = {
            'businesses': businesses
        }
        return render(request, 'pages/capitals.html', context)
    

class UsersView(MainView):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        
        context = {
            'users': users
        }
        return render(request, 'pages/users.html', context)
    

def send_registration_email(email):
    username = None
    message = f'message sending'
    send_mail(
        'Welcome to My Website',
        message,
        'from@example.com',
        [email],
        fail_silently=False,
    )
    
    
def generate_password():
    length=10
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

class CreateNewUserView(MainView):
    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        
        context = {
            'form': form
        }
        return render(request,'pages/add_new_user.html', context)
    
    def post(self, request, *args, **kwargs):
        context = list()
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = User()
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.username = request.POST['username']
            user.email = request.POST['email']
            user.password = generate_password()
            pwd = user.password
            user.save()
            user.refresh_from_db()
            
            info = {
                'status': True,
                'message': "Created Successfully",
            }
            context.append(info)
            return HttpResponse(json.dumps(info))
        else:
            info = {
                'status': Failed,
                'message': "Failed to create"
            }
            context.append(info)
            return HttpResponse(json.dumps(info))
        
class EditCapitalView(MainView):
    def get(self, request, *args, **kwargs):
        business_id=self.kwargs.get("business")
        business = Business.objects.filter(id=business_id).first()
        form = BusinessForm(instance=business)
        
        context = {
            'form':form,
            'business':business
        }
        return render(request,'pages/edit_capital.html', context)
        
        
    def post(self, request, *args, **kwargs):
        context = list()
        business_id=self.kwargs.get("business")
        business = Business.objects.filter(id=business_id).first()
        
        form = BusinessForm(request.POST, instance=business)
        
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': "Successfully Updated"
            }
            context.append(info)
            return HttpResponse(json.dumps(info))
        
        else:
            info = {
                'status': False,
                'message': "Failed to Update, Please fill the empty fields"
            }
            context.append(info)
            return HttpResponse(json.dumps(info))
        
        
class RemoveCapitalView(MainView):
    def get(self, request, *args, **kwargs):
        business_id=self.kwargs.get("business")
        business = Business.objects.filter(id=business_id).first()
        business.is_active=False
        business.save()
        info = {
            'status': True,
            'message': "Successfully Removed"
        }
        return HttpResponse(json.dumps(info))

class EditTransactionView(MainView):
    def get(self, request, *args, **kwargs):
        transaction_id=self.kwargs.get("transaction")
        transaction = Transaction.objects.filter(id=transaction_id).first()
        form=TransactionForm(instance=transaction)
        
        context = {
            'transaction': transaction,
            'form':form
        }
        return render(request, 'pages/edit_transaction.html', context)
    
    def post(self, request, *args, **kwargs):
        context = list()
        transaction_id=self.kwargs.get("transaction")
        transaction = Transaction.objects.filter(id=transaction_id).first()
        form=TransactionForm(request.POST,instance=transaction)
        
        if form.is_valid():
            form.save()
            info = {
                'status': True,
                'message': "Successfully updated Information"
            }
            
            context.append(info)
        else:
            info = {
                'status': False,
                'message': "Failed to update details"
            }
            context.append(info)
        return HttpResponse(json.dumps(context))
    
class RemoveTransactionView(MainView):
    def get(self, request,  *args, **kwargs):
        transaction_id=self.kwargs.get("transaction")
        transaction = Transaction.objects.filter(id=transaction_id).first()
        transaction.is_active=False
        transaction.save()
        info = {
            'status': True,
            'message': "Successfully deleted"
        }
        return HttpResponse(json.dumps(info))
    
class ShowTransactionView(MainView):
    def get(self, request, *args, **kwargs):
        business_id = self.kwargs.get("business")
        business = Business.objects.filter(id=business_id).first()
        transactions = Transaction.objects.filter(
            business=business,
            is_active=True,
            is_deleted=False
        )
        
        context = {
            'transactions': transactions,
            'business': business
        }
        
        return render(request,'pages/show_transactions.html', context)