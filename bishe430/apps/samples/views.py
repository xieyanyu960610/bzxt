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
import os
import numpy as np
import matplotlib.pyplot as plt
import math
from django.http import HttpResponse
from .tasks import *
import re


from .models import *
from .serializers import *
# from .task import renew
from utils.permissions import IsAdmin
from utils.XRDhandle import preprocess
from utils.XRFhandle import xls_process
from bishe430.settings import MEDIA_ROOT,BASE_DIR
from user_operation.models import *
from evis.models import *
from utils.XRDhandle import *
from utils.XRFhandle import *
from utils.PCB import *
from utils.GCMS_handle import *





exploMatchType = []
devCompMatchType = []

def tasks(request,x,y):
    print('before run_test_suit')
    result = add.delay(x,y)
    print('after run_test_suit')
    return HttpResponse("job is runing background~")


def updateExploMatch(self):
    counting = len(exploMatchType)
    for i in range(0,counting):
        if exploMatchType[0] == 3 :
            exploMatchType.remove(3)
            exploMatch.objects.filter(matchType = 3).delete()
            evi_files = os.path.join(MEDIA_ROOT, "file\exploEviFile\handled")
            all_file = os.listdir(evi_files)
            for i in range(0, len(all_file)):
                if os.path.splitext(all_file[i])[1] == '.txt':
                    cur_path = os.path.join(evi_files, all_file[i])
                    cur_txt = all_file[i]
                    txt_id = os.path.splitext(cur_txt)[0]
                    # eviMatchs = exploMatch.objects.filter(exploEvi_id=txt_id).filter(
                    #     matchType=3)  # exploEvi.objects.get(id = txt_id))
                    # evis = eviMatchs.order_by("matchDegree")
                    #
                    # for evi in evis:
                    #     evi.delete()
                    for i in similarity_rank(cur_path,
                                             os.path.join(MEDIA_ROOT, "file\exploSampleFile\handled")):
                        explo_match = exploMatch()
                        explo_match.exploSample_id = i[0]
                        explo_match.exploEvi_id = txt_id  # exploEviMatch
                        explo_match.matchType = 3
                        explo_match.matchDegree = i[1]
                        explo_match.save()

        elif exploMatchType[0] == 4:
            exploMatchType.remove(4)
            exploMatch.objects.filter(matchType = 4).delete()
            eviChs = exploChEvi.objects.all()
            for i in range(0,len(eviChs)):
                chSamples = exploChSample.objects.filter(detectType=eviChs[i].detectType)
                sampleListAll = []
                for chSample in chSamples:
                    # print  (chSample['exploSample'])
                    sampleList = json.loads(chSample.elementsList)
                    sampleList.append(chSample.exploSampleFile.exploSample_id)
                    sampleListAll.append(sampleList)
                chEvi = json.loads(eviChs[i].elementsList)
                chEvi.insert(0,eviChs[i].detectType)
                scoresList = xrf_rank(chEvi, sampleListAll)
                for scoreList in scoresList:
                    explo_match = exploMatch()
                    explo_match.exploSample_id = scoreList[0]  # exploSample.objects.get(id=scoreList[0])
                    explo_match.exploEvi = eviChs[i].exploEviFile.exploEvi
                    explo_match.matchType = 4
                    explo_match.matchModel = chEvi[0]
                    explo_match.matchDegree = scoreList[1]
                    explo_match.save()
            # return HttpResponse("exploMatchingXRF is runing background~")

    return HttpResponse("exploMatching has updated~")


            # chEvi_list = xls_process(os.path.join(MEDIA_ROOT, str(file.docUrl)))
            # for chEvi in chEvi_list:
            #     explo_ChEvi = exploChEvi()
            #     explo_ChEvi.exploEviFile = file
            #     explo_ChEvi.detectType = chEvi[0]
            #     explo_ChEvi.elementsList = json.dumps(chEvi[1:])
            #     explo_ChEvi.save()
            #     chSamples = exploChSample.objects.filter(detectType=chEvi[0])
            #     sampleListAll = []
            #     for chSample in chSamples:
            #         # print  (chSample['exploSample'])
            #         sampleList = json.loads(chSample.elementsList)
            #         sampleList.append(chSample.exploSampleFile.exploSample_id)
            #         sampleListAll.append(sampleList)
            #     scoresList = xrf_rank(chEvi, sampleListAll)
            #     for scoreList in scoresList:
            #         explo_match = exploMatch()
            #         explo_match.exploSample_id = scoreList[0]  # exploSample.objects.get(id=scoreList[0])
            #         explo_match.exploEvi = file.exploEvi
            #         explo_match.matchType = 4
            #         explo_match.matchModel = chEvi[0]
            #         explo_match.matchDegree = scoreList[1]
            #         explo_match.save()
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


