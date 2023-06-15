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
            print("***valid")
            user = form.login(request)
            if user:
                login(request, user)
                return redirect('dashboard')
                
            else:
                messages.error(request, 'failed')
                return redirect('login')
                
        else:
            print("**not valid")
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
        if office:
            print("----there is office")
            print(office)
            business = Business.objects.filter(
                is_active=True,
                is_deleted=False,
                office=office,
                created__date__range=[start_date, end_date]
            )
            print("-----print business")
            print(business)
            
        else:
            office == 2
            print("-----no office")
            
        business_id = business.last().id if business else None
        print("-----lastly id ", business_id)
        
        cash_amount = business.aggregate(total=Sum('cash_capital'))['total'] if business else 0
        float_amount = business.aggregate(total=Sum('float_capital'))['total'] if business else 0
        
        cash_total = cash_amount or 0
        float_total = float_amount or 0
        capital = business.last().capital
        
        transactions = Transaction.objects.filter(
            is_active=True,
            is_deleted=False,
            business=business_id
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
            is_deleted=False
        ).first()
        
        print("------office:", office)
        
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
            print("------here business")
            print(business)
            business_id = Business.objects.filter(id=business).first()
        else:
            business_id = None
        
        if form.is_valid():
            print("---------valid form")
            transaction = Transaction()
            transaction.amount = request.POST['amount']
            transaction.amount_type = request.POST['amount_type']
            transaction.tag = request.POST['tag']
            transaction.business = business_id
            transaction.staff = request.user
            transaction.save()
            transaction.refresh_from_db()
            
            info = {
                'status': True, 
                'message': "Success"
            }
            context.append(context)
            return HttpResponse(json.dumps(info))
    
        else:
            print("--------invalid form")
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
        
        context = {
            'branches': branches
        }
        return render(request, 'pages/branches.html', context)
    

def generate_branch_code():
    return random.randint(10000,99999)

class NewBranchView(MainView):
    def get(self, request, *args, **kwargs):
        print("-------**** get form")
        form = BranchForm()
        print("-------*** end get form")
        context = {
            'form': form
        }
        return render(request, 'pages/add_new_branch.html', context)
    
    def post(self, request, *args, **kwargs):
        context = list()
        form = BranchForm(request.POST)
        if form.is_valid():
            print("----------isvalid")
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
            print("-----not valid")
            info = {
                'status': False,
                'message': "Failed to create"
            }
            context.append(info)
            return HttpResponse(json.dumps(context))
        
    
        
class ReportBaseView(MainView):
    def get(self, request, *args, **kwargs):
        
        return render(request, 'reports/index.html')