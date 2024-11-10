from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)
    id_number = models.CharField(max_length=9, blank=True, null=True)  # מספר תעודת זהות (9 ספרות)
    days_per_week = models.IntegerField(default=0)  # שדה למספר הימים בשבוע
    subscription_valid_until = models.DateField(default=date.today)  # תאריך תפוגת המנוי
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)  # הוספת את שדה הגיל

    def __str__(self):
        return self.username
    
class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    
    @property
    def total_classes(self):
        """חשב את מספר השיעורים שהמשתמש זכאי להם במהלך תקופת המנוי"""
        duration = (self.end_date - self.start_date).days // 7  # חישוב מספר השבועות
        return self.user.days_per_week * duration

