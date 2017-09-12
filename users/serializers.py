from rest_framework import serializers
from .models import User

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'bio', 'birth_date', 'preferences', 'avatar_url', 'date_joined')
