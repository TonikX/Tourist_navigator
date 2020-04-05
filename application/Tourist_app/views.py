from rest_framework import permissions
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


class RouteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        '''
        routes=route_composition.objects.all()
        serializer=RouteSerializer(routes, many=True)
        return Response({"routes:": serializer.data})
        '''
        id_route = request.GET.get("route")
        route_comp = RouteComposition.objects.filter(route_id=id_route).order_by('obj_position')
        serializer = RouteSerializer(route_comp, many=True)
        return Response({"routes:": serializer.data})


class UserClasses(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        classes = TouristClass.objects.all()
        serializer = TouristClassSerializer(classes, many=True)
        return Response({"users_classes:": serializer.data})

    def post(selfself, request):
        serializer = TouristClassSerializer(data=request.data)
        if serializer.is_valid():
            class_saved = serializer.save()
            return Response({"success": "New Class '{}' created successfully".format(class_saved.class_name)})
