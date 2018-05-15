from rest_framework import serializers

from .models import *
from samples.serializers import  *
from evis.serializers import *



class exploMatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = exploMatch
        #返回id是为了方便删除
        fields = "__all__"

class exploMatchDetailSerializer(serializers.ModelSerializer):
    exploSample = exploSampleSerializer()
#    exploMatchSample = serializers.SerializerMethodField()
    exploEvi= exploEviSerializer()


    class Meta:
        model = exploMatch
        fields = ("id", "matchType","matchModel","matchDegree", "exploSample", "exploEvi")


class devCompMatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = devCompMatch
        #返回id是为了方便删除
        fields = "__all__"

class devCompMatchDetailSerializer(serializers.ModelSerializer):
    devCompSample = devCompSampleSerializer()
    devCompEvi= devCompEviSerializer()

    class Meta:
        model = devCompMatch
        fields = ("id", "matchType", "matchModel","matchDegree", "devCompSample", "devCompEvi")


class devShapeMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = devShapeMatch
        # 返回id是为了方便删除
        fields = "__all__"


class devShapeMatchDetailSerializer(serializers.ModelSerializer):
    devShapeSample =devShapeSampleSerializer()
    devShapeEvi = devShapeEviSerializer()

    class Meta:
        model = devShapeMatch
        fields = ("id", "matchType", "matchCoordi", "devShapeSample","devShapeEvi")
