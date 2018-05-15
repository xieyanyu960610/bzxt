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
from utils.permissions import IsOwnerOrReadOnly
from utils.XRDhandle import *
from utils.XRFhandle import *
from bishe430.settings import MEDIA_ROOT
from samples.models import *
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
    queryset = exploEvi.objects.all()
    #serializer_class = exploSampleSerializer
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("caseID", "evidenceID"," picDescrip","note")
    ordering_fields = ("evidenceID", "inputDate",)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return exploEviDetailSerializer
        return exploEviSerializer


class exploEviFileViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = exploEviFile.objects.all()
    # serializer_class = exploEviFileSerializer
    def get_serializer_class(self):
        if self.action == "retrieve":
            return exploEviFileDetailSerializer
        return exploEviFileSerializer

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
        elif file.detectType == 4:
            chEvi_list = xls_process(os.path.join(MEDIA_ROOT, str(file.docUrl)))
            for chEvi in chEvi_list:
                explo_ChEvi = exploChEvi()
                explo_ChEvi.exploEviFile= file
                explo_ChEvi.detectType = chEvi[0]
                explo_ChEvi.elementsList = json.dumps(chEvi[1:])
                explo_ChEvi.save()
                chSamples = exploChSample.objects.filter(detectType=chEvi[0])
                sampleListAll=[]
                for chSample in chSamples:
                    # print  (chSample['exploSample'])
                    sampleList= json.loads(chSample.elementsList)
                    sampleList.append(chSample.exploSampleFile.exploSample_id)
                    sampleListAll.append(sampleList)
                scoresList = xrf_rank(chEvi,sampleListAll)
                for scoreList in scoresList:
                    explo_match = exploMatch()
                    explo_match.exploSample =exploSample.objects.get(id=scoreList[0])
                    explo_match.exploEvi = file.exploEvi
                    explo_match.matchType = 4
                    explo_match.matchModel = chEvi[0]
                    explo_match.matchDegree = scoreList[1]
                    explo_match.save()
                #
                # for chSample in chSamples:
                #     print()
                #     i =0
                #     while i<10:
                #         explo_match = exploMatch()
                #         explo_match.exploSample = chSample.exploSample
                #         explo_match.exploEvi = file.exploEvi
                #         explo_match.matchType = 4
                #         explo_match.matchModel = chEvi[0]
                #         explo_match.matchDegree = xrf_similarity(chEvi[1:],json.loads(chSample.elementsList))
                #         explo_match.save()
                #         i+=1
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
    # serializer_class = devCompEviFileSerializer
    def get_serializer_class(self):
        if self.action == "retrieve":
            return devCompEviFileDetailSerializer
        return devCompEviFileSerializer

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
        elif file.detectType == 4:
            chEvi_list = xls_process(os.path.join(MEDIA_ROOT, str(file.docUrl)))
            for chEvi in chEvi_list:
                dev_ChEvi = devCompChEvi()
                dev_ChEvi.devCompEviFile= file
                dev_ChEvi.detectType = chEvi[0]
                dev_ChEvi.elementsList = json.dumps(chEvi[1:])
                dev_ChEvi.save()
                chSamples = devCompChSample.objects.filter(detectType=chEvi[0])
                sampleListAll=[]
                for chSample in chSamples:
                    # print  (chSample['exploSample'])
                    sampleList= json.loads(chSample.elementsList)
                    sampleList.append(chSample.devCompSampleFile.devCompSample_id)
                    sampleListAll.append(sampleList)
                scoresList = xrf_rank(chEvi,sampleListAll)
                for scoreList in scoresList:
                    dev_match = devCompMatch()
                    dev_match.devCompSample = devCompSample.objects.get(id=scoreList[0])
                    dev_match.devCompEvi = file.devCompEvi
                    dev_match.matchType = 4
                    dev_match.matchModel = chEvi[0]
                    dev_match.matchDegree = scoreList[1]
                    dev_match.save()
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
    queryset = devCompEvi.objects.all()
    #serializer_class = exploSampleSerializer
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("caseID", "evidenceID"," picDescrip","note")
    ordering_fields = ("caseID", "evidenceID", "inputDate")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return devCompEviDetailSerializer
        return devCompEviSerializer


class devShapeEviViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = devShapeEvi.objects.all()
    serializer_class = devShapeEviSerializer
