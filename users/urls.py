# ב-urls.py של אפליקציית users
from django.urls import path
from . import views
from .views import CustomTokenObtainPairView , login_view




urlpatterns = [
    path('create/', views.create_user, name='create_user'),  # URL ליצירת מנוי חדש
    # path('login/', CustomTokenObtainPairView.as_view(), name='login'),
  #  path('login/', login_view, name='login'),

 #  path('success/', views.success_page, name='success_page'),  # דף הצלחה

]
