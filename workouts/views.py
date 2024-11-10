# workouts/views.py
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Workout
from .serializers import WorkoutSerializer
from users.models import User

# הצגת כל האימונים של המשתמש
@api_view(['GET'])
def workout_list(request):
    """
    מחזיר את רשימת האימונים של המשתמש המחובר
    """
    if request.method == 'GET':
        workouts = Workout.objects.filter(user=request.user)
        serializer = WorkoutSerializer(workouts, many=True)
        # מחשבים את האימונים שנשארו למנוי
        remaining_classes = sum(1 for workout in workouts if not workout.completed)
        return Response({'workouts': serializer.data, 'remaining_classes': remaining_classes})

# יצירת אימון חדש
@api_view(['POST'])
def workout_create(request):
    """
    יצירת אימון חדש
    """
    if request.method == 'POST':
        serializer = WorkoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # נשייך את האימון למשתמש המחובר
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# עדכון אימון קיים
@api_view(['PUT'])
def workout_update(request, pk):
    """
    עדכון אימון קיים
    """
    try:
        workout = Workout.objects.get(pk=pk, user=request.user)
    except Workout.DoesNotExist:
        return Response({'error': 'Workout not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = WorkoutSerializer(workout, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# מחיקת אימון
@api_view(['DELETE'])
def workout_delete(request, pk):
    """
    מחיקת אימון
    """
    try:
        workout = Workout.objects.get(pk=pk, user=request.user)
    except Workout.DoesNotExist:
        return Response({'error': 'Workout not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        workout.delete()
        return Response({'message': 'Workout deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
