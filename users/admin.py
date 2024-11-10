# users/admin.py

from django.contrib import admin
from .models import User, Subscription

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'id_number', 'email', 'phone_number', 'weight', 'days_per_week', 'subscription_valid_until', 'is_active')
    search_fields = ('name', 'email', 'phone_number', 'id_number')
    list_filter = ('is_active', 'subscription_valid_until')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'total_classes')
    
    fieldsets = (
        (None, {
            'fields': ('user',)
        }),
        ('Subscription details', {
            'fields': ('start_date', 'end_date', 'total_classes')
        }),
    )
