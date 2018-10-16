# _*_ encoding:utf-8 _*_
from datetime import datetime
import os

from django.db import models
from apps.users.models import UserProfile
from bishe430.settings import MEDIA_ROOT


class Image(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    url = models.ImageField(upload_to="image/test/", null=True, blank=True, verbose_name='图片测试url')

    class Meta:
        verbose_name = '图片测试'
        verbose_name_plural = verbose_name



# Create your models here.
class exploSample(models.Model):
    """
    炸药及原材料常见样本表
    """

    sname =models.CharField(max_length=10,verbose_name="样本名称")
    sampleID =models.CharField(max_length=10,verbose_name="样本编号")
    user = models.ForeignKey(UserProfile, verbose_name=u"处理人员")
    inputDate =models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    sampleState =models.CharField(max_length=30,null=True, blank=True,verbose_name="样本状态")
    sampleOrigin =models.CharField(max_length=30,null=True, blank=True,verbose_name="样本产地")
    sampleType =models.CharField(max_length=30, null=True, blank=True,verbose_name="样本种类")
    sampleMake =models.CharField(max_length=30, null=True, blank=True,verbose_name="样本制备方法")
    sampleDraw =models.CharField(max_length=30,null=True, blank=True, verbose_name="样本提取方法")
    sampleAnalyse =models.CharField(max_length=30,null=True, blank=True, verbose_name="样本分析方法")
    analyseCondition =models.CharField(max_length=30,null=True, blank=True, verbose_name="分析条件")
    picUrl =models.ImageField(max_length=100,upload_to="image/exploSample/",null=True,blank=True,verbose_name="炸药外观图片路径")
    picDescrip =models.CharField(max_length=100, null=True, blank=True, verbose_name="图片描述")
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name="备注")
 #   isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "炸药及原材料常见样本表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sname


class exploSampleFile(models.Model):
    """
    炸药及原材料常见样本文件存储表
    """
    def get_file_path(instance, filename):
        return 'file/exploSampleFile/%s/%s/%s' % (instance.exploSample.sname, instance.strength, filename)

    DETECT_TYPE = (
        (1, "FTIF"),
        (2, "Raman"),
        (3, "XRD"),
        (4, "XRF"),
        (5, "GC-MS"),
    )
    DOC_TYPE = (
        (1, "txt"),
        (2, "excel"),
        (3, "PDF"),
    )
    exploSample=models.ForeignKey(exploSample, verbose_name=u"对应的炸药样本",related_name="exploSampleFile",on_delete=models.CASCADE)
    user= models.ForeignKey(UserProfile, verbose_name=u"处理人员")
    detectDevice =models.CharField(max_length=30, null=True, blank=True, verbose_name="检测设备名称及型号")
    detectMrfs =models.CharField(max_length=20, null=True, blank=True, verbose_name="仪器厂家")
    inputDate=models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    detectType =models.IntegerField(choices=DETECT_TYPE, verbose_name="检测数据类型")
    docType =models.IntegerField(choices=DOC_TYPE,null=True,blank=True, verbose_name="录入文档格式")
    docUrl =models.FileField(max_length=100,upload_to=get_file_path,null=True,blank=True,verbose_name="录入文档路径")
    strength = models.CharField(max_length=20, default="", verbose_name="浓度")
    #handledUrl2 = models.CharField(max_length=200,null=True,blank=True,verbose_name="处理完的文件",)
    handledUrl = models.FileField(max_length=100,null=True,blank=True,verbose_name="处理完的文件")
 #   isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")




    class Meta:
        verbose_name = "炸药及原材料常见样本文件存储表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s(%d)".format(self.exploSample.sname, self.detectType)


class exploChSample(models.Model):
    """
    炸药及原材料常见样本子元素表
    """
    exploSampleFile = models.ForeignKey(exploSampleFile, verbose_name=u"对应的炸药文件", related_name="exploChSample",
                                        on_delete=models.CASCADE)
    detectType =models.CharField(max_length=20,null=True,blank=True,verbose_name='检测类型')
    elementsList = models.CharField(max_length=300,null=True,blank=True,verbose_name='元素列表')
    #isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "炸药及原材料常见样本子元素表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.exploSampleFile.exploSample.sname


