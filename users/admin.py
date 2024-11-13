from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    # עדכון תצוגת השדות ב- list_display
    list_display = ('id_number', 'name', 'email', 'age', 'weight', 'height', 'is_active', 'day_of_week', 'total_classes_display')
    readonly_fields = ('total_classes_display',)
    list_filter = ('day_of_week',)

    # פונקציה למצגת של total_classes
    def total_classes_display(self, obj):
        return obj.total_classes_available() if obj.total_classes_available() is not None else '0'
    total_classes_display.short_description = 'Total Classes'

    # עדכון שדות ה-fieldsets כך שיכללו את id_number במקום username
    fieldsets = (
        (None, {
            'fields': ('id_number', 'password', 'name', 'last_name', 'email', 'phone_number', 'is_active')
        }),
        ('Subscription details', {
            'fields': ('subscription_valid_until', 'days_per_week', 'start_date', 'end_date')
        }),
        ('Personal details', {
            'fields': ('age', 'weight', 'height')
        }),
    )

admin.site.register(User, UserAdmin)
