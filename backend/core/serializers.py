from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Equipment, Dataset
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'equipment_type', 'flowrate', 'pressure', 'temperature']

class DatasetSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=True, read_only=True)
    class Meta:
        model = Dataset
        fields = ['id', 'filename', 'uploaded_at', 'total_count', 'avg_flowrate', 'avg_pressure', 'avg_temperature', 'equipment']
    