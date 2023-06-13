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

# Create your views here.
class MainView(View):
    @method_decorator(never_cache)
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
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
        # now = pendulum.now()
        # start_date = now.start_of('month').date()
        # end_date = now.end_of('month').date()
        business = Business.objects.filter(
            is_active=True,
            is_deleted=False,
            # created__date__range=[start_date,end_data]
        )
        cash_amount = business.aggregate(total=Sum('cash_capital'))
        float_amount = business.aggregate(total=Sum('float_capital'))
        
        cash_total = cash_amount['total'] or 0
        float_total = float_amount['total'] or 0
        capital = cash_total + float_total
        
        transactions = Transaction.objects.filter(
            is_active=True,
            is_deleted=False,
        ).order_by('-created')
        
        business_id = business.last()
        if business_id:
            business_id = business_id.id
        else:
            business_id = None
        print("-----lastly id ", business_id)
      
        context = {
            'cash':cash_amount,
            'float':float_amount,
            'capital':capital,
            'transactions':transactions,
            'business': business_id
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

        if form.is_valid():
            business = Business()
            business.cash_capital = request.POST['cash_capital']
            business.float_capital = request.POST['float_capital']
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