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
    def do_mark(self, prepare_data : dict):
        try:
            student_status = prepare_data.get('status')
            student_id = prepare_data.get('student_id')
            lesson_id = prepare_data.get('lesson_id')
        except KeyError:
            return Response({'error': 'student_id, lesson_id and status are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        default_admin_user = User.objects.get(user_login='admin')

        try:
            Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            return Response({'error': f'student_id : {student_id} doesnt exists'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({'error': f'lesson_id : {student_id} doesnt exists'},
                            status=status.HTTP_400_BAD_REQUEST)

        # MAYBE IMPORTANT make try except : when lesson->subject->group != student->group



        try:
            attendance = Attendance.objects.get(student_id=student_id, lesson_id=lesson_id)
            serializer = AttendancePutPostSerializer(attendance, data=prepare_data, partial=True)
        except Attendance.DoesNotExist:
            attendance = Attendance(student_id=student_id, lesson_id=lesson_id, updated_by=default_admin_user, is_attendend=student_status)
            serializer = AttendancePutPostSerializer(attendance, data=prepare_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        prepare_data = request.data
        return self.do_mark(prepare_data)
