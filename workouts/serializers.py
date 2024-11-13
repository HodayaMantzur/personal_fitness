# workouts/serializers.py
from rest_framework import serializers
from .models import Workout

class WorkoutSerializer(serializers.ModelSerializer):
    is_today = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = ['id', 'user', 'date', 'completed', 'is_today', 'calories_burned']

    def get_is_today(self, obj):
        return obj.completed_today()
