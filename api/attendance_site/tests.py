from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from attendance.models import Attendance,User,Student,Group,Lesson
from attendance.serializers import AttendancePutPostSerializer

class AttendanceViewTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('Mark students as attend or not')
        self.user = User.objects.create(user_login='admin',user_password='12345')
        #prepare data to correct test

        student = Student.objects.all()[:1]
        lesson = Lesson.objects.get(subject_id__group_id=student.group_id)

        self.correct_data = {
            'student_id' : student.student_id,
            'lesson_id' : lesson.id,
            'status' : 1,
        }


    def test_create_attendance(self):
        response = self.client.post(self.url, self.data, format='json')
        #testing to correct request
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #testing that new data in DB
        old_size = Attendance.objects.count()
        self.assertEqual(Attendance.objects.count(), old_size+1)
        # checking data to equals
        attendance = Attendance.objects.get(lesson_id=response.data['lesson_id'],student_id=response.data['student_id'])
        serializer = AttendancePutPostSerializer(attendance)
        self.assertEqual(response.data, serializer.data)

    def test_update_attendance(self):
        self.client.post(self.url, self.data, format='json')
        #changing status
        self.data['status'] = 0
        #make request
        response = self.client.post(self.url, self.data, format='json')
        #check to correct request
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #size matching
        old_size = Attendance.objects.count()
        self.assertEqual(Attendance.objects.count(), old_size + 1)
        #checking data to equals
        attendance = Attendance.objects.get(lesson_id=response.data['lesson_id'],student_id=response.data['student_id'])
        serializer = AttendancePutPostSerializer(attendance)
        self.assertEqual(response.data, serializer.data)