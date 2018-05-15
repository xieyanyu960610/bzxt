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
import json

from .models import *
from .serializers import *
from utils.permissions import IsAdmin
from utils.XRDhandle import preprocess
from utils.XRFhandle import xls_process
from bishe430.settings import MEDIA_ROOT
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
    queryset = exploSample.objects.all()
    #queryset = exploSample.objects.filter(sname="样本3")
    #serializer_class = exploSampleSerializer
    permission_classes = (IsAuthenticated,IsAdmin)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("note","sname","picDescrip", "sampleID",)
    ordering_fields = ("sampleID", "inputDate",)

    # def get_queryset(self):
    #     queryset = exploSample.objects.all()
    #     sname = self.request.query_params.get("sname","")
    #     if sname:
    #         queryset = queryset.filter(sname__contains=sname)
    #     return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return exploSampleDetailSerializer
        return exploSampleSerializer


class exploSampleFileViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,IsAdmin)
    queryset = exploSampleFile.objects.all()
    # serializer_class = exploSampleFileSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return exploSampleFileDetailSerializer
        return exploSampleFileSerializer

    def perform_create(self, serializer):
        file = serializer.save()
        if file.detectType == 3:
            file.handledUrl= preprocess(file.exploSample.id,os.path.join(MEDIA_ROOT,str(file.docUrl)),os.path.join(MEDIA_ROOT,"file\exploSampleFile\handled"),"file\exploSampleFile")
            file.save()
        elif file.detectType == 4:
            chSample_list = xls_process(os.path.join(MEDIA_ROOT,str(file.docUrl)))
            for chSample in chSample_list :
                explo_ChSample = exploChSample()
                explo_ChSample.exploSampleFile = file
                explo_ChSample.detectType = chSample[0]
                explo_ChSample.elementsList = json.dumps(chSample[1:])
                explo_ChSample.save()
        return file


class exploSamplePeakViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,IsAdmin)
    queryset = exploSamplePeak.objects.all()
    serializer_class = exploSamplePeakSerializer


class exploChSampleViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,IsAdmin)
    queryset = exploChSample.objects.all()
    serializer_class = exploChSampleSerializer


class devCompSampleFileViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,IsAdmin)
    queryset = devCompSampleFile.objects.all()
    # serializer_class = devCompSampleFileSerializer
    def get_serializer_class(self):
        if self.action == "retrieve":
            return devCompSampleFileDetailSerializer
        return devCompSampleFileSerializer

    def perform_create(self, serializer):
        file = serializer.save()
        if file.detectType == 3:
            file.handledUrl= preprocess(file.devCompSample.id,os.path.join(MEDIA_ROOT,str(file.docUrl)),os.path.join(MEDIA_ROOT,"file\devCompSampleFile\handled"),"file\devCompSampleFile")
            file.save()
        elif file.detectType == 4:
            chSample_list = xls_process(os.path.join(MEDIA_ROOT,str(file.docUrl)))
            for chSample in chSample_list :
                dev_ChSample = devCompChSample()
                dev_ChSample.devCompSampleFile = file
                dev_ChSample.detectType = chSample[0]
                dev_ChSample.elementsList = json.dumps(chSample[1:])
                dev_ChSample.save()
        return file


class devCompSamplePeakViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,IsAdmin)
    queryset = devCompSamplePeak.objects.all()
    serializer_class = devCompSamplePeakSerializer


class devCompChSampleViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,IsAdmin)
    queryset = devCompChSample.objects.all()
    serializer_class = devCompChSampleSerializer


class devCompSampleViewset(mixins.CreateModelMixin,mixins.ListModelMixin, mixins.RetrieveModelMixin,
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
    queryset = devCompSample.objects.all()
    #serializer_class = exploSampleSerializer
    permission_classes = (IsAuthenticated,IsAdmin)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("note","sname","picDescrip", "sampleID")
    ordering_fields = ("sampleID", "inputDate",)
    # def get_queryset(self):
    #     queryset = devCompSample.objects.all()
    #     sname = self.request.query_params.get("sname","")
    #     if sname:
    #         queryset = queryset.filter(sname__contains=sname)
    #     return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return devCompSampleDetailSerializer
        return devCompSampleSerializer


class devShapeSampleViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,IsAdmin)
    queryset = devCompChSample.objects.all()
    serializer_class = devShapeSampleSerializer