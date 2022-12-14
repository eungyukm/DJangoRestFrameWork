from xml.dom import ValidationErr
from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):

        email_exists = User.objects.filter(email=attrs['email']).exists()

        if email_exists:
            raise ValidationErr("Email has already been used")

        return super().validate(attrs)

    def create(self, vaidated_data):
        password = vaidated_data.pop("password")

        user = super().create(vaidated_data)
        user.set_password(password)

        user.save()

        Token.objects.create(user=user)

        return user


class CurrentUserPostsSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'posts']
