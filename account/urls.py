from django.urls import path
from . import views
from django.conf import settings


urlpatterns = [
    path('', views.AuthenticationView.as_view(), name="login"),
    path(f'{settings.SYSTEM_STATE}/dashboard', views.DashboardView.as_view(), name="dashboard"),
    path(f'{settings.SYSTEM_STATE}/add_new_capital', views.AddCapitalView.as_view(), name="add_new_capital"),
    path(f'{settings.SYSTEM_STATE}/add_transaction/<int:business>/', views.AddNewTransaction.as_view(), name="add_transaction"),
    path(f'{settings.SYSTEM_STATE}/reports', views.ReportBaseView.as_view(), name="reports"),
    path(f'{settings.SYSTEM_STATE}/logout', views.LogoutView.as_view(), name="logout"),
    path(f'{settings.SYSTEM_STATE}/branches', views.BranchesView.as_view(), name="branches"),
    path(f'{settings.SYSTEM_STATE}/add_new_branch', views.NewBranchView.as_view(), name="add_new_branch"),
    path(f'{settings.SYSTEM_STATE}/system_users', views.UsersView.as_view(), name="system_users"),
    path(f'{settings.SYSTEM_STATE}/transactions', views.TransactionsMadeView.as_view(), name="transactions"),
    path(f'{settings.SYSTEM_STATE}/get_filtered_transactions', views.GetTransactionsView.as_view(), name="get_filtered_transactions"),
    path(f'{settings.SYSTEM_STATE}/add_new_user', views.CreateNewUserView.as_view(), name="add_new_user"),
    path(f'{settings.SYSTEM_STATE}/capitals', views.CapitalBusinessView.as_view(), name="capitals"),
    path(f'{settings.SYSTEM_STATE}/edit_capital/<int:business>', views.EditCapitalView.as_view(), name="edit_capital"),
    path(f'{settings.SYSTEM_STATE}/remove_capital/<int:business>', views.RemoveCapitalView.as_view(), name="remove_capital"),
    path(f'{settings.SYSTEM_STATE}/edit_transaction/<int:transaction>', views.EditTransactionView.as_view(), name="edit_transaction"),
    path(f'{settings.SYSTEM_STATE}/remove_transaction/<int:transaction>', views.RemoveTransactionView.as_view(), name="remove_transaction"),
    path(f'{settings.SYSTEM_STATE}/show_transaction/<int:business>', views.ShowTransactionView.as_view(), name="show_transaction"),
]