class exploSamplePeak(models.Model):
    """
    炸药及原材料常见样本峰值表
    """
    exploSampleFile = models.ForeignKey(exploSampleFile, verbose_name=u"对应的炸药文件",related_name="exploSamplePeak",on_delete=models.CASCADE)
    peakPos = models.FloatField(default=0, verbose_name="峰高位置")
    peakHeight = models.FloatField(default=0, verbose_name="峰高")
    peakArea = models.FloatField(default=0, verbose_name="峰面积")
    class Meta:
        verbose_name = "炸药及原材料常见样本峰值表"
        verbose_name_plural = verbose_name


class devCompSample(models.Model):
    """
    爆炸装置常见样本成分表
    """
    sname = models.CharField(max_length=50, verbose_name="物品名称及测量部位")
    sampleID = models.CharField(max_length=10, verbose_name="样本编号")
    user = models.ForeignKey(UserProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    sampleState =models.CharField(max_length=30,null=True, blank=True,verbose_name="样本状态")
    sampleOrigin =models.CharField(max_length=30,null=True, blank=True,verbose_name="样本产地")
    sampleType =models.CharField(max_length=30, null=True, blank=True,verbose_name="样本种类")
    sampleMake =models.CharField(max_length=30, null=True, blank=True,verbose_name="样本制备方法")
    sampleDraw =models.CharField(max_length=30,null=True, blank=True, verbose_name="样本提取方法")
    sampleAnalyse =models.CharField(max_length=30,null=True, blank=True, verbose_name="样本分析方法")
    analyseCondition = models.CharField(max_length=30, null=True, blank=True, verbose_name="分析条件")
    picUrl = models.ImageField(max_length=100, upload_to="image/devCompSample/", null=True, blank=True, verbose_name="爆炸装置样本外观图片路径")
    picDescrip = models.CharField(max_length=100, null=True, blank=True, verbose_name="图片描述")
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name="备注")
    #isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "爆炸装置常见样本成分表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sname


class devCompSampleFile(models.Model):
    """
    爆炸装置常见样本成分文件存储表
    """
    DETECT_TYPE = (
        (1, "FTIF"),
        (2, "Raman"),
        (3, "XRD"),
        (4, "XRF"),
        (5, "GC-MS"),
    )
    DOC_TYPE = (
        (1, "txt"),
        (2, "excel"),
        (3, "PDF"),
    )
    devCompSample = models.ForeignKey(devCompSample, verbose_name=u"对应的样本",related_name="devCompSampleFile",on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, verbose_name=u"处理人员")
    detectDevice = models.CharField(max_length=30, null=True, blank=True, verbose_name="检测设备名称及型号")
    detectMrfs = models.CharField(max_length=20, null=True, blank=True, verbose_name="仪器厂家")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    detectType = models.IntegerField(choices=DETECT_TYPE, verbose_name="检测数据类型")
    docType = models.IntegerField(choices=DOC_TYPE, null=True,blank=True,verbose_name="录入文档格式")
    docUrl = models.FileField(max_length=100, upload_to="file/devCompSampleFile/", null=True, blank=True,
                              verbose_name="录入文档路径")
    strength = models.CharField(max_length=20, default="", verbose_name="浓度")
    handledUrl = models.FileField(max_length=100, null=True, blank=True,
                                  verbose_name="处理完的文件")
    #isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "爆炸装置常见样本成分文件存储表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s(%d)".format(self.devCompSample.sname, self.detectType)

class devCompChSample(models.Model):
    """
    爆炸装置常见样本成分子元素表
    """
    devCompSampleFile = models.ForeignKey(devCompSampleFile, verbose_name=u"对应的物证文件",related_name="devCompChSample",on_delete=models.CASCADE)
    detectType =models.CharField(max_length=20,null=True,blank=True,verbose_name='检测类型')
    elementsList = models.CharField(max_length=300,null=True,blank=True,verbose_name='元素列表')
   # isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "爆炸装置常见样本成分子元素表"
        verbose_name_plural = verbose_name

    # def __str__(self):
    #     return self.devCompSampleFile.devCompSample.sname


