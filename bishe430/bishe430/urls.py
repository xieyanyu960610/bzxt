"""bishe430 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# -*- coding: utf-8 -*-


from django.conf.urls import url,include
# from django.contrib import admin
import xadmin
from bishe430.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from samples.views import *
from evis.views import *
from apps.users.views import UserViewset
from user_operation.views import *


from django.conf.urls import url
from samples import views





router = DefaultRouter()

#配置exploSamples的url
router.register(r'exploSamples', exploSampleViewset, base_name="exploSamples")


#配置exploSampleFiles的url
router.register(r'exploSampleFiles', exploSampleFileViewset, base_name="exploSampleFiles")

router.register(r'exploSamplePeaks', exploSamplePeakViewset, base_name="exploSamplePeaks")

router.register(r'exploChSamples',exploChSampleViewset, base_name="exploChSamples")

router.register(r'devCompSampleFiles', devCompSampleFileViewset, base_name="devCompSampleFiles")

router.register(r'devCompSamplePeaks', devCompSamplePeakViewset, base_name="devCompSamplePeaks")

router.register(r'devCompChSamples', devCompChSampleViewset, base_name="devCompChSamples")

router.register(r'devCompSamples', devCompSampleViewset, base_name="devCompSamples")

router.register(r'devShapeSamples', devShapeSampleViewset, base_name="devShapeSamples")

router.register(r'exploEvis', exploEviViewset, base_name="exploEvis")

router.register(r'exploEviFiles', exploEviFileViewset, base_name="exploEviFiles")

router.register(r'exploEviPeaks', exploEviPeakViewset, base_name="exploEviPeaks")

router.register(r'exploChEvis', exploChEviViewset, base_name="exploChEvis")

router.register(r'devCompEviFiles', devCompEviFileViewset, base_name="devCompEviFiles")

router.register(r'devCompEviPeaks', devCompEviPeakViewset, base_name="devCompEviPeaks")

router.register(r'devCompChEvis', devCompChEviViewset, base_name="devCompChEvis")

router.register(r'devCompEvis',devCompEviViewset, base_name="devCompEvis")

router.register(r'devShapeEvis', devShapeEviViewset, base_name="devShapeEvis")

router.register(r'exploMatchs', exploMatchViewset, base_name="exploMatchs")

router.register(r'devCompMatchs', devCompMatchViewset, base_name="devCompMatchs")

router.register(r'devShapeMatchs', devShapeMatchViewset, base_name="devShapeMatchs")

router.register(r'users', UserViewset, base_name="users")
urlpatterns = [
     url(r'^xadmin/', xadmin.site.urls),
     url(r'^media/(?P<path>.*)$',  serve, {"document_root":MEDIA_ROOT}),

     url(r'^', include(router.urls)),
     # # drf自带的token认证模式
     # url(r'^api-token-auth/', views.obtain_auth_token),

     url(r'docs/', include_docs_urls(title="爆炸系统")),
     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

     # jwt的认证接口
     url(r'^login/', obtain_jwt_token),
     url(r'^api-token-auth/', obtain_jwt_token),

     url(r'^task/(\d+)/(\d+)/', views.tasks, name='task'),

     url(r'updateExploMatch/',views.updateExploMatch,name='updateExploMatch'),
     url(r'updateDevCompMatch/',views.updateDevCompMatch,name="updateDevCompMatch")



]
