#!/usr/bin/env python
# encoding: utf-8

import xadmin
from samples.models import *


class exploSampleAdmin(object):
    list_display = ["sname", "sampleID", "user", "inputDate"]
    search_fields = ["sname", "sampleID", "user"]
    list_filter = ["sname", "sampleID", "user__name", "inputDate", "sampleState", "sampleOrigin",
                    "sampleType", "sampleMake", "sampleDraw", "sampleAnalyse", "analyseCondition"]


class exploChSampleAdmin(object):
    list_display = ["exploSample", "name", "content", "offset"]
    list_filter = ["exploSample__sname", "name"]
    search_fields = ["exploSample__sname", "name" ]


class exploSampleFileAdmin(object):
    list_display = [" exploSample", " user","inputDate"]
    list_filter = ["exploSample__sname"]


class exploSamplePeakAdmin(object):
    list_display = ["exploSampleFile", "peakStart", "peakEnd","peakHeight","peakArea"]


class devCompSampleAdmin(object):
    list_display = ["sname", "sampleID", "user", "inputDate"]


class devCompChSampleAdmin(object):
    list_display = ["devCompSample", "name", "content", "offset"]


class devCompSampleFileAdmin(object):
    list_display = [" devCompSample", " user", "inputDate"]

class devCompSamplePeakAdmin(object):
    list_display = ["devCompSampleFile", "peakStart", "peakEnd","peakHeight","peakArea"]

class devShapeSampleAdmin(object):
    list_display = ["isCircuit","sname", "sampleID", "user", "inputDate"]


xadmin.site.register(exploSample, exploSampleAdmin)
xadmin.site.register(exploChSample, exploChSampleAdmin)
xadmin.site.register(exploSampleFile, exploSampleFileAdmin)
xadmin.site.register( exploSamplePeak,  exploSamplePeakAdmin)

xadmin.site.register(devCompSample, devCompSampleAdmin)
xadmin.site.register(devCompChSample, devCompChSampleAdmin)
xadmin.site.register(devCompSampleFile, devCompSampleFileAdmin)
xadmin.site.register(devCompSamplePeak, devCompSamplePeakAdmin)

xadmin.site.register(devShapeSample, devShapeSampleAdmin)

