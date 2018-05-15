from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class exploEvi(models.Model):
    """
    炸药及原材料案件物证表
    """
    caseID = models.CharField(max_length=10, verbose_name="案件编号")
    evidenceID = models.CharField(max_length=10, verbose_name="物证编号")
    user = models.ForeignKey(User, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    eviState = models.CharField(max_length=30, null=True, blank=True, verbose_name="物证状态")
    eviMake = models.CharField(max_length=30, null=True, blank=True, verbose_name="物证制备方法")
    eviDraw = models.CharField(max_length=30, null=True, blank=True, verbose_name="物证提取方法")
    eviAnalyse= models.CharField(max_length=30, null=True, blank=True, verbose_name="物证分析方法")
    analyseCondition = models.CharField(max_length=30, null=True, blank=True, verbose_name="分析条件")
    picUrl = models.ImageField(max_length=100, upload_to="image/exploEvi/", null=True, blank=True, verbose_name="炸药物证外观图片路径")
    picDescrip = models.CharField(max_length=100, null=True, blank=True, verbose_name="图片描述")
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name="备注")
   # isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "炸药及原材料案件物证表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.evidenceID


class exploEviFile(models.Model):
    """
    炸药及原材料案件物证文件存储表
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
    exploEvi = models.ForeignKey(exploEvi, verbose_name=u"对应的物证",related_name="exploEviFile",on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=u"处理人员",on_delete=models.CASCADE)
    detectDevice = models.CharField(max_length=30, null=True, blank=True, verbose_name="检测设备名称及型号")
    detectMrfs = models.CharField(max_length=20, null=True, blank=True, verbose_name="仪器厂家")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    detectType = models.IntegerField(choices=DETECT_TYPE, verbose_name="检测数据类型")
    docType = models.IntegerField(choices=DOC_TYPE, null=True, blank=True,verbose_name="录入文档格式")
    docUrl = models.FileField(max_length=100, upload_to="file/exploEviFile/", null=True, blank=True,
                              verbose_name="录入文档路径")
    handledUrl = models.FileField(max_length=100, null=True, blank=True,
                                  verbose_name="处理完的文件")
  #  isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "炸药及原材料案件物证文件存储表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%d(%d)".format(self. exploEvi.evidenceID, self.detectType)
class exploChEvi(models.Model):
    """
    炸药及原材料案件物证子元素表
    """
    exploEviFile = models.ForeignKey(exploEviFile, verbose_name=u"对应的物证文件",related_name="exploChEvi",on_delete=models.CASCADE)
    detectType =models.CharField(max_length=20,null=True,blank=True,verbose_name='检测类型')
    elementsList = models.CharField(max_length=300,null=True,blank=True,verbose_name='元素列表')
  # isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "炸药及原材料案件物证子元素表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.exploEviFile.exploEvi.evidenceID


class exploEviPeak(models.Model):
    """
    炸药及原材料案件物证峰值表
    """
    exploEviFile = models.ForeignKey(exploEviFile, verbose_name=u"对应的物证文件",related_name="exploEviPeak",on_delete=models.CASCADE)
    peakPos = models.FloatField(default=0, verbose_name="峰高位置")
    peakHeight = models.FloatField(default=0, verbose_name="峰高")
    peakArea = models.FloatField(default=0, verbose_name="峰面积")
    class Meta:
        verbose_name = "炸药及原材料案件物证峰值表"
        verbose_name_plural = verbose_name


class devCompEvi(models.Model):
    """
    爆炸装置案件物证成分表
    """
    caseID = models.CharField(max_length=10, verbose_name="案件编号")
    evidenceID = models.CharField(max_length=10, verbose_name="物证编号")
    user = models.ForeignKey(User, verbose_name=u"处理人员")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    eviState = models.CharField(max_length=30, null=True, blank=True, verbose_name="物证状态")
    eviMake = models.CharField(max_length=30, null=True, blank=True, verbose_name="物证制备方法")
    eviDraw = models.CharField(max_length=30, null=True, blank=True, verbose_name="物证提取方法")
    eviAnalyse = models.CharField(max_length=30, null=True, blank=True, verbose_name="物证分析方法")
    analyseCondition = models.CharField(max_length=30, null=True, blank=True, verbose_name="分析条件")
    picUrl = models.ImageField(max_length=100, upload_to="image/devCompEvi/", null=True, blank=True, verbose_name="装置物证外观图片路径")
    picDescrip = models.CharField(max_length=100, null=True, blank=True, verbose_name="图片描述")
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name="备注")
   # isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "爆炸装置案件物证成分表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.evidenceID



class devCompEviFile(models.Model):
    """
    爆炸装置案件物证成分文件存储表
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
    devCompEvi = models.ForeignKey(devCompEvi, verbose_name=u"对应的物证",related_name="devCompEviFile",on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=u"处理人员",on_delete=models.CASCADE)
    detectDevice = models.CharField(max_length=30, null=True, blank=True, verbose_name="检测设备名称及型号")
    detectMrfs = models.CharField(max_length=20, null=True, blank=True, verbose_name="仪器厂家")
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    detectType = models.IntegerField(choices=DETECT_TYPE, verbose_name="检测数据类型")
    docType = models.IntegerField(choices=DOC_TYPE, null=True, blank=True,verbose_name="录入文档格式")
    docUrl = models.FileField(max_length=100, upload_to="file/devCompEviFile/", null=True, blank=True,
                              verbose_name="录入文档路径")
    handledUrl = models.FileField(max_length=100, null=True, blank=True,
                                  verbose_name="处理完的文件")
 #   isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "爆炸装置案件物证成分文件存储表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%d(%d)".format(self. devCompEvi.evidenceID, self.detectType)


