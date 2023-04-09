from rest_framework.generics import ListAPIView

from attendance.models import Group
from attendance.serializers import GroupSerializer


class GroupAPIView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
