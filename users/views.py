# users/views.py

from datetime import date
from django.shortcuts import render
from django.http import JsonResponse
from .models import User, Subscription

def create_user(request):
    if request.method == 'POST':
        # קבלת הנתונים מהטופס
        name = request.POST.get('name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        subscription_valid_until = request.POST.get('subscription_valid_until')
        days_per_week = request.POST.get('days_per_week')
        
        # יצירת המשתמש החדש
        user = User.objects.create(
            name=name,
            email=email,
            age=age,
            subscription_valid_until=subscription_valid_until,
            days_per_week=days_per_week
        )
        
        # יצירת מנוי חדש למשתמש
        subscription = Subscription.objects.create(
            user=user,
            start_date=date.today(),
            end_date=subscription_valid_until
        )
        
        return JsonResponse({
            'message': 'המשתמש נוצר בהצלחה!',
            'user': {'name': user.name, 'email': user.email},
            'subscription': {
                'start_date': subscription.start_date,
                'end_date': subscription.end_date
            }
        })
    return JsonResponse({'error': 'Request method not allowed'}, status=400)

def success_page(request):
    return render(request, 'users/success.html')  # דף הצלחה
