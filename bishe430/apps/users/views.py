from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler


from apps.users.serializers import *
from apps.users.models import UserProfile
from utils.permissions import *
#User = get_user_model()

# Create your views here.
class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            users = UserProfile.objects.filter(isDelete=False)
            user = users.get(username=username)
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserViewset(viewsets.ModelViewSet):
    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = UserProfile.objects.all()
    lookup_field = "username"
#    permission_classes = (IsAuthenticated,IsSuperAdmin,)
    def get_permissions(self):
        if self.action == "retrieve" or self.action =="list":
            return [IsAuthenticated(),]
        else:
            return [IsAuthenticated(),IsSuperAdmin(),]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):
        return serializer.save()
#url后返回的对象 比如此时就是users/任意数字都会返回当前用户
#    def get_object(self):
 #       return self.request.user
    def perform_destroy(self, instance):
        instance.isDelete = True
        instance.save()


