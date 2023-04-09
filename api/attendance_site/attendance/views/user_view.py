from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.attendance_site.attendance.auxiliary.hash_coding import str_to_hash
from api.attendance_site.attendance.models import Group
from api.attendance_site.attendance.models import User

from api.attendance_site.attendance.serializers import GroupSerializer
from api.attendance_site.attendance.serializers import UserSerializer


# Create your views here.


class UserAPIView(APIView):
    def get(self, request):
        user_data = User.objects.all()
        return Response({'posts': UserSerializer(user_data, many=True).data})

    def post(self, request):
        # Hashing user_password with SHA255
        password_hash = str_to_hash(request.data.get('user_password'))
        request.data['user_password'] = password_hash
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # checking is user_login is unique
        if User.objects.filter(user_login=request.data.get('user_login')).exists():
            return Response({'error': f'Such a user with login {request.data.get("user_login")}' + ' already exists'},
                            status=400)

        #post data to database
        serializer.save()
        return Response({'post': serializer.data},
                        status=201)
