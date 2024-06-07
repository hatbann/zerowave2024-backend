from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        nickname = validated_data.get('nickname')
        email = validated_data.get('email')
        password = validated_data.get('password')
        last_login = timezone.datetime.now()

        user = User(
            nickname=nickname,
            email=email,
            last_login= last_login
        )
        user.set_password(password)
        user.save()
        return user