# Create your views here.
def updateDevCompMatch(self):
    counting = len(devCompMatchType)
    for i in range(0,counting):
        if devCompMatchType[0] == 3 :
            devCompMatchType.remove(3)
            devCompMatch.objects.filter(matchType = 3).delete()
            evi_files = os.path.join(MEDIA_ROOT, "file\devCompEviFile\handled")
            all_file = os.listdir(evi_files)
            for i in range(0, len(all_file)):
                if os.path.splitext(all_file[i])[1] == '.txt':
                    cur_path = os.path.join(evi_files, all_file[i])
                    cur_txt = all_file[i]
                    txt_id = os.path.splitext(cur_txt)[0]
                    # eviMatchs = exploMatch.objects.filter(exploEvi_id=txt_id).filter(
                    #     matchType=3)  # exploEvi.objects.get(id = txt_id))
                    # evis = eviMatchs.order_by("matchDegree")
                    #
                    # for evi in evis:
                    #     evi.delete()
                    for i in similarity_rank(cur_path,
                                             os.path.join(MEDIA_ROOT, "file\devCompSampleFile\handled")):
                        devComp_match = devCompMatch()
                        devComp_match.devCompSample_id = i[0]  # devCompSample.objects.get(id=i[0])
                        devComp_match.devCompEvi_id = txt_id
                        devComp_match.matchType = 3
                        devComp_match.matchDegree = i[1]
                        devComp_match.save()

        elif devCompMatchType[0] == 4:
            devCompMatchType.remove(4)
            devCompMatch.objects.filter(matchType = 4).delete()
            eviChs =devCompChEvi.objects.all()
            for i in range(0,len(eviChs)):
                chSamples = devCompChSample.objects.filter(detectType=eviChs[i].detectType)
                sampleListAll = []
                for chSample in chSamples:
                    # print  (chSample['exploSample'])
                    sampleList = json.loads(chSample.elementsList)
                    sampleList.append(chSample.devCompSampleFile.devCompSample_id)
                    sampleListAll.append(sampleList)
                chEvi = json.loads(eviChs[i].elementsList)
                chEvi.insert(0,eviChs[i].detectType)
                scoresList = xrf_rank(chEvi, sampleListAll)
                for scoreList in scoresList:
                    dev_match = devCompMatch()
                    dev_match.devCompSample_id = scoreList[0]  # devCompSample.objects.get(id=scoreList[0])
                    dev_match.devCompEvi = eviChs[i].devCompEviFile.devCompEvi
                    dev_match.matchType = 4
                    dev_match.matchModel = chEvi[0]
                    dev_match.matchDegree = scoreList[1]
                    dev_match.save()
            # return HttpResponse("exploMatchingXRF is runing background~")

    return HttpResponse("devCompMatching has updated~")

