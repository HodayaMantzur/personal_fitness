# workouts/models.py
from django.db import models
from users.models import User

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout_date = models.DateTimeField()
    calories_burned = models.FloatField()
    completed = models.BooleanField(default=False)  # שדה לסימון אם האימון בוצע

    def __str__(self):
        return f"{self.user.username} - {self.workout_date}"

    @property
    def remaining_classes(self):
        """חשב את מספר השיעורים שנותרו למנוי"""
        subscription = self.user.subscription
        total_classes = subscription.total_classes
        completed_classes = Workout.objects.filter(user=self.user, completed=True).count()
        return total_classes - completed_classes
