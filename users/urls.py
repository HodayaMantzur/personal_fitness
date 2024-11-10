# ב-urls.py של אפליקציית users
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_user, name='create_user'),  # URL ליצירת מנוי חדש
    path('success/', views.success_page, name='success_page'),  # דף הצלחה

]
