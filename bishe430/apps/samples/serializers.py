# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import *
from utils.XRDhandle import preprocess

class ImgSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def __str__(self):
        return self.url

    class Meta:
        model = Image
        fields = ('user', 'url')

class ListImgSerializer(serializers.Serializer):
    imgs = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=True),
        write_only=True )
    return_imgs = serializers.ListField(
        child=serializers.CharField(max_length=1000,),
        read_only=True )

    def create(self, validated_data):
        imgs = validated_data.get('imgs')
        images = []
        for index, url in enumerate(imgs):
            image = Image.objects.create(url=url, user=UserProfile.objects.get(id=self.context['request'].user.id))
            blog = ImgSerializer(image, context=self.context)
            images.append(blog.data['url'])
            return {'return_imgs':images}


class exploChSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = exploChSample
        fields = "__all__"

class exploSampleFileDetailSerializer(serializers.ModelSerializer):

    exploChSample=exploChSampleSerializer(many=True)

    class Meta:
        model = exploSampleFile
        fields =("exploSample", "user", "inputDate", "detectDevice", "detectMrfs", "detectType", "docType", "docUrl",
         "handledUrl", "exploChSample")


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
                  "picDescrip", "note", "devCompSampleFile",)


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