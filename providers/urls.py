from django.urls import path
from . import views
from .views import provider_dashboard, create_service_profile, logout_view, create_post, provider_posts

urlpatterns = [
       path('provider/dashboard/', provider_dashboard, name='provider_dashboard'),
       path("create-profile/", create_service_profile, name="provider_profile"),
        path("create/", views.create_post, name="create_post"),
       path("posts/", views.provider_posts, name="provider_posts"),
       path("edit/<int:pk>/", views.edit_post, name="edit_post"),
       path("delete/<int:pk>/", views.delete_post, name="delete_post"),
       path("logout/", logout_view, name="logout"),
]