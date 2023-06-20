from django.urls import path
from . import views


urlpatterns = [
    path('', views.AuthenticationView.as_view(), name="login"),
    path('dashboard', views.DashboardView.as_view(), name="dashboard"),
    path('add_new_capital', views.AddCapitalView.as_view(), name="add_new_capital"),
    path('add_transaction/<int:business>/', views.AddNewTransaction.as_view(), name="add_transaction"),
    path('reports', views.ReportBaseView.as_view(), name="reports"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('branches', views.BranchesView.as_view(), name="branches"),
    path('add_new_branch', views.NewBranchView.as_view(), name="add_new_branch"),
    path('system_users', views.UsersView.as_view(), name="system_users"),
    path('transactions', views.TransactionsMadeView.as_view(), name="transactions"),
    path('get_filtered_transactions', views.GetTransactionsView.as_view(), name="get_filtered_transactions"),
    path('add_new_user', views.CreateNewUserView.as_view(), name="add_new_user"),
    path('capitals', views.CapitalBusinessView.as_view(), name="capitals"),
    path('edit_capital/<int:business>', views.EditCapitalView.as_view(), name="edit_capital"),
    path('remove_capital/<int:business>', views.RemoveCapitalView.as_view(), name="remove_capital"),
    path('edit_transaction/<int:transaction>', views.EditTransactionView.as_view(), name="edit_transaction"),
    path('remove_transaction/<int:transaction>', views.RemoveTransactionView.as_view(), name="remove_transaction"),
]