class devCompSamplePeak(models.Model):
    """
    爆炸装置常见样本成分峰值表
    """
    devCompSampleFile = models.ForeignKey(devCompSampleFile, verbose_name=u"对应的物证文件",related_name="devCompSamplePeak",on_delete=models.CASCADE)
    peakPos = models.FloatField(default=0, verbose_name="峰高位置")
    peakHeight = models.FloatField(default=0, verbose_name="峰高")
    peakArea = models.FloatField(default=0, verbose_name="峰面积")
    class Meta:
        verbose_name = "爆炸装置常见样本成分峰值表"
        verbose_name_plural = verbose_name


class devShapeSample(models.Model):
    """
    爆炸装置常见样本形态表
    """
    # isCircuit =models.BooleanField(default=False, verbose_name="是否是电路板")
    sname = models.CharField(max_length=20, verbose_name="装置名称")
    sampleID = models.CharField(max_length=10, verbose_name="装置编号")
    belongTo =models.CharField(max_length=20,null=True, blank=True, verbose_name="所属装置")
    user = models.ForeignKey(UserProfile, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    mrfs=models.CharField(max_length=30,null=True, blank=True, verbose_name="厂家")
    sampleModel=models.CharField(max_length=20,null=True, blank=True, verbose_name="型号")
    trademark=models.CharField(max_length=30,null=True, blank=True, verbose_name="商标")
    function=models.CharField(max_length=100,null=True, blank=True, verbose_name="所属装置")
    isFirst = models.BooleanField(default=True,verbose_name="是否是第一次分割")
    rectCoordi=models.CharField(max_length=100,null=True, blank=True, verbose_name="矩形框坐标（4个）")
    proCoordi = models.CharField(max_length=400, null=True, blank=True, verbose_name="前景颜色点坐标")
    backCoordi=models.CharField(max_length=400,null=True, blank=True, verbose_name="背景颜色点坐标")
    boardCoordi=models.CharField(max_length=400,null=True, blank=True, verbose_name="主板颜色点坐标")
    blackWhiteUrl=models.ImageField(max_length=100,null=True, blank=True, verbose_name="黑白图像路径")#upload_to="image/devShapeSample/blackWhite/",
    interColorUrl=models.ImageField(max_length=100,null=True, blank=True, verbose_name="中间彩色图像路径")#,upload_to="image/devShapeSample/interColor/"
    middleResultUrl = models.FileField(max_length=100,null=True, blank=True,verbose_name="第一次文件路径")#,upload_to="file/devShapeSample/middleResult"
    compCheckCoordi=models.CharField(max_length=400,null=True, blank=True, verbose_name="元器件点坐标（校验）")
    boardCheckCoordi=models.CharField(max_length=400,null=True, blank=True, verbose_name="主板像素坐标（校验）")
    featureUrl=models.FileField(max_length=100,null=True, blank=True, verbose_name="特征文件路径")#, upload_to="file/devShapeSample/feature"
    resultPicUrl=models.ImageField(max_length=100,null=True, blank=True, verbose_name="结果图像形式路径")#upload_to="image/devShapeSample/result/",
    resultFileUrl=models.FileField(max_length=100,null=True, blank=True, verbose_name="结果文件形式路径")# upload_to="file/devShapeSample/result/",
    originalUrl =models.ImageField(max_length=100,upload_to="image/devShapeSample/original/",null=True,blank=True,verbose_name="原始图像文件路径")#
    originalResolution =models.CharField(max_length=30,null=True, blank=True, verbose_name="原始图像采集分辨率")
    nomUrl =models.ImageField(max_length=100,upload_to="image/devShapeSample/nom/",null=True,blank=True,verbose_name="归一化图像文件路径")#
    nomResolution=models.CharField(max_length=30,null=True, blank=True, verbose_name="归一化图像分辨率")
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name="备注")
   # isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "爆炸装置常见样本形态表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sname