from rest_framework import serializers
from ..models import User


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'name', 'email', 'role', 'auth_provider')

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
