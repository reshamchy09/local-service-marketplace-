from django.contrib import admin
from app.models import FAQ

# Register your models here.
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    search_fields = ('question',)
    list_filter = ('created_at',)