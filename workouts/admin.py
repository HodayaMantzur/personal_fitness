from django.contrib import admin
from .models import Workout
from django.utils.timezone import now

class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'completed', 'calories_burned', 'remaining_workouts', 'missed_workouts')
    list_filter = ('date', 'completed')

    # כמות האימונים שנותרו בהתאם למנוי
    def remaining_workouts(self, obj):
        return obj.user.total_classes_available()

    remaining_workouts.short_description = 'Remaining Workouts'

    # כמות האימונים שהחסירו
    def missed_workouts(self, obj):
        return obj.user.missed_workouts_count()

    missed_workouts.short_description = 'Missed Workouts'

    # מאפשר עדכון סטטוס של אימון בוצע וקלוריות שנשרפו
    def save_model(self, request, obj, form, change):
        if obj.date == now().date():
            obj.completed = form.cleaned_data.get('completed', obj.completed)
        obj.calories_burned = form.cleaned_data.get('calories_burned', obj.calories_burned)
        super().save_model(request, obj, form, change)

admin.site.register(Workout, WorkoutAdmin)
