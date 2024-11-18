from rest_framework import serializers
from .models import Workout
#from users.serializers import UserSerializer  # סריאלייזר מותאם למשתמש

class WorkoutSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    is_today = serializers.SerializerMethodField()
    total_classes_available = serializers.SerializerMethodField()
    completed_workouts = serializers.SerializerMethodField()
    missed_workouts = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = ['id', 'user', 'date', 'completed', 'is_today', 'calories_burned', 'total_classes_available', 'completed_workouts', 'missed_workouts']

    def get_user(self, obj):
        return {
            "name": obj.user.name,
            "id_number": obj.user.id_number
        }

    def get_is_today(self, obj):
        return obj.completed_today()

    def get_total_classes_available(self, obj):
        # מחשבים את מספר האימונים שנותרו למנוי
        user = obj.user  # משתמש האימון
        return user.total_classes_available()

    def get_completed_workouts(self, obj):
        # מחזירים את מספר האימונים שהמשתמש סיים
        user = obj.user  # משתמש האימון
        return user.completed_workouts_count()

    def get_missed_workouts(self, obj):
        # מחזירים את מספר האימונים שהיו צריכים להתבצע אך לא הושלמו
        user = obj.user  # משתמש האימון
        return user.missed_workouts_count()
