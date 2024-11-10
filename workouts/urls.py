from django.urls import path
from . import views

urlpatterns = [
    path('', views.workout_list, name='workout-list'),
    path('<int:pk>/', views.workout_list, name='workout-detail'),
    path('create/', views.workout_create, name='workout-create'),
    path('<int:pk>/update/', views.workout_update, name='workout-update'),
    path('<int:pk>/delete/', views.workout_delete, name='workout-delete'),
]