class devCompChEvi(models.Model):
    """
    爆炸装置案件物证成分子元素表
    """
    devCompEviFile = models.ForeignKey(devCompEviFile, verbose_name=u"对应的物证文件",related_name="devCompChEvi",on_delete=models.CASCADE)
    detectType =models.CharField(max_length=20,null=True,blank=True,verbose_name='检测类型')
    elementsList = models.CharField(max_length=300,null=True,blank=True,verbose_name='元素列表')
#    isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "爆炸装置案件物证成分子元素表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.devCompEviFile.devCompEvi.evidenceID

class devCompEviPeak(models.Model):
    """
    爆炸装置案件物证成分峰值表
    """
    devCompEviFile = models.ForeignKey(devCompEviFile, verbose_name=u"对应的物证文件",related_name="devCompEviPeak",on_delete=models.CASCADE)
    peakPos = models.FloatField(default=0, verbose_name="峰高位置")
    peakHeight = models.FloatField(default=0, verbose_name="峰高")
    peakArea = models.FloatField(default=0, verbose_name="峰面积")
    class Meta:
        verbose_name = "爆炸装置案件物证成分峰值表"
        verbose_name_plural = verbose_name


class devShapeEvi(models.Model):
    """
    爆炸装置案件物证形态表
    """
    isCircuit = models.BooleanField(default=False, verbose_name="是否是电路板")
    eviID = models.CharField(max_length=10, verbose_name="物证编号")
    user = models.ForeignKey(User, verbose_name=u"处理人员")#,on_delete=models.CASCADE)
    inputDate = models.DateTimeField(default=datetime.now, verbose_name=u"录入日期")
    rectCoordi = models.CharField(max_length=100, null=True, blank=True, verbose_name="矩形框坐标（4个）")
    proCoordi = models.CharField(max_length=400, null=True, blank=True, verbose_name="前景颜色点坐标")
    backCoordi = models.CharField(max_length=400, null=True, blank=True, verbose_name="背景颜色点坐标")
    boardCoordi = models.CharField(max_length=400, null=True, blank=True, verbose_name="主板颜色点坐标")
    blackWhiteUrl = models.ImageField(max_length=100, upload_to="image/devShapeEvi/blackWhite/", null=True,
                                      blank=True, verbose_name="黑白图像路径")
    interColorUrl = models.ImageField(max_length=100, upload_to="image/devShapeEvi/interColor/", null=True,
                                      blank=True, verbose_name="中间彩色图像路径")
    compCheckCoordi = models.CharField(max_length=400, null=True, blank=True, verbose_name="元器件点坐标（校验）")
    boardCheckCoordi = models.CharField(max_length=400, null=True, blank=True, verbose_name="主板像素坐标（校验）")
    featureUrl = models.FileField(max_length=100, upload_to="file/devShapeEvi/feature", null=True, blank=True,
                                  verbose_name="特征文件路径")
    resultPicUrl = models.ImageField(max_length=100, upload_to="image/devShapeEvi/result/", null=True, blank=True,
                                     verbose_name="结果图像形式路径")
    resultFileUrl = models.FileField(max_length=100, upload_to="file/devShapeEvi/result/", null=True, blank=True,
                                     verbose_name="结果文件形式路径")
    originalUrl = models.ImageField(max_length=100, upload_to="image/devShapeEvi/original/", null=True, blank=True,
                                    verbose_name="原始图像文件路径")
    originalResolution = models.CharField(max_length=30, null=True, blank=True, verbose_name="原始图像采集分辨率")
    nomUrl = models.ImageField(max_length=100, upload_to="image/devShapeEvi/nom/", null=True, blank=True,
                               verbose_name="归一化图像文件路径")
    nomResolution = models.CharField(max_length=30, null=True, blank=True, verbose_name="归一化图像分辨率")
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name="备注")
   # isDelete = models.BooleanField(default=False, verbose_name="是否逻辑删除")
    class Meta:
        verbose_name = "爆炸装置案件物证形态表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.eviID
