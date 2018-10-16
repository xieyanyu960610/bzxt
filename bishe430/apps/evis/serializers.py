# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import *

class exploChEviSerializer(serializers.ModelSerializer):
    class Meta:
        model = exploChEvi
        fields = "__all__"

class exploEviFileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    handledUrl =serializers.FileField(read_only=True,)
    class Meta:
        model = exploEviFile
        fields = "__all__"


class exploEviFileDetailSerializer(serializers.ModelSerializer):
    exploChEvi = exploChEviSerializer(many=True)
    class Meta:
        model = exploEviFile
        fields =("exploEvi", "user", "inputDate", "detectDevice", "detectMrfs", "detectType", "docType", "docUrl",
         "handledUrl", "exploChEvi")


class exploEviPeakSerializer(serializers.ModelSerializer):
    class Meta:
        model = exploEviPeak
        fields = "__all__"


class exploEviDetailSerializer(serializers.ModelSerializer):
    exploEviFile = exploEviFileDetailSerializer(many=True)

    class Meta:
        model = exploEvi
        fields = ("id","caseID", "evidenceID", "user", "inputDate", "eviState", "eviMake",
                    "eviDraw", "eviAnalyse", "analyseCondition","picUrl",
                    "picDescrip","note","exploEviFile")

class exploEviSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(
        read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = exploEvi
        fields = "__all__"

class devCompChEviSerializer(serializers.ModelSerializer):
    class Meta:
        model = devCompChEvi
        fields = "__all__"

class devCompEviFileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    handledUrl = serializers.FileField(read_only=True, )

    class Meta:
        model = devCompEviFile
        fields = "__all__"

class devCompEviFileDetailSerializer(serializers.ModelSerializer):
    devCompChEvi = devCompChEviSerializer(many=True)

    class Meta:
        model = devCompEviFile
        fields =("devCompEvi", "user", "inputDate", "detectDevice", "detectMrfs", "detectType", "docType", "docUrl",
         "handledUrl", "devCompChEvi")


class devCompEviPeakSerializer(serializers.ModelSerializer):
    class Meta:
        model = devCompEviPeak
        fields = "__all__"



class devCompEviDetailSerializer(serializers.ModelSerializer):
    devCompEviFile = devCompEviFileDetailSerializer(many=True)

    class Meta:
        model = devCompEvi
        fields = ("id","caseID", "evidenceID", "user", "inputDate", "eviState", "eviMake",
                    "eviDraw", "eviAnalyse", "analyseCondition","picUrl",
                    "picDescrip","note","devCompEviFile")


class devCompEviSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    inputDate = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = devCompEvi
        fields = "__all__"

class devShapeEviSerializer(serializers.ModelSerializer):
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
        model = devShapeEvi
        fields = "__all__"