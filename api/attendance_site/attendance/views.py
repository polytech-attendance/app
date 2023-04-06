from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Group
from .serializers import GroupSerializer

# Create your views here.
class GroupAPIView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
