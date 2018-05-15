# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import *
from utils.XRDhandle import preprocess


class exploChSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = exploChSample
        fields = "__all__"

class exploSampleFileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    handledUrl =serializers.FileField(read_only=True,)

    class Meta:
        model = exploSampleFile
        fields = "__all__"

class exploSampleFileDetailSerializer(serializers.ModelSerializer):

    exploChSample=exploChSampleSerializer(many=True)

    class Meta:
        model = exploSampleFile
        fields =("exploSample", "user", "inputDate", "detectDevice", "detectMrfs", "detectType", "docType", "docUrl",
         "handledUrl", "exploChSample")


class exploSamplePeakSerializer(serializers.ModelSerializer):
    class Meta:
        model = exploSamplePeak
        fields = "__all__"


class exploSampleDetailSerializer(serializers.ModelSerializer):
    exploSampleFile = exploSampleFileDetailSerializer(many=True)

    class Meta:
        model = exploSample
        fields = ("id","sname", "sampleID", "user", "inputDate", "sampleState", "sampleOrigin",
                    "sampleType", "sampleMake", "sampleDraw", "sampleAnalyse", "analyseCondition","picUrl",
                    "picDescrip","note","exploSampleFile")


class exploSampleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = exploSample
        fields = "__all__"


class devCompChSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = devCompChSample
        fields = "__all__"

class devCompSampleFileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    handledUrl = serializers.FileField(read_only=True, )

    class Meta:
        model = devCompSampleFile
        fields = "__all__"


class devCompSampleFileDetailSerializer(serializers.ModelSerializer):

    devCompChSample = devCompChSampleSerializer(many=True)

    class Meta:
        model = devCompSampleFile
        fields =("devCompSample","user","inputDate","detectDevice","detectMrfs","detectType","docType","docUrl","handledUrl","devCompChSample")


class devCompSamplePeakSerializer(serializers.ModelSerializer):
    class Meta:
        model = devCompSamplePeak
        fields = "__all__"



class devCompSampleDetailSerializer(serializers.ModelSerializer):
    devCompSampleFile = devCompSampleFileDetailSerializer(many=True)

    class Meta:
        model =devCompSample
        fields = ("id", "sname", "sampleID", "user", "inputDate", "sampleState", "sampleOrigin",
                  "sampleType", "sampleMake", "sampleDraw", "sampleAnalyse", "analyseCondition", "picUrl",
                  "picDescrip", "note", "devCompSampleFile", "devCompChSample")


class devCompSampleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = devCompSample
        fields = "__all__"

class devShapeSampleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    blackWhiteUrl =serializers.FileField(read_only=True,)
    interColorUrl =serializers.FileField(read_only=True,)
    featureUrl =serializers.FileField(read_only=True,)
    resultPicUrl =serializers.FileField(read_only=True,)
    resultFileUrl = serializers.FileField(read_only=True, )
    nomUrl = serializers.FileField(read_only=True, )
    nomResolution = serializers.FileField(read_only=True, )

    class Meta:
        model = devShapeSample
        fields = "__all__"