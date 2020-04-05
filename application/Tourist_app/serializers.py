from rest_framework import serializers, viewsets

from .models import *


class TouristClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristClass
        fields = '__all__'


class userProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с акканутами"""
    user = serializers.StringRelatedField(read_only=True)
    user_class = TouristClassSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class ObjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjType
        fields = '__all__'


class MapObjectSerializer(serializers.ModelSerializer):
    object_type = ObjectTypeSerializer(many=True, read_only=True)

    class Meta:
        model = MapObject
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    map_id = MapObjectSerializer(many=False, read_only=True)

    class Meta:
        model = RouteComposition
        fields = '__all__'
