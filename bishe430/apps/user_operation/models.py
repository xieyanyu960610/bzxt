from django.db import models

from samples.models import *
from evis.models import *

# Create your models here.
class exploMatch(models.Model):
    """
    炸药及原材料物证匹配结果表
    """
    DETECT_TYPE = (
        (1, "FTIF"),
        (2, "Raman"),
        (3, "XRD"),
        (4, "XRF"),
        (5, "GC-MS"),
    )
    exploSample = models.ForeignKey(exploSample,null=True,blank=True, verbose_name=u"对应的样本",related_name="exploMatchSample",on_delete=models.CASCADE)
    exploEvi = models.ForeignKey(exploEvi, verbose_name=u"对应的物证",related_name="exploMatchEvi",on_delete=models.CASCADE)
    matchType =models.IntegerField(choices=DETECT_TYPE, verbose_name="匹配数据类型")
    matchModel =models.CharField(max_length=20,null=True,blank=True,verbose_name='检测类型')
    matchDegree =models.FloatField(default=0.0,verbose_name="匹配程度")
    isSure = models.BooleanField(default=False, verbose_name="是否确认")
  #  isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "炸药及原材料物证匹配结果表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s(%d)".format(self. exploSample.sname, self.exploEvi.evidenceID)


class devCompMatch(models.Model):
    """
    爆炸装置案件物证成分匹配结果表
    """
    DETECT_TYPE = (
        (1, "FTIF"),
        (2, "Raman"),
        (3, "XRD"),
        (4, "XRF"),
        (5, "GC-MS"),
    )
    devCompSample = models.ForeignKey(devCompSample, null=True,blank=True,verbose_name=u"对应的成分样本",related_name="devCompMatchSample",on_delete=models.CASCADE)
    devCompEvi = models.ForeignKey(devCompEvi, verbose_name=u"对应的物证",related_name="devCompMatchEvi",on_delete=models.CASCADE)
    matchType =models.IntegerField(choices=DETECT_TYPE, verbose_name="匹配数据类型")
    matchModel =models.CharField(max_length=20,null=True,blank=True,verbose_name='检测类型')
    matchDegree =models.FloatField(default=0.0,verbose_name="匹配程度")
    strength = models.CharField(max_length=20, default="千分之一", verbose_name="浓度")
    isSure = models.BooleanField(default=False, verbose_name="是否确认")
 #   isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "爆炸装置案件物证成分匹配结果表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s(%d)".format(self. devCompSample.sname, self.devCompEvi.evidenceID)


class devShapeMatch(models.Model):
    """
   爆炸装置案件物证形态匹配结果表
    """
    devShapeSample = models.ForeignKey(devShapeSample, null=True,blank=True,verbose_name=u"对应的成分样本",related_name="devShapeMatchSample",on_delete=models.CASCADE)
    devShapeEvi = models.ForeignKey(devShapeEvi, verbose_name=u"对应的物证",related_name="devShapeMatchEvi",on_delete=models.CASCADE)
    isCircuit = models.BooleanField(default=False, verbose_name="是否是元器件匹配")
    matchDegree =models.FloatField(default=0.0,verbose_name="得分")
    matchSampleCoordi = models.CharField(max_length=400, null=True, blank=True, verbose_name="匹配的样本位置坐标")
    matchEviCoordi = models.CharField(max_length=400, null=True, blank=True, verbose_name="匹配的物证位置坐标")
    isSure = models.BooleanField(default=False, verbose_name="是否确认")
    class Meta:
        verbose_name = "爆炸装置案件物证形态匹配结果表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s(%d)".format(self.devShapeSample.sname, self.devShapeEvi.eviID)