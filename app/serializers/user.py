"""
   This File will contain Serializers related to users,
   Register,Login and author serializers.

"""

from rest_framework import serializers
from app.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.Serializer):
    """Registeration Serializer"""

    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(allow_null=True, required=False)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        try:
            user = User.objects.create(
                username=validated_data.get("username",None),
                email=validated_data.get("email",None),
                first_name=validated_data.get("first_name",None),
                last_name=validated_data.get("last_name",None),
            )

            user.set_password(validated_data["password"])
            user.save()

            return user
        except Exception as e:
            raise serializers.ValidationError(f'an error occuerd: {e}')


class ReadUserSerializer(serializers.Serializer):
    """This Serializer will be used in other Serializers to retrieve user data"""

    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
