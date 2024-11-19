from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from datetime import datetime
from django.shortcuts import render
from .serializers import CustomTokenObtainPairSerializer, UserSerializer



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

def login_view(request):
    return render(request, 'login.html')


def index(request):
    return render(request, 'index.html')

# def admin_view(request):
#     users = User.objects.all()
#     users_data = [
#         {
#             'id_number': user.id_number,
#             'name': user.name,
#             'email': user.email,
#             'phone_number': user.phone_number,
#             'workouts_count': user.workouts.count(),
#             'completed_workouts': user.workouts.filter(status='completed').count(),
#         }
#         for user in users
#     ]
#     print(users_data)  # הדפסת הנתונים כדי לבדוק אם הם מוגשים נכון
#     return JsonResponse(users_data, safe=False)

class AdminListView(APIView):
    def get(self, request):
        try:
            # שלוף את כל המנויים
            users = User.objects.all()
            # השתמש בסריאליזר להמיר את המשתמשים לפורמט JSON
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except Exception as e:
            # אם יש שגיאה כלשהי, מחזירים תשובה עם קוד שגיאה 500
            print(f"Error: {str(e)}")  # הדפס את השגיאה בקונסול של השרת
            return Response({"error": str(e)}, status=500)
        
# Serializer מותאם אישית להפקת Token על פי שם ומספר זהות
class CustomTokenObtainPairSerializer(serializers.Serializer):
    id_number = serializers.CharField()
    name = serializers.CharField()

    def validate(self, attrs):
        id_number = attrs.get('id_number')
        name = attrs.get('name')

        # נוודא שהמשתמש קיים לפי שם ומספר זהות
        try:
            user = User.objects.get(id_number=id_number, name=name)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')

        # יצירת טוקן על פי המשתמש
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }

# View מותאם אישית לשימוש ב- Token
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({'message': 'המנוי נמחק בהצלחה!'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'error': 'המנוי לא נמצא'}, status=404)

@csrf_exempt  # להסרת בדיקת CSRF - נדרש רק לפיתוח, לא לפרודקשן
@api_view(['POST'])
@permission_classes([AllowAny])  # מאפשר גישה ללא אימות
def create_user(request):
    if request.method == 'POST':
        try:
            # ניתוח הנתונים מתוך בקשת JSON
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            phone_number = data.get('phone_number')
            id_number = data.get('id_number')  # הוספת id_number
            age = data.get('age')
            subscription_valid_until = data.get('subscription_valid_until')
            days_per_week = data.get('days_per_week', 0)  # ברירת מחדל ל-0 אם לא נשלח
            weight = data.get('weight')
            height = data.get('height')


            # המרת התאריך מ- str ל- datetime.date
            try:
                subscription_valid_until = datetime.strptime(subscription_valid_until, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'error': 'תאריך לא חוקי'}, status=400)

            # בדיקה האם כל השדות החיוניים הוזנו
            if not all([name, email, subscription_valid_until, id_number]):
                return JsonResponse({'error': 'חסרים נתונים חיוניים ליצירת משתמש'}, status=400)

            # בדיקה אם id_number כבר קיים במערכת
            if User.objects.filter(id_number=id_number).exists():
                return JsonResponse({'error': 'מספר הזהות קיים כבר במערכת'}, status=400)

            # הוספת אימות לשדות נוספים, אם נדרש
            if days_per_week < 1 or days_per_week > 3:
                return JsonResponse({'error': 'מספר האימונים בשבוע חייב להיות בין 1 ל-3'}, status=400)
            
            if age and age < 0:
                return JsonResponse({'error': 'גיל לא יכול להיות שלילי'}, status=400)
            
            if weight and weight <= 0:
                return JsonResponse({'error': 'משקל לא יכול להיות שלילי או 0'}, status=400)

            if height and height <= 0:
                return JsonResponse({'error': 'גובה לא יכול להיות שלילי או 0'}, status=400)

            # יצירת המנוי במערכת
            user = User.objects.create(
                name=name,
                email=email,
                phone_number=phone_number,
                id_number=id_number,  # הוספת id_number
                age=age,
                subscription_valid_until=subscription_valid_until,
                days_per_week=days_per_week,
                weight=weight,
                height=height,
                start_date=datetime.today().date(),  # הנחה שהמנוי מתחיל בתאריך הנוכחי
                end_date=subscription_valid_until,  # התוקף עד התאריך שנמסר
            )

            return JsonResponse({
                'message': 'המשתמש נוצר בהצלחה!',
                'user': {
                    'name': user.name,
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'age': user.age,

                    'days_per_week': user.days_per_week,
                },
                'subscription': {
                    'start_date': user.start_date,
                    'end_date': user.subscription_valid_until,
                    'total_classes_available': user.total_classes_available(),
                    'missed_workouts_count': user.missed_workouts_count(),
                }


            })
        except Exception as e:
            return JsonResponse({'error': f"שגיאה: {str(e)}"}, status=400)

    return JsonResponse({'error': 'Request method not allowed'}, status=405)
