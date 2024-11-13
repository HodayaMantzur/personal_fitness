from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
from django.contrib.auth.models import UserManager

class CustomUserManager(UserManager):
    def create_superuser(self, id_number, password=None, **extra_fields):
        if not id_number:
            raise ValueError('The given id_number must be set')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        user = self.model(id_number=id_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    username = None  # הסרת השדה 'username'
    name = models.CharField(max_length=100, blank=True, null=True)
    id_number = models.CharField(max_length=10, blank=True, null=True, default='0000000000', unique=True)  # שדה ייחודי
    days_per_week = models.IntegerField(default=0)
    subscription_valid_until = models.DateField(default=date.today)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    height = models.FloatField(null=True, blank=True)

    DAY_CHOICES = [
            ('Sun', 'ראשון'),
            ('Mon', 'שני'),
            ('Tue', 'שלישי'),
            ('Wed', 'רביעי'),
            ('Thu', 'חמישי'),
            ('Fri', 'שישי'),
            ('Sat', 'שבת'),
        ]
    
    day_of_week = models.CharField(
            max_length=3, 
            choices=DAY_CHOICES, 
            default='Sun',  # ניתן לשנות את ברירת המחדל אם יש צורך
            blank=True,
            null=True
        )

    USERNAME_FIELD = 'id_number'  # הגדרת 'id_number' כשדה ייחודי
    REQUIRED_FIELDS = ['email', 'name', 'phone_number', 'weight', 'age', 'height']

    objects = CustomUserManager()  # שימוש במנהל מותאם אישית

    def save(self, *args, **kwargs):
        # הגדרת start_date ו-end_date בעת יצירת המנוי
        if not self.start_date:
            self.start_date = date.today()  # הנחה שהמנוי מתחיל בתאריך הנוכחי
        if not self.end_date and self.subscription_valid_until:
            self.end_date = self.subscription_valid_until  # הנחה שהתוקף הוא עד התאריך שניתן
        super().save(*args, **kwargs)

    def total_classes_available(self):
        """מספר האימונים שנותרו למנוי עד סוף התוקף"""
        if self.start_date and self.end_date and self.days_per_week > 0:
            remaining_weeks = max(0, (self.subscription_valid_until - date.today()).days // 7)
            return self.days_per_week * remaining_weeks
        return 0  # מחזיר 0 במידה ואין מספיק נתונים לחישוב

    def completed_workouts_count(self):
        """מספר האימונים שהמשתמש סיים עד היום"""
        return self.workout_set.filter(completed=True).count()  # בהנחה שיש קשר עם מודל האימונים

    def missed_workouts_count(self):
        """מספר האימונים שהיו צריכים להתבצע עד היום אך לא הושלמו"""
        if self.start_date and self.days_per_week > 0:
            weeks_elapsed = (date.today() - self.start_date).days // 7
            expected_workouts = self.days_per_week * weeks_elapsed
            return max(0, expected_workouts - self.completed_workouts_count())
        return 0  # מחזיר 0 אם אין מספיק נתונים לחישוב

    def __str__(self):
        return self.id_number  # כעת מציגים את מספר הזהות במקום שם המשתמש
