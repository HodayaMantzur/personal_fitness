# workouts/urls.py
from django.urls import path
from . import views

urlpatterns = [
   # path('', views.workout_list, name='workout_list'),               # רשימת אימונים
#    path('<int:pk>/', views.workout_detail, name='workout-detail'),   # פרטי אימון מסוים
 #   path('<int:pk>/update/', views.workout_update, name='workout-update'), # עדכון אימון
 #   path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
 #   path('workouts/', views.workout_list, name='workouts'),
    path('list/', views.workout_list, name='workout_list'),  # דף עם רשימת אימונים
    path('add/', views.add_workout, name='add_workout'),  # הוספת אימון חדש

    # נתיבים נוספים אם יש צורך
]
