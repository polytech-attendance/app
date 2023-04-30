import pytz
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from attendance.models import Group, Lesson, Subject, Teacher, Attendance, Student, User
from attendance.serializers import GroupSerializer, LessonSerializer, AttendanceSerializer,AttendancePutPostSerializer
from datetime import datetime, timedelta
from django.utils import timezone
import json

class AttendanceView(APIView):
    def do_mark(self,prepare_data,attendend_status :bool):
        try:
            student_id = prepare_data.pop('student_id')
            lesson_id = prepare_data.pop('lesson_id')
            student_status = prepare_data.pop('status')
        except KeyError:
            return Response({'error': 'student_id, lesson_id and status are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        attendance = Attendance.objects.filter(student__student_id=student_id, lesson__id=lesson_id).first()
        if not attendance:
            return Response({'error': 'Attendance not found'}, status=status.HTTP_404_NOT_FOUND)

        attendance.is_attendend = attendend_status
        default_admin_user = User.objects.get(user_login='admin')
        attendance.updated_by = default_admin_user

        serializer = AttendancePutPostSerializer(attendance, data=prepare_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        prepare_data=request.data
        status=False
        return self.do_mark(prepare_data,status)

    def put(self,request):
        prepare_data=request.data
        status=True
        return self.do_mark(prepare_data,status)
