from rest_framework.response import Response
from rest_framework.views import APIView
from attendance.models import Teacher
from attendance.models import User

from attendance.serializers import TeacherSerializer

import requests
import json

class TeacherAPIView(APIView):
    def get(self, request):
        user_data = Teacher.objects.all()
        return Response({'posts': TeacherSerializer(user_data, many=True).data})

    def post(self, request):
        # Find id of teacher at ruz.spbstu.ru/api/v1/teachers
        serializer = TeacherSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if Teacher.objects.filter(user_id=request.data.get('user_id')).exists():
            return Response({'error': f'Such a teacher with user_id {request.data.get("user_id")}' + ' already exists'},
                            status=400)

        if Teacher.objects.filter(teacher_name=request.data.get('teacher_name')).exists():
            return Response({'error': f'Such a teacher with teacher_name {request.data.get("teacher_name")}' + ' already exists'},
                            status=400)



        if not User.objects.filter(user_id=request.data.get('user_id')).exists():
            return Response({'error': f'Such a user with user_id {request.data.get("user_id")}' + ' doesnt exists'},
                            status=400)





        #find id by name
        teachers_req = requests.get('https://ruz.spbstu.ru/api/v1/ruz/teachers/')
        teachers_json = teachers_req.json();
        teachers_list = teachers_json['teachers']

        #new teacher id for our db
        teacher_id = None
        print(teachers_list)
        for teacher in teachers_list:
            if(str(request.data.get('teacher_name')).lower() == str(teacher['full_name']).lower()):
                teacher_id = teacher['id']
                print('Found')

        #check if teacher in ruz.spbstu/.../teachers
        if(teacher_id == None):
            return Response({'error': f'Such a teacher with name {request.data.get("teacher_name")}' + ' doesnt exists'},
                            status=400)


        #if teacher was found
        request.data['teacher_id'] = str(teacher_id)
        serializer = TeacherSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #post data to database
        serializer.save()
        return Response({'post': serializer.data},
                        status=201)
