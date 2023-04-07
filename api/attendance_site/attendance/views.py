from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .auxiliary.hash_coding import str_to_hash
from .models import Group
from .models import User


from .serializers import GroupSerializer
from .serializers import UserSerializer




# Create your views here.
class GroupAPIView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserAPIView(APIView):
    def get(self, request):
        user_data = User.objects.all()
        return Response({'posts': UserSerializer(user_data, many=True).data})

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #Hashing user_password with SHA255
        password_hash = str_to_hash(request.data.get('user_password'))


        post_new = User.objects.create(
            user_login = request.data.get('user_login'),
            user_password = password_hash
        )

        return Response({'post' : UserSerializer(post_new).data})