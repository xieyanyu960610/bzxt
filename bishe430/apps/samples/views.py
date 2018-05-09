# -*- coding: utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import UserRateThrottle

from .models import *
from .serializers import *
from utils.permissions import IsOwnerOrReadOnly
# Create your views here.

class exploSampleViewset(mixins.CreateModelMixin,mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    炸药及原材料常见样本管理
    list:
        获取
    create:
        添加
    update:
        更新
    delete:
        删除
    """
    #queryset = exploSample.objects.filter(sname="样本3")
    #serializer_class = exploSampleSerializer
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
   # search_fields = ("sname", "sampleID", "user__name", "inputDate",)
    ordering_fields = ("sampleID", "inputDate",)
    def get_queryset(self):
        queryset = exploSample.objects.all()
        sname = self.request.query_params.get("sname","")
        if sname:
            queryset = queryset.filter(sname__contains=sname)
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return exploSampleDetailSerializer
        return exploSampleSerializer
"""
    def perform_create(self, serializer):
        exploSample = serializer.save()
        shop_carts = exploSample.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            exploSampleFiles = exploSampleFile()
            exploSampleFiles.goods = shop_cart.goods
            exploSampleFiles.goods_num = shop_cart.nums
            exploSampleFiles.exploSample = exploSample
            order_goods.save()

            shop_cart.delete()
        return exploSample
"""


class exploSampleFileViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = exploSampleFile.objects.all()
    serializer_class = exploSampleFileSerializer

class exploSamplePeakViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = exploSamplePeak.objects.all()
    serializer_class = exploSamplePeakSerializer

class exploChSampleViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = exploChSample.objects.all()
    serializer_class = exploChSampleSerializer

class devCompSampleFileViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = devCompSampleFile.objects.all()
    serializer_class = devCompSampleFileSerializer

class devCompSamplePeakViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = devCompSamplePeak.objects.all()
    serializer_class = devCompSamplePeakSerializer

class devCompChSampleViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = devCompChSample.objects.all()
    serializer_class = devCompChSampleSerializer

class devCompSampleViewset(mixins.CreateModelMixin,mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    炸药及原材料常见样本管理
    list:
        获取
    create:
        添加
    update:
        更新
    delete:
        删除
    """
    #queryset = exploSample.objects.filter(sname="样本3")
    #serializer_class = exploSampleSerializer
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
   # search_fields = ("sname", "sampleID", "user__name", "inputDate",)
    ordering_fields = ("sampleID", "inputDate",)
    def get_queryset(self):
        queryset = exploSample.objects.all()
        sname = self.request.query_params.get("sname","")
        if sname:
            queryset = queryset.filter(sname__contains=sname)
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return devCompSampleDetailSerializer
        return devCompSampleSerializer

class devShapeSampleViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = devCompChSample.objects.all()
    serializer_class = devShapeSampleSerializer