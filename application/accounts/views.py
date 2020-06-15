from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
from rest_framework.permissions import IsAuthenticated
from Tourist_app.models import User
from Tourist_project.permissions import IsOwnerProfileOrReadOnly
from Tourist_app.serializers import UserProfileSerializer

# Create your views here.


class UserProfileListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save()


class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerProfileOrReadOnly, IsAuthenticated]
