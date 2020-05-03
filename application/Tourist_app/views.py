from django.http import Http404
from rest_framework import permissions, generics
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, ListAPIView
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

class MapObjectView(ListAPIView):
    '''
        Получение  информации об объектах (можно получить объекты содержащие определнные типы если через "_" вводить их id)
    '''
    serializer_class = MapObjectSerializer
    def get_queryset(self):
        if('pk' in dict(self.kwargs)):
            if ('_' in str(self.kwargs['pk'])):
                name = self.kwargs['pk'].split('_')
                return MapObject.objects.filter(object_type__in=name)
            elif (str(self.kwargs['pk']).isnumeric()):
                return MapObject.objects.filter(object_type=self.kwargs['pk'])
            else:
                raise Http404
        else:
            return MapObject.objects.all()




class RouteView(ListAPIView):
    '''
    Получение  информации о всех точках в пути по айди (в порядке нумерации точек)
    '''
    serializer_class = RouteCompositionSerializer
    def get_queryset(self):
        return RouteComposition.objects.filter(route_id=self.kwargs['pk']).order_by('obj_position')

class UserRoutesView(ListCreateAPIView):
    '''
    Получение  информации о всех созданных маршрутах и добавление последних
    '''
    serializer_class = IndividualRouteSerializer

    def get_queryset(self):
        return IndividualRoute.objects.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()



class UserClasses(generics.ListCreateAPIView):
    '''
       Получение и добавление типов (тестовая вьюха)
    '''
    permission_classes = [permissions.AllowAny]

    serializer_class = TouristClassSerializer
    def get_queryset(self):
        return TouristClass.objects.all()
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()

class RoutePointView (generics.ListCreateAPIView):
    '''
    Добавление и просмотр отдельных точек
    '''
    serializer_class = RouteCompositionSerializer
    def get_queryset(self):
        return RouteComposition.objects.all().order_by('route_id_id')
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()

