from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.models import Subject
from attendance.serializers import SubjectSerializer
from rest_framework import generics

'''
class SubjectAPIView(APIView):
    def get(self,request):
        subject_data = Subject.objects.all()
        return Response({'posts': SubjectAPIView(subject_data, many=True).data})
'''

class SubjectAPIView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer