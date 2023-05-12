from django.contrib.auth.models import User
from rest_framework import serializers

from courses.models import Classroom, Avatar


class AddUserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['user_id']


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'groups', 'is_staff', 'is_superuser', 'is_active']


class ClassroomSerializer(serializers.ModelSerializer):
    students = UserSerializer(many=True, read_only=True)
    teachers = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'name', 'description', 'students', 'teachers']


class AvatarSerializer(serializers.ModelSerializer):
    account = UserSerializer(read_only=True)

    class Meta:
        model = Avatar
        fields = ['id', 'account', 'image']
