from django.contrib import admin
from .models import ServiceProfile

@admin.register(ServiceProfile)
class ServiceProfileAdmin(admin.ModelAdmin):
    list_display = ("business_name", "phone", "is_approved", "is_shop")
    list_filter = ("is_approved", "is_shop")
    search_fields = ("business_name", "phone")