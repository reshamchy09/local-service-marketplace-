from django.urls import path
from .views import dealer_dashboard

urlpatterns = [
    path('dealer/dashboard/', dealer_dashboard, name='dealer_dashboard'),
]