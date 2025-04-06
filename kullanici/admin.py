from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'company_name', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'company_name')
    list_filter = ('city', 'created_at')
