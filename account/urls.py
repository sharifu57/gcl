from django.urls import path
from . import views


urlpatterns = [
    path('', views.AuthenticationView.as_view(), name="login"),
    path('dashboard', views.DashboardView.as_view(), name="dashboard")
]