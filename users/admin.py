from django.contrib import admin
from .models import User, UserSession, Address

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'user_id', 'created_at']
    search_fields = ['email', 'username', 'user_id']
    list_filter = ['created_at']

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_token', 'expires_at', 'created_at']
    search_fields = ['user__email', 'session_token']
    list_filter = ['created_at', 'expires_at']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'city', 'state', 'is_default']
    search_fields = ['user__email', 'full_name', 'city']
    list_filter = ['state', 'is_default']
