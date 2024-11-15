from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    id_number = serializers.CharField(write_only=True)  # שדה write_only כך שלא יוחזר ב-Response
    name = serializers.CharField(write_only=True)  # שדה write_only כך שלא יוחזר ב-Response

    def validate(self, attrs):
        # כאן אנו מאמתים את המשתמש לפי id_number וה-name בלבד
        user = get_user_model().objects.filter(id_number=attrs['id_number'], name=attrs['name']).first()
        
        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        # יוצרים את ה-token על פי המשתמש המאומת
        refresh = self.get_token(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
