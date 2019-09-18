#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: media_base.py
Date: 2015/06/11 11:06:20
"""

import datetime
import os
import time
import random
import sys

class MediaBase(object):
    """media base class"""
    def __init__(self):
        """init some Variable"""

        '''
        self.timeout = 30
#        self.sourceBucket = 'bucketin1'
#        self.targetBucket = 'bucketout1'
#        self.watermarkBucket = 'watermark'
        self.sourceBucket = 'sdk-input'
        self.targetBucket = 'sdk-output'
        self.watermarkBucket = 'sdk-watermark'
        #fileName is EnglishName
        self.fileKeyEnName = 'mediainfotest.mp4'
        self.fileKeyContainFolder = 'media/info/mediainfotest.mp4'
        self.fileKeyChName = '媒体信息测试.mp3'
        self.fileKeySpecialChars = 'test#@$%^()&test.mp3'
        self.prefix = 'mct_py_sdk_'
        '''

        self.timeout = 30
        self.sourceBucket = 'testmctjjm'
        self.targetBucket = 'testmctjjm'
        self.watermarkBucket = 'testmctjjm'
        # fileName is EnglishName
        self.fileKeyEnName = 'mediainfotest.mp4'
        self.fileKeyContainFolder = 'media/info/mediainfotest.mp4'
        self.fileKeyChName = '媒体信息测试.mp3'
        self.fileKeySpecialChars = 'test#@$%^()&test.mp3'
        self.prefix = 'test_'
        self.PY2 = sys.version_info[0] == 2
        self.PY3 = sys.version_info[0] == 3

         
    def convertName(self, name):
        """return  diffrent name"""
#        time = datetime.datetime.now().microsecond'
        name = '%s_%d%d' % (name, time.time()*1000, random.randint(100, 999))
        return name
