# workouts/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Workout
from .serializers import WorkoutSerializer
from django.utils.timezone import now

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # רק משתמשים מחוברים יוכלו לגשת
def workout_list(request):
    workouts = Workout.objects.filter(user=request.user)
    serializer = WorkoutSerializer(workouts, many=True)

    total_classes_available = request.user.total_classes_available()
    completed_workouts = request.user.completed_workouts_count()
    missed_workouts = request.user.missed_workouts_count()

    return Response({
        'workouts': serializer.data,
        'total_classes_available': total_classes_available,
        'completed_workouts': completed_workouts,
        'missed_workouts': missed_workouts
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
