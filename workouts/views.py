# workouts/views.py
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Workout
from .serializers import WorkoutSerializer
from django.utils.timezone import now
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import CustomTokenObtainPairSerializer
from django.shortcuts import render
from datetime import date




def workout_list_view(request):
    return render(request, 'workouts.html')  # החזר את קובץ ה-HTML

def login(request):
    return render(request, 'login.html')

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class WorkoutListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # כאן תקבל את האימונים על פי המשתמש שנכנס
        return Workout.objects.filter(user=self.request.user)
    
    serializer_class = WorkoutSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # רק משתמשים מחוברים יוכלו לגשת
def workout_list(request):
    today = date.today()
    workouts = Workout.objects.filter(user=request.user).order_by('date')
    serializer = WorkoutSerializer(workouts, many=True)

    total_classes_available = request.user.total_classes_available()
    completed_workouts = request.user.completed_workouts_count()
    missed_workouts = request.user.missed_workouts_count()
    


    return Response({
        'workouts': serializer.data,
        'total_classes_available': total_classes_available,
        'completed_workouts': completed_workouts,
        'missed_workouts': missed_workouts,
        'today': today
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def workout_detail(request, pk):
    try:
        workout = Workout.objects.get(pk=pk, user=request.user)
    except Workout.DoesNotExist:
        return Response({'error': 'Workout not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)

    serializer = WorkoutSerializer(workout)
    total_classes_available = request.user.total_classes_available()
    completed_workouts = request.user.completed_workouts_count()
    missed_workouts = request.user.missed_workouts_count()

    return Response({
        'workout': serializer.data,
        'total_classes_available': total_classes_available,
        'completed_workouts': completed_workouts,
        'missed_workouts': missed_workouts
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_workout(request):
    """
    פונקציה להוספת אימון חדש למשתמש המחובר.
    מצפה לנתונים כמו תאריך, משך זמן, שריפת קלוריות ועוד.
    """
    serializer = WorkoutSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)  # מקשר את האימון למשתמש המחובר
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def workout_update(request, pk):
    try:
        workout = Workout.objects.get(pk=pk, user=request.user)
    except Workout.DoesNotExist:
        return Response({'error': 'Workout not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)

    workout.completed = request.data.get('completed', workout.completed)
    workout.calories_burned = request.data.get('calories_burned', workout.calories_burned)
    workout.save()

    serializer = WorkoutSerializer(workout)
    return Response(serializer.data)