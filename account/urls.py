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
    path('add_new_branch', views.NewBranchView.as_view(), name="add_new_branch")
]