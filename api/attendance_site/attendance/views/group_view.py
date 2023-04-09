from rest_framework.generics import ListAPIView
from api.attendance_site.attendance.models import Group
from api.attendance_site.attendance.serializers import GroupSerializer


class GroupAPIView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