def updateDevShapeMatch(self):
    evis = devShapeEvi.objects.all()
    for evi in evis:
        id = evi.id
        typeLists = [ match.isCircuit for match in devShapeMatch.objects.filter(devShapeEvi_id = id)]
        # devShapeMatch.objects.filter(devShapeEvi_id=id).delete()
        existType = []
        for typeList in typeLists:
            if typeList not in existType:
                existType.append(typeList)
        devShapeMatch.objects.filter(devShapeEvi_id=id).delete()
        for i in range(0,len(existType)):
            if existType[i] == False:
                FeatureMatching(id)
            else:
                CompMatching(id)

            fileUrl = os.path.join(MEDIA_ROOT, "file/devShapeEvi/match/" + str(id) + ".txt")
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
                os.remove(fileUrl)

    return HttpResponse("devShapeMatching has updated~")






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



    def handleFile(self,file):

        def pearson(txt_1, txt_2):
            signal_1 = np.loadtxt(txt_1)[1]
            print(signal_1)
            signal_2 = np.loadtxt(txt_2)[1]
            print(signal_2)
            n = len(signal_1)
            mean1 = signal_1.mean()
            mean2 = signal_2.mean()
            standvalue1 = math.sqrt(sum((signal_1 - mean1) * (signal_1 - mean1)))
            standvalue2 = math.sqrt(sum((signal_2 - mean2) * (signal_2 - mean2)))
            cov = sum((signal_1 - mean1) * (signal_2 - mean2))
            pearson = cov / (standvalue1 * standvalue2)
            return pearson

        if file.detectType == 3:
            file.handledUrl = preprocess(file.exploSample.id, os.path.join(MEDIA_ROOT, str(file.docUrl)),
                                         os.path.join(MEDIA_ROOT, "file\exploSampleFile\handled"),
                                         "file\exploSampleFile")
            file.save()
            renew2.delay()

            fileId = file.id



            # evi_files = os.path.join(MEDIA_ROOT,"file\exploEviFile\handled")
            # all_file = os.listdir(evi_files)
            # for i in range(0, len(all_file)):
            #     if os.path.splitext(all_file[i])[1] == '.txt':
            #         cur_path = os.path.join(evi_files, all_file[i])
            #         cur_txt = all_file[i]
            #         txt_id = os.path.splitext(cur_txt)[0]
            #         # exploEviMatch = exploEvi.objects.get(id=txt_id)
            #         cur_score = pearson(os.path.join(MEDIA_ROOT,str(file.handledUrl)), cur_path)
            #         eviMatchs = exploMatch.objects.filter(exploEvi_id = txt_id).filter(matchType=3) #exploEvi.objects.get(id = txt_id))
            #         sampleMatch = eviMatchs.filter(exploSample_id=file.exploSample.id)
            #         evis = eviMatchs.order_by("matchDegree")
            #
            #         if len(sampleMatch) == 0:
            #             if len(evis) != 0:
            #                 if cur_score > evis[0].matchDegree:
            #                     if len(evis) == 10:
            #                         evis[0].delete()
            #
            #                     explo_match = exploMatch()
            #                     explo_match.exploSample = file.exploSample
            #                     explo_match.exploEvi_id = txt_id  # exploEviMatch
            #                     explo_match.matchType = 3
            #                     explo_match.matchDegree = cur_score
            #                     explo_match.save()
            #             else:
            #                 for i in similarity_rank(cur_path,
            #                                          os.path.join(MEDIA_ROOT, "file\exploSampleFile\handled")):
            #                     explo_match = exploMatch()
            #                     explo_match.exploSample_id = i[0]
            #                     explo_match.exploEvi_id = txt_id  # exploEviMatch
            #                     explo_match.matchType = 3
            #                     explo_match.matchDegree = i[1]
            #                     explo_match.save()
            #         else:
            #             if cur_score >= evis[0].matchDegree:
            #                 sampleMatch[0].matchDegree = cur_score
            #                 sampleMatch[0].save()
            #             else:
            #                 for evi in evis:
            #                     evi.delete()
            #                 for i in similarity_rank(cur_path,
            #                                          os.path.join(MEDIA_ROOT, "file\exploSampleFile\handled")):
            #                     explo_match = exploMatch()
            #                     explo_match.exploSample_id = i[0]
            #                     explo_match.exploEvi_id = txt_id  # exploEviMatch
            #                     explo_match.matchType = 3
            #                     explo_match.matchDegree = i[1]
            #                     explo_match.save()
            #     # end = time.time()
            #     # print(end - start)
            #     # print("end")

            # exploMatch.objects.filter(matchType=3).delete()
            # evi_files = os.path.join(MEDIA_ROOT, "file\exploEviFile\handled")
            # all_file = os.listdir(evi_files)
            # for i in range(0, len(all_file)):
            #     if os.path.splitext(all_file[i])[1] == '.txt':
            #         cur_path = os.path.join(evi_files, all_file[i])
            #         cur_txt = all_file[i]
            #         txt_id = os.path.splitext(cur_txt)[0]
            #         # eviMatchs = exploMatch.objects.filter(exploEvi_id=txt_id).filter(
            #         #     matchType=3)  # exploEvi.objects.get(id = txt_id))
            #         # evis = eviMatchs.order_by("matchDegree")
            #         #
            #         # for evi in evis:
            #         #     evi.delete()
            #         for i in similarity_rank(cur_path,
            #                                  os.path.join(MEDIA_ROOT, "file\exploSampleFile\handled")):
            #             explo_match = exploMatch()
            #             explo_match.exploSample_id = i[0]
            #             explo_match.exploEvi_id = txt_id  # exploEviMatch
            #             explo_match.matchType = 3
            #             explo_match.matchDegree = i[1]
            #             explo_match.save()


        elif file.detectType == 4:
            chSample_list = xls_process(os.path.join(MEDIA_ROOT, str(file.docUrl)))
            for chSample in chSample_list:
                explo_ChSample = exploChSample()
                explo_ChSample.exploSampleFile = file
                explo_ChSample.detectType = chSample[0]
                explo_ChSample.elementsList = json.dumps(chSample[1:])
                explo_ChSample.save()
        if file.detectType not in exploMatchType:
            exploMatchType.append(file.detectType)
        return file


    def perform_update(self, serializer):
        file = serializer.save()
        file = self.handleFile(file)
        # result = run_test_suit.delay('110')
        return file


    def perform_create(self, serializer):
        file = serializer.save()
        file = self.handleFile(file)
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

    def handleFile(self,file):
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
        elif file.detectType == 5 :
            oriFile = os.path.join(MEDIA_ROOT,str(file.docUrl))

            exfolder = os.path.join(MEDIA_ROOT,"file\devCompSampleFile")
            folder = exfolder + "/"+str(file.devCompSample_id)+"/"+file.strength+"/"

            if not os.path.exists(folder):  # 判断是否存在文件夹如果不存在则创建为文件夹
                os.makedirs(folder)  # makedirs 创建文件时如果路径不存在会创建这个路径
            file.docUrl = "file/devCompSampleFile/"+str(file.devCompSample_id)+"/"+file.strength+"/"+GCMS_handle(file.devCompSample.sname,oriFile,folder)
            file.save()


        if file.detectType not in devCompMatchType:
            devCompMatchType.append(file.detectType)
        return file

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # docUrlOri = instance.docUrl
        # os.remove(os.path.join(MEDIA_ROOT, str(instance.handledUrl)))
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # fileDelete =
        self.perform_update(serializer)
        # docUrlUpdate = serializer.data["docUrl"]
        # if docUrlOri != docUrlUpdate:
        #     os.remove(os.path.join(MEDIA_ROOT, str(docUrlOri)))

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        file = serializer.save()
        file = self.handleFile(file)
        return file

    def perform_create(self, serializer):
        file = serializer.save()
        file = self.handleFile(file)
        return file

        # if file.detectType == 3:
        #     file.handledUrl= preprocess(file.devCompSample.id,os.path.join(MEDIA_ROOT,str(file.docUrl)),os.path.join(MEDIA_ROOT,"file\devCompSampleFile\handled"),"file\devCompSampleFile")
        #     file.save()
        # elif file.detectType == 4:
        #     chSample_list = xls_process(os.path.join(MEDIA_ROOT,str(file.docUrl)))
        #     for chSample in chSample_list :
        #         dev_ChSample = devCompChSample()
        #         dev_ChSample.devCompSampleFile = file
        #         dev_ChSample.detectType = chSample[0]
        #         dev_ChSample.elementsList = json.dumps(chSample[1:])
        #         dev_ChSample.save()
        # return file


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
    queryset = devShapeSample.objects.all()
    serializer_class = devShapeSampleSerializer

    def perform_create(self, serializer):
        sample = serializer.save()
        id = sample.id
        #重命名
        name = str(sample.originalUrl).split("/")[-1]
        picType = os.path.splitext(name)[1]
        path = os.path.join(MEDIA_ROOT,"image/devShapeSample/original/")
        os.rename(os.path.join(MEDIA_ROOT,str(sample.originalUrl)), os.path.join(path, str(id) + picType))
        sample.originalUrl = "image/devShapeSample/original/" + str(id) + picType
        sample.save()
        return sample


    def perform_update(self, serializer):
        sample = serializer.save()
        id =sample.id
        middle = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "utils/middle/")
        if sample.isFirst == True:
            middle = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "utils/middle/")

            # 写文件
            rectUrl = os.path.join(middle, str(id) + "-1.txt")
            proUrl = os.path.join(middle, str(id) + "-2.txt")
            backUrl = os.path.join(middle, str(id) + "-3.txt")
            boardUrl = os.path.join(middle, str(id) + "-4.txt")

            rect = open(rectUrl, "w")
            rect.write(sample.rectCoordi)
            rect.close()
            pro = open(proUrl, "w")
            pro.write(sample.proCoordi)
            pro.close()
            back = open(backUrl, "w")
            back.write(sample.backCoordi)
            back.close()
            board = open(boardUrl, "w")
            board.write(sample.boardCoordi)
            board.close()

            getPCB(id, "Sample")

            sample.blackWhiteUrl = "image/devShapeSample/blackWhite/" + str(id) + ".jpg"
            sample.interColorUrl = "image/devShapeSample/interColor/" + str(id) + ".jpg"
            sample.middleResultUrl = "file/devShapeSample/middleResult/" + str(id) + ".txt"

            os.remove(rectUrl)
            os.remove(proUrl)
            os.remove(backUrl)
            os.remove(boardUrl)

            sample.save()
        else:
            compCheckUrl = os.path.join(middle,str(id) + "-5.txt")
            boardCheckUrl = os.path.join(middle,str(id) + "-6.txt")

            compCheck = open(compCheckUrl,"w")
            compCheck.write(sample.compCheckCoordi)
            compCheck.close()
            boardCheck = open(boardCheckUrl,"w")
            boardCheck.write(sample.boardCheckCoordi)
            boardCheck.close()

            segComp(id, "Sample")

            sample.featureUrl = "file/devShapeSample/feature/"+str(id)+".harris"
            sample.resultPicUrl = "image/devShapeSample/result/"+str(id)+".jpg"
            sample.resultFileUrl = "file/devShapeSample/result/"+str(id)+".seg"

            os.remove(compCheckUrl)
            os.remove(boardCheckUrl)

            sample.save()
        return sample

    def perform_destroy(self, instance):
        # originalUrl= os.path.join(MEDIA_ROOT,str( instance.originalUrl))
        # if os.path.exists(originalUrl):
        #     os.remove(originalUrl)
        instance.delete()



