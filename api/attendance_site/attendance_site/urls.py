"""
URL configuration for attendance_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from attendance.views.group_view import GroupAPIView, GroupScheduleView, GroupItemView, GroupAttendanceListView, \
    GroupAttendanceSubjectView
from attendance.views.user_view import UserAPIView
from attendance.views.teacher_view import TeacherAPIView, TeacherScheduleView
from attendance.views.subject_view import SubjectAPIView, SubjectByTeacherAPIView, SubjectAttendanceView
from attendance.views.attendance_view import AttendanceView

from rest_framework import routers

apiTAG = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{apiTAG}users/', UserAPIView.as_view()),
    path(f'{apiTAG}teachers/', TeacherAPIView.as_view()),
    path(f'{apiTAG}teachers/<int:teacher_id>/schedule/', TeacherScheduleView.as_view(), name='Teacher schedule'),
    path(f'{apiTAG}subjects/', SubjectAPIView.as_view()),
    path(f'{apiTAG}groups/', GroupAPIView.as_view(), name='Groups list'),
    path(f'{apiTAG}groups/<int:group_id>/schedule/', GroupScheduleView.as_view(), name='Group week schedule'),
    path(f'{apiTAG}groups/<int:group_id>/', GroupItemView.as_view(), name='Group by id'),
    path(f'{apiTAG}groups/<int:group_id>/attendance/', GroupAttendanceListView.as_view(),
         name='Attendance by lesson id'),
    path(f'{apiTAG}groups/<int:group_id>/attendance/<int:subject_id>/', GroupAttendanceSubjectView.as_view(),
         name='Attendance by subject'),
    path(f'{apiTAG}attendance', AttendanceView.as_view(), name='Mark students as attend or not'),
    path(f'{apiTAG}teachers/<int:teacher_id>/subjects/', SubjectByTeacherAPIView.as_view(), name='subject-by-teacher'),
    path(f'{apiTAG}subjects/<int:subject_id>/attendance/',SubjectAttendanceView.as_view(),name='attendance by subject'),

]
