from django.contrib.auth import password_validation
from rest_framework import serializers

from .models import Usuario


class RegistroSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
    }  

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def create(self, validated_data):
        return Usuario.objects.create_user(**validated_data)
    
    
class PerfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = ('id', 'email', 'first_name', 'last_name', 'rol')
