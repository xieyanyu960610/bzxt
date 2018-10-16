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
import re

from .models import *
from .serializers import *
from utils.permissions import IsOwnerOrReadOnly
from utils.XRDhandle import *
from utils.XRFhandle import *
from bishe430.settings import MEDIA_ROOT
from samples.models import *
from user_operation.models import *
from utils.PCB import *
from utils.GCMS_handle import *
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

    def handleFile(self,file):
        if file.detectType == 3:
            file.handledUrl= preprocess(file.exploEvi.id,os.path.join(MEDIA_ROOT,str(file.docUrl)),os.path.join(MEDIA_ROOT,"file\exploEviFile\handled"),"file\exploEviFile")
            file.save()
            for i in similarity_rank(os.path.join(MEDIA_ROOT,str(file.handledUrl)),os.path.join(MEDIA_ROOT,"file\exploSampleFile\handled")):
                explo_match = exploMatch()
                explo_match.exploSample_id = i[0] # exploSample.objects.get(id=i[0])
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
                    explo_match.exploSample_id = scoreList[0]#exploSample.objects.get(id=scoreList[0])
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

    def perform_update(self, serializer):
        file = serializer.save()
        # for match in exploMatch.objects.filter(exploEvi =file.exploEvi):
        #     match.delete()
        file = self.handleFile(file)
        return file

    def perform_create(self, serializer):
        file = serializer.save()
        file = self.handleFile(file)
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

    def handleFile(self,file):
        if file.detectType == 3:
            file.handledUrl= preprocess(file.devCompEvi.id,os.path.join(MEDIA_ROOT,str(file.docUrl)),os.path.join(MEDIA_ROOT,"file\devCompEviFile\handled"),"file\devCompEviFile")
            file.save()
            for i in similarity_rank(os.path.join(MEDIA_ROOT, str(file.handledUrl)),
                                     os.path.join(MEDIA_ROOT, "file\devCompSampleFile\handled")):
                devComp_match = devCompMatch()
                devComp_match.devCompSample_id = i[0]#devCompSample.objects.get(id=i[0])
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
                    dev_match.devCompSample_id = scoreList[0]#devCompSample.objects.get(id=scoreList[0])
                    dev_match.devCompEvi = file.devCompEvi
                    dev_match.matchType = 4
                    dev_match.matchModel = chEvi[0]
                    dev_match.matchDegree = scoreList[1]
                    dev_match.save()
        elif file.detectType == 5 :
            oriFile = os.path.join(MEDIA_ROOT,str(file.docUrl))

            exfolder = os.path.join(MEDIA_ROOT,"file\devCompEviFile")
            folder = exfolder + "/"+str(file.devCompEvi_id)+"/"

            if not os.path.exists(folder):  # 判断是否存在文件夹如果不存在则创建为文件夹
                os.makedirs(folder)  # makedirs 创建文件时如果路径不存在会创建这个路径
            file.docUrl = "file/devCompEviFile/"+str(file.devCompEvi_id)+"/"+GCMS_handle(file.devCompEvi.sname,oriFile,folder)
            file.save()

            for sim in similarity_count(folder,os.path.join(MEDIA_ROOT,"file\devCompSampleFile")):
                dev_match = devCompMatch()
                dev_match.devCompSample_id = sim[0]  # devCompSample.objects.get(id=scoreList[0])
                dev_match.devCompEvi = file.devCompEvi
                dev_match.matchType = 5
                dev_match.matchDegree =sim[1]
                dev_match.strength = sim[2]
                dev_match.save()

        return file

    def perform_update(self, serializer):
        file = serializer.save()
        file = self.handleFile(file)
        return file

    def perform_create(self, serializer):
        file = serializer.save()
        file = self.handleFile(file)
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

    def perform_create(self, serializer):
        evi = serializer.save()
        id = evi.id
        #重命名
        name = str(evi.originalUrl).split("/")[-1]
        picType = os.path.splitext(name)[1]
        path = os.path.join(MEDIA_ROOT,"image/devShapeEvi/original/")
        os.rename(os.path.join(MEDIA_ROOT,str(evi.originalUrl)), os.path.join(path, str(id) + picType))
        evi.originalUrl = "image/devShapeEvi/original/" + str(id) + picType
        evi.save()
        #特征匹配
        if evi.isCircuit == False:
            FeatureMatching(id)
            evi.featureUrl = "file/devShapeEvi/feature/" + str(id) + ".harris"
            evi.save()
            fileUrl = os.path.join(MEDIA_ROOT,"file/devShapeEvi/match/"+ str(id)+".txt")
            file = open(fileUrl)
            seq = re.compile("\s+")
            for line in file:
                lst = seq.split(line.strip())
                shapeMatch = devShapeMatch()
                shapeMatch.devShapeEvi_id = lst[0]
                shapeMatch.devShapeSample_id = lst[1]
                shapeMatch.matchDegree = lst[2]
                shapeMatch.matchSampleCoordi = json.dumps(lst[3:6])
                shapeMatch.matchEviCoordi = json.dumps(lst[6:])
                shapeMatch.isCircuit = False
                shapeMatch.save()
            file.close()
            os.remove(fileUrl)

        return evi


    def perform_update(self, serializer):
        evi = serializer.save()
        id =evi.id
        if evi.isCircuit == False:
            FeatureMatching(id)
            evi.featureUrl = "file/devShapeEvi/feature/" + str(id) + ".harris"
            evi.save()
        else:
            middle = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "utils/middle/")
            if evi.isFirst == True:

                # 写文件
                rectUrl = os.path.join(middle, str(id) + "-1.txt")
                proUrl = os.path.join(middle, str(id) + "-2.txt")
                backUrl = os.path.join(middle, str(id) + "-3.txt")
                boardUrl = os.path.join(middle, str(id) + "-4.txt")

                rect = open(rectUrl, "w")
                rect.write(evi.rectCoordi)
                rect.close()
                pro = open(proUrl, "w")
                pro.write(evi.proCoordi)
                pro.close()
                back = open(backUrl, "w")
                back.write(evi.backCoordi)
                back.close()
                board = open(boardUrl, "w")
                board.write(evi.boardCoordi)
                board.close()

                getPCB(id, "Evi")

                evi.blackWhiteUrl = "image/devShapeEvi/blackWhite/" + str(id) + ".jpg"
                evi.interColorUrl = "image/devShapeEvi/interColor/" + str(id) + ".jpg"
                evi.middleResultUrl = "file/devShapeEvi/middleResult/" + str(id) + ".txt"

                os.remove(rectUrl)
                os.remove(proUrl)
                os.remove(backUrl)
                os.remove(boardUrl)

                evi.save()
            else:
                compCheckUrl = os.path.join(middle, str(id) + "-5.txt")
                boardCheckUrl = os.path.join(middle, str(id) + "-6.txt")

                compCheck = open(compCheckUrl, "w")
                compCheck.write(evi.compCheckCoordi)
                compCheck.close()
                boardCheck = open(boardCheckUrl, "w")
                boardCheck.write(evi.boardCheckCoordi)
                boardCheck.close()

                segComp(id, "Evi")

                evi.featureUrl = "file/devShapeEvi/feature/" + str(id) + ".harris"
                evi.resultPicUrl = "image/devShapeEvi/result/" + str(id) + ".jpg"
                evi.resultFileUrl = "file/devShapeEvi/result/" + str(id) + ".seg"

                os.remove(compCheckUrl)
                os.remove(boardCheckUrl)
                evi.save()

                CompMatching(id)


        fileUrl = os.path.join(MEDIA_ROOT,"file/devShapeEvi/match/"+ str(id)+".txt")
        if os.path.exists(fileUrl):
            file = open(fileUrl)
            seq = re.compile("\s+")
            for line in file:
                lst = seq.split(line.strip())
                shapeMatch = devShapeMatch()
                shapeMatch.devShapeEvi_id = lst[0]
                shapeMatch.devShapeSample_id = lst[1]
                shapeMatch.matchDegree = lst[2]
                shapeMatch.matchSampleCoordi = json.dumps(lst[3:6])
                shapeMatch.matchEviCoordi = json.dumps(lst[6:])
                shapeMatch.isCircuit = evi.isCircuit
                shapeMatch.save()
            file.close()
            # os.remove(fileUrl)
        return evi






    #
    # def perform_destroy(self, instance):
    #     # originalUrl= os.path.join(MEDIA_ROOT,str( instance.originalUrl))
    #     # if os.path.exists(originalUrl):
    #     #     os.remove(originalUrl)
    #     instance.delete()
