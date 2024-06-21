from .models import BoardModel
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardModel
        fields = '__all__'