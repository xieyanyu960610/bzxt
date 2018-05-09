# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import *


class exploSampleFileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    handledUrl =serializers.FileField(read_only=True,)
    class Meta:
        model = exploSampleFile
        fields = "__all__"

class exploSamplePeakSerializer(serializers.ModelSerializer):
    class Meta:
        model = exploSamplePeak
        fields = "__all__"


class exploChSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = exploChSample
        fields = "__all__"


class exploSampleDetailSerializer(serializers.ModelSerializer):
    exploSampleFile = exploSampleFileSerializer(many=True)
    exploChSample = exploChSampleSerializer(many=True)
    class Meta:
        model = exploSample
        fields = ("id","sname", "sampleID", "user", "inputDate", "sampleState", "sampleOrigin",
                    "sampleType", "sampleMake", "sampleDraw", "sampleAnalyse", "analyseCondition","picUrl",
                    "picDescrip","note","exploSampleFile","exploChSample")

class exploSampleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = exploSample
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


class devCompSamplePeakSerializer(serializers.ModelSerializer):
    class Meta:
        model = devCompSamplePeak
        fields = "__all__"


class devCompChSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = devCompChSample
        fields = "__all__"


class devCompSampleDetailSerializer(serializers.ModelSerializer):
    devCompSampleFile = devCompSampleFileSerializer(many=True)
    devCompChSample = devCompChSampleSerializer(many=True)

    class Meta:
        model = exploSample
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