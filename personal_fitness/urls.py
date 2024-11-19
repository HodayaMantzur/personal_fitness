from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import CustomTokenObtainPairView, AdminListView, login_view
from django.views.generic import TemplateView  # אם אתה רוצה להפנות לדף תבנית

urlpatterns = [
    path('admin/', admin.site.urls),
    path('workouts/', include('workouts.urls')),  # כל האימונים כאן
    path('users/', include('users.urls')),  # שמירה על ה-URLs של המשתמשים
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    # path('', TemplateView.as_view(template_name="front/index.html"), name="index"),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
   # path('login/', login_view.as_view(), name='login'),

]
