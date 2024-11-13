#URL
from django.urls import path
from . import views

urlpatterns = [
    path('workouts/', views.workout_list, name='workout-list'),  # הצגת כל האימונים
    path('<int:pk>/', views.workout_detail, name='workout-detail'),  # פרטי אימון
    path('<int:pk>/update/', views.workout_update, name='workout-update'),  # עדכון סטטוס אימון
]
