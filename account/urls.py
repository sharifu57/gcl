from django.urls import path
from . import views


urlpatterns = [
    path('', views.AuthenticationView.as_view(), name="login"),
    path('dashboard', views.DashboardView.as_view(), name="dashboard"),
    path('add_new_capital', views.AddCapitalView.as_view(), name="add_new_capital")
]