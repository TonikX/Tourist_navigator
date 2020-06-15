from django.http import Http404
from rest_framework import permissions, generics
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .PathFinderClass import FindRoute

from .serializers import *


class MapObjectView(ListAPIView):
    '''
        Получение  информации об объектах (можно получить объекты содержащие определнные типы если через "_" вводить их id)
    '''
    serializer_class = MapObjectSerializer

    def get_queryset(self):
        if ('pk' in dict(self.kwargs)):
            if ('_' in str(self.kwargs['pk'])):
                name = self.kwargs['pk'].split('_')
                for i in range(len(name)):
                    if name[i].isalpha():
                        raise Http404
                return MapObject.objects.filter(object_type__in=name).order_by("object_type")
            elif (str(self.kwargs['pk']).isnumeric()):
                return MapObject.objects.filter(object_type=self.kwargs['pk']).order_by("object_type")
            else:
                raise Http404
        else:
            return MapObject.objects.all().order_by('id')


class RouteView(ListAPIView):
    '''
    Получение  информации о всех точках в пути по айди (в порядке нумерации точек)
    '''
    serializer_class = RouteCompositionSerializer

    def get_queryset(self):
        return RouteComposition.objects.filter(route_id=self.kwargs['pk']).order_by('obj_position')


class UserRoutesView(ListCreateAPIView):
    '''
    Получение  информации о всех созданных маршрутах конкретным пользователем и добавление последних
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
    serializer_class = TouristClassSerializer

    def get_queryset(self):
        return TouristClass.objects.all().order_by('id')

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()


class RoutePointView(generics.ListCreateAPIView):
    '''
    Добавление и просмотр отдельных точек
    '''
    serializer_class = RouteCompositionSerializer

    def get_queryset(self):
        return RouteComposition.objects.all().order_by('route_id_id')

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()


class RoutePointCreateView(generics.RetrieveUpdateAPIView):
    serializer_class = RouteCompositionSerializer
    queryset = RouteComposition

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save()

class RouteGenerateView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        arrayCoord=request.data['array']
        newroute = FindRoute(arrayCoord)
        response=newroute.solveTSP()
        if response==1:
            return Response({"route:": "Error! One or more points are unreachable"})
        else:
            return Response({"route:": response})