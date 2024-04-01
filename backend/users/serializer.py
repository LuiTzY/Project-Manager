from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("nombre","email","password","created_at","update_at")
        read_only_fields =("created_at","update_at")