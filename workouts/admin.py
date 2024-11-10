
from django.contrib import admin
from .models import Workout

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'workout_date', 'calories_burned', 'completed')
    search_fields = ('user__name',)
    list_filter = ('workout_date', 'completed')  # פילטר גם לפי סטטוס האימון
