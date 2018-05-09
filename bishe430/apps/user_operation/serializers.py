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
    exlpoMatchSample = exploSampleSerializer(many=True)
    exlpoMatchEvi= exploEviSerializer(many=True)

    class Meta:
        model = exploMatch
        fields = ("id", "matchType", "matchDegree", "exlpoMatchSample", "exlpoMatchEvi")


class devCompMatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = devCompMatch
        #返回id是为了方便删除
        fields = "__all__"

class devCompMatchDetailSerializer(serializers.ModelSerializer):
    devCompMatchSample = devCompSampleSerializer(many=True)
    devCompMatchEvi= devCompEviSerializer(many=True)

    class Meta:
        model = devCompMatch
        fields = ("id", "matchType", "matchDegree", "devCompMatchSample ", "devCompMatchEvi")


class devShapeMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = devShapeMatch
        # 返回id是为了方便删除
        fields = "__all__"


class devShapeMatchDetailSerializer(serializers.ModelSerializer):
    devShapeMatchSample =devShapeSampleSerializer(many=True)
    devShapeMatchEvi = devShapeEviSerializer(many=True)

    class Meta:
        model = devShapeMatch
        fields = ("id", "matchType", "matchCoordi", "devShapeMatchSample ", "devShapeMatchEvi")
