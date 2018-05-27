#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from celery import task
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import math

from .models import *
from .serializers import *
from bishe430.settings import MEDIA_ROOT,BASE_DIR
from user_operation.models import *
from evis.models import *
from utils.XRDhandle import *

@task()
def add(x, y):
    time.sleep(10.0)
    return x + y


@task
def run_test_suit(ts_id):
    print ("++++++++++++++++++++++++++++++++++++")
    print('jobs[ts_id=%s] running....' % ts_id)
    time.sleep(10.0)
    print('jobs[ts_id=%s] done' % ts_id)
    result = True
    return result

@task
def renew(fileId):
    file = exploSampleFile.objects.get(id=fileId)
    print("start")
    # start =time.time()
    def pearson(txt_1, txt_2):
        signal_1 = np.loadtxt(txt_1)[1]
        print(signal_1)
        signal_2 = np.loadtxt(txt_2)[1]
        print(signal_2)
        n = len(signal_1)
        mean1 = signal_1.mean()
        mean2 = signal_2.mean()
        standvalue1 = math.sqrt(sum((signal_1 - mean1) * (signal_1 - mean1)))
        standvalue2 = math.sqrt(sum((signal_2 - mean2) * (signal_2 - mean2)))
        cov = sum((signal_1 - mean1) * (signal_2 - mean2))
        pearson = cov / (standvalue1 * standvalue2)
        return pearson


    evi_files = os.path.join(MEDIA_ROOT, "file\exploEviFile\handled")
    all_file = os.listdir(evi_files)
    for i in range(0, len(all_file)):
        if os.path.splitext(all_file[i])[1] == '.txt':
            cur_path = os.path.join(evi_files, all_file[i])
            cur_txt = all_file[i]
            txt_id = os.path.splitext(cur_txt)[0]
            # exploEviMatch = exploEvi.objects.get(id=txt_id)
            cur_score = pearson(os.path.join(MEDIA_ROOT, str(file.handledUrl)), cur_path)
            eviMatchs = exploMatch.objects.filter(exploEvi_id=txt_id).filter(
                matchType=3)  # exploEvi.objects.get(id = txt_id))
            sampleMatch = eviMatchs.filter(exploSample_id=file.exploSample.id)
            evis = eviMatchs.order_by("matchDegree")

            if len(sampleMatch) == 0:
                if len(evis) != 0:
                    if cur_score > evis[0].matchDegree:
                        if len(evis) == 10:
                            evis[0].delete()

                        explo_match = exploMatch()
                        explo_match.exploSample = file.exploSample
                        explo_match.exploEvi_id = txt_id  # exploEviMatch
                        explo_match.matchType = 3
                        explo_match.matchDegree = cur_score
                        explo_match.save()
                else:
                    for i in similarity_rank(cur_path,
                                             os.path.join(MEDIA_ROOT, "file\exploSampleFile\handled")):
                        explo_match = exploMatch()
                        explo_match.exploSample_id = i[0]
                        explo_match.exploEvi_id = txt_id  # exploEviMatch
                        explo_match.matchType = 3
                        explo_match.matchDegree = i[1]
                        explo_match.save()
            else:
                if cur_score >= evis[0].matchDegree:
                    sampleMatch[0].matchDegree = cur_score
                    sampleMatch[0].save()
                else:
                    for evi in evis:
                        evi.delete()
                    for i in similarity_rank(cur_path,
                                             os.path.join(MEDIA_ROOT, "file\exploSampleFile\handled")):
                        explo_match = exploMatch()
                        explo_match.exploSample_id = i[0]
                        explo_match.exploEvi_id = txt_id  # exploEviMatch
                        explo_match.matchType = 3
                        explo_match.matchDegree = i[1]
                        explo_match.save()
    # end = time.time()
    # print(end - start)
    print("end")

@task
def renew2():
    print("start")
    # start =time.time()
    exploMatch.objects.all().delete()
    evi_files = os.path.join(MEDIA_ROOT, "file\exploEviFile\handled")
    all_file = os.listdir(evi_files)
    for i in range(0, len(all_file)):
        if os.path.splitext(all_file[i])[1] == '.txt':
            cur_path = os.path.join(evi_files, all_file[i])
            cur_txt = all_file[i]
            txt_id = os.path.splitext(cur_txt)[0]
            # eviMatchs = exploMatch.objects.filter(exploEvi_id=txt_id).filter(
            #     matchType=3)  # exploEvi.objects.get(id = txt_id))
            # evis = eviMatchs.order_by("matchDegree")
            #
            # for evi in evis:
            #     evi.delete()
            for i in similarity_rank(cur_path,
                                     os.path.join(MEDIA_ROOT, "file\exploSampleFile\handled")):
                explo_match = exploMatch()
                explo_match.exploSample_id = i[0]
                explo_match.exploEvi_id = txt_id  # exploEviMatch
                explo_match.matchType = 3
                explo_match.matchDegree = i[1]
                explo_match.save()

    # end = time.time()
    # print(end - start)
    print("end")