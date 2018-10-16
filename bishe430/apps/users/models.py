from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    """
    用户
    """
    ROLE_TYPE = (
        (1, "超级管理员"),
        (2, "管理员"),
        (3, "普通用户"),
    )
    userID = models.CharField(max_length=20, verbose_name = "人员编号")
    name = models.CharField(max_length=6,verbose_name="人员姓名")
    gender = models.CharField(max_length=6,choices=(("male",u"男"),("female",u"女")),default="female",verbose_name="性别")
    phone = models.CharField(max_length=20,verbose_name="联系电话")
    isDelete =models.BooleanField(default=False,verbose_name="是否逻辑删除")
    role = models.IntegerField(choices=ROLE_TYPE,default=3, verbose_name="权限标识", help_text="权限标识")
    picUrl =models.ImageField(max_length=100,upload_to="image/user/",null=True,blank=True,verbose_name="头像路径")
    note =models.CharField(max_length=200,null=True,blank=True,verbose_name="备注")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        return self.name



