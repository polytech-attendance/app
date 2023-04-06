from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Group
from .models import User

from .serializers import GroupSerializer
from .serializers import UserSerializer

# Create your views here.
class GroupAPIView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer