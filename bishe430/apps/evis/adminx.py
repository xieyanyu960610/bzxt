#!/usr/bin/env python
# encoding: utf-8

import xadmin
from evis.models import *


class exploEviAdmin(object):
    list_display = ["caseID", "evidenceID", "user", "inputDate"]
    search_fields = ["caseID", "evidenceID", "user__name"]
    list_filter = ["caseID", "evidenceID", "user__name" ]


class exploChEviAdmin(object):
    list_display = ["exploEvi", "name", "content", "offset"]
    list_filter = ["exploEvi__sname", "name"]
    search_fields = ["exploEvi__sname", "name" ]


class exploEviFileAdmin(object):
    list_display = [" exploEvi", " user","inputDate"]
    list_filter = ["exploEvi__sname"]


class exploEviPeakAdmin(object):
    list_display = [" exploEviFile", "peakStart", "peakEnd","peakHeight","peakArea"]


class devCompEviAdmin(object):
    list_display = ["caseID", "evidenceID", "user", "inputDate"]


class devCompChEviAdmin(object):
    list_display = ["devCompEvi", "name", "content", "offset"]


class devCompEviFileAdmin(object):
    list_display = [" devCompEvi", " user", "inputDate"]

class devCompEviPeakAdmin(object):
    list_display = ["devCompEviFile", "peakStart", "peakEnd","peakHeight","peakArea"]

class devShapeEviAdmin(object):
    list_display = ["isCircuit", "eviID", "user", "inputDate"]


xadmin.site.register(exploEvi, exploEviAdmin)
xadmin.site.register(exploChEvi, exploChEviAdmin)
xadmin.site.register(exploEviFile, exploEviFileAdmin)
xadmin.site.register( exploEviPeak, exploEviPeakAdmin)

xadmin.site.register(devCompEvi, devCompEviAdmin)
xadmin.site.register(devCompChEvi, devCompChEviAdmin)
xadmin.site.register(devCompEviFile, devCompEviFileAdmin)
xadmin.site.register(devCompEviPeak, devCompEviPeakAdmin)

xadmin.site.register(devShapeEvi, devShapeEviAdmin)
