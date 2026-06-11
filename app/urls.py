from django import views
from django.urls import path
from .views import home, become_provider, become_dealer, login_view
from . import views

urlpatterns = [
     path("", views.home, name="home"),
      path("provider/<int:pk>/", views.provider_detail, name="provider_detail"),
     path('login/', login_view, name='login'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq_page, name='faq'),
    path('about/', views.about, name='about'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('become-provider/', become_provider, name='become_provider'),
    path('become-dealer/', become_dealer, name='become_dealer'),
        path("services/", views.public_services, name="public_services"),
]