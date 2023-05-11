from rest_framework.response import Response
from rest_framework.views import APIView
from attendance.models import Lesson

from attendance.serializers import TeacherSerializer

import requests
import json

