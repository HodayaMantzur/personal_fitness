from django.db import models
from django.conf import settings  # ייבוא הגדרת המודל המשתמש ממערכת ההגדרות
from django.utils.timezone import now  # יש לוודא שאתה מייבא את now מ- timezone

class Workout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # עדכון ל- AUTH_USER_MODEL
    date = models.DateField()
    completed = models.BooleanField(default=False)  # שדה המצביע אם האימון בוצע
    calories_burned = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.name} ({self.user.id_number}) - {self.date}"  # הצגת שם המשתמש ומספר הזהות

    def completed_today(self):
        return self.date == now().date()