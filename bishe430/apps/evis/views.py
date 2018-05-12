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
from utils.XRDhandle import *
from bishe430.settings import MEDIA_ROOT
from user_operation.models import *
# Create your views here.

class exploEviViewset(mixins.CreateModelMixin,mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
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
        queryset = exploEvi.objects.all()
        sname = self.request.query_params.get("sname","")
        if sname:
            queryset = queryset.filter(sname__contains=sname)
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return exploEviDetailSerializer
        return exploEviSerializer
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


class exploEviFileViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = exploEviFile.objects.all()
    serializer_class = exploEviFileSerializer
    def perform_create(self, serializer):
        file = serializer.save()
        if file.detectType == 3:
            file.handledUrl= preprocess(file.exploEvi.id,os.path.join(MEDIA_ROOT,str(file.docUrl)),os.path.join(MEDIA_ROOT,"file\exploEviFile\handled"),"file\exploEviFile")
            file.save()
            for i in similarity_rank(os.path.join(MEDIA_ROOT,str(file.handledUrl)),os.path.join(MEDIA_ROOT,"file\exploSampleFile\handled")):
                explo_match = exploMatch()
                explo_match.exploSample = exploSample.objects.get(id=i[0])
                explo_match.exploEvi = file.exploEvi
                explo_match.matchType = 3
                explo_match.matchDegree = i[1]
                explo_match.save()
           # string=similarity_rank(os.path.join(file.exploEvi.id + '.txt'),os.path.join(MEDIA_ROOT,"file\exploEviFile\handled"))
           # print(string)
        return file

class exploEviPeakViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = exploEviPeak.objects.all()
    serializer_class = exploEviPeakSerializer

class exploChEviViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = exploChEvi.objects.all()
    serializer_class = exploChEviSerializer

class devCompEviFileViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = devCompEviFile.objects.all()
    serializer_class = devCompEviFileSerializer
    def perform_create(self, serializer):
        file = serializer.save()
        if file.detectType == 3:
            file.handledUrl= preprocess(file.devCompEvi.id,os.path.join(MEDIA_ROOT,str(file.docUrl)),os.path.join(MEDIA_ROOT,"file\devCompEviFile\handled"),"file\devCompEviFile")
            file.save()
            for i in similarity_rank(os.path.join(MEDIA_ROOT, str(file.handledUrl)),
                                     os.path.join(MEDIA_ROOT, "file\devCompSampleFile\handled")):
                devComp_match = devCompMatch()
                devComp_match.devCompSample = devCompSample.objects.get(id=i[0])
                devComp_match.devCompEvi = file.devCompEvi
                devComp_match.matchType = 3
                devComp_match.matchDegree = i[1]
                devComp_match.save()
        return file

class devCompEviPeakViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = devCompEviPeak.objects.all()
    serializer_class = devCompEviPeakSerializer

class  devCompChEviViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = devCompChEvi.objects.all()
    serializer_class =  devCompChEviSerializer

class devCompEviViewset(mixins.CreateModelMixin,mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
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
        queryset = devCompEvi.objects.all()
        sname = self.request.query_params.get("sname","")
        if sname:
            queryset = queryset.filter(sname__contains=sname)
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return devCompEviDetailSerializer
        return devCompEviSerializer

class devShapeEviViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = devShapeEvi.objects.all()
    serializer_class = devShapeEviSerializer
