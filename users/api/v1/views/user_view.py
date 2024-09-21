from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.api.v1.serializer.user_serializer import UserSerializer


class MeView(APIView):
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
