from django.db.models import Max
from rest_framework import serializers, viewsets

from .models import *
class IndividualRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualRoute
        fields = ('id', 'route_user', 'comment')


class TouristClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristClass
        fields = '__all__'


class userProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с акканутами"""
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


class RouteCompositionSerializer(serializers.ModelSerializer):
    #map_id = MapObjectSerializer(many=False, read_only=True)
    class Meta:
        model = RouteComposition
        fields = '__all__'

    def create(self, validated_data):
        object_postion_max = RouteComposition.objects.filter(route_id=validated_data['route_id']).aggregate(Max('obj_position'))
        validated_data['obj_position']=int(object_postion_max['obj_position__max'])+1
        route_point = RouteComposition.objects.create(**validated_data)
        route_point.save()
        return route_point
    def to_representation(self, value):
        self.fields['map_id']=MapObjectSerializer(many=False, read_only=True)
        return super().to_representation(value)