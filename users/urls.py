# ב-urls.py של אפליקציית users
from django.urls import path
from . import views
from .views import CustomTokenObtainPairView , AdminListView


urlpatterns = [
    path('create/', views.create_user, name='create_user'),  # URL ליצירת מנוי חדש
    path('admin/<int:user_id>/', views.delete_user, name='delete_user'),  # הוספת הנתיב למחיקת מנוי
    path('admin/', AdminListView.as_view(), name='admin-list'),  # השתמש ב-AdminListView.as_view()
 
   # path('admin/', admin_view, name='admin-list'),  # יש לקרוא לפונקציה ישירות
 #  path('success/', views.success_page, name='success_page'),  # דף הצלחה

]
