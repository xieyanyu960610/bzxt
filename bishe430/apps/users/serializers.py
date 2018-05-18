# -*- coding: utf-8 -*-
import re
from rest_framework import serializers
from datetime import datetime
from datetime import timedelta
from rest_framework.validators import UniqueValidator

from apps.users.models import UserProfile


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    class Meta:
        model = UserProfile
        fields = ("username","name", "gender", "role", "phone", "isDelete","picUrl","note")


class UserRegSerializer(serializers.ModelSerializer):
    username = serializers.CharField(label="编号", help_text="编号", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=UserProfile.objects.all(), message="该编号已被注册过")])

    password = serializers.CharField(
        style={'input_type': 'password'},help_text="密码", label="密码",# write_only=True,
    )

    def validate_role(self, role):
        # 注意参数，self以及字段名
        # 注意函数名写法，validate_ + 字段名字
        if self.context["request"].user.role == 3:
            raise serializers.ValidationError("您没有执行该操作的权限。")
        elif self.context["request"].user.role == 2 and role != 3:
            raise serializers.ValidationError("您没有执行该操作的权限。")
        else:
            return role

    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    # def update(self, instance, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     password = user.set_password(validated_data["password"])
    #     validated_data["password"] = password
    #     instance.save()

    class Meta:
        model = UserProfile
        fields = ("username", "password","userID","name", "gender", "role", "phone", "isDelete","picUrl","note")
