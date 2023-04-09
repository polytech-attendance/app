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

from attendance.views.group_view import GroupAPIView
from attendance.views.user_view import UserAPIView
from attendance.views.teacher_view import TeacherAPIView

apiTAG = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{apiTAG}groups/',GroupAPIView.as_view()),
    path(f'{apiTAG}users/',UserAPIView.as_view()),
    path(f'{apiTAG}teachers/',TeacherAPIView.as_view()),
]
