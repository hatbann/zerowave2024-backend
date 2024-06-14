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
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def update(self, instance, validated_data):
        # 5.
        
        # 6.
        for (key, value) in validated_data.items():
            # 7.
            setattr(instance, key, value)


        # 9.
        instance.save()

        return instance
    

class UserProfileSerializer(serializers.ModelSerializer): 
     class Meta:
        model=User
        fields=['id','email','nickname']