#!/usr/bin/env python
# encoding: utf-8

import xadmin
from user_operation.models import *


class exploMatchAdmin(object):
    list_display = ["exploSample", "exploEvi"]
    search_fields = ["exploSample", "exploEvi"]
    list_filter = ["exploSample", "exploEvi"]


class devCompMatchAdmin(object):
    list_display = ["exploEvi", "name", "content", "offset"]
    list_filter = ["exploEvi__sname", "name"]
    search_fields = ["exploEvi__sname", "name" ]


class devShapeMatchAdmin(object):
    list_display = ["devShapeSample", "devShapeEvi"]
    list_filter = ["devShapeSample", "devShapeEvi"]

xadmin.site.register(exploMatch, exploMatchAdmin)
xadmin.site.register(devCompMatch, devCompMatchAdmin)
xadmin.site.register(devShapeMatch, devShapeMatchAdmin)
