from django.db.models import Max
from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import *


class UserView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        users = User.objects.all()
        serializer = userProfileSerializer(users, many=True)
        return Response({"users:": serializer.data})

class MapObjectView(APIView):
    def get(self, request, name):
        print(name)
        name=name.split('_')
        map_objects=MapObject.objects.filter(object_type__in=name)
        serializer = MapObjectSerializer(map_objects, many=True)
        return Response({"objects:": serializer.data})


class RouteView(APIView):
    '''
    Получение  информации о всех точках в пути по айди (в порядке нумерации точек)
    '''
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        # id_route = request.GET.get()
        route_comp = RouteComposition.objects.filter(route_id=pk).order_by('obj_position')
        serializer = RouteCompositionSerializer(route_comp, many=True)
        return Response({"routes:": serializer.data})


class UserRoutesView(APIView):
    '''
    Получение  информации о всех маршрутах пользователя
    '''
    permission_classes = [permissions.AllowAny]
    def get(self, request, pk):
        routes=IndividualRoute.objects.filter(route_user=pk)
        serializer=IndividualRouteSerializer(routes, many=True)
        return Response({"routes:": serializer.data})
    '''
     Добавление маршрута (не точек) передается по адресу айди пользователя (присваивать айди в запросе не надо т.е.)
    '''
    def post(self, request, pk):
        request.data['route_user']=pk
        serializer = IndividualRouteSerializer(data=request.data)
        if serializer.is_valid():
            class_saved = serializer.save()
            return Response({"success": "New Route  created successfully"})


class UserClasses(APIView):
    permission_classes = [permissions.AllowAny]
    '''
      Тестовая вещь
    '''
    def get(self, request):
        classes = TouristClass.objects.all()
        serializer = TouristClassSerializer(classes, many=True)
        return Response({"users_classes:": serializer.data})

    def post(self, request):
        serializer = TouristClassSerializer(data=request.data)
        if serializer.is_valid():
            class_saved = serializer.save()
            return Response({"success": "New Class '{}' created successfully".format(class_saved.class_name)})

class RoutePointView (APIView):
    def get(self, request):
        route_point = RouteComposition.objects.all()
        serializer = RouteCompositionSerializer(route_point, many=True)
        return Response({"route points:": serializer.data})
    def post(self,request):
        '''
        Добавление точки в пути;
        Позицию точки можно не указывать она добавляется автоматически;
        '''
        object_postion_max = RouteComposition.objects.filter(route_id=request.data['route_id']).aggregate(Max('obj_position'))
        request.data['obj_position']=int(object_postion_max['obj_position__max'])+1
        serializer = RouteCompositionSerializer(data=request.data)
        if serializer.is_valid():
            point_saved = serializer.save()
            return Response({"success": "New point created successfully"})
    def put(self, request, pk):
        route_point=RouteComposition.objects.get(pk=pk)
        serializer=RouteCompositionSerializer(route_point, request.data, partial=True)
        if serializer.is_valid():
            point_saved = serializer.save()
            return Response({"success": "Point updated successfully"})


