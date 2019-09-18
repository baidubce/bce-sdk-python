#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: test_list_watermark.py
Date: 2015/06/23 19:42:24
"""

import os
import re
import sys
import time

_NOW_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
_COMMON_PATH = _NOW_PATH + '../../../'
sys.path.insert(0, _COMMON_PATH)

import mediaBase
import media_config
from baidubce.services.media import media_client
from baidubce.exception import BceHttpClientError
from baidubce.exception import BceServerError
from baidubce.exception import BceClientError

import nose
from nose.tools import raises

class TestListWatermark(mediaBase.MediaBase):
    """test list watermark"""
    def __init__(self):
        """construction """
        mediaBase.MediaBase.__init__(self)
        self.watermark_id = None
        self.watermark_id2 = None
        self.key = '120X90.jpg'
        self.client = media_client.MediaClient(media_config.config)

    def setUp(self):
        """create env"""
        time.sleep(1)
        succ = True
        try:
            self.watermark_id = self.client.create_watermark(self.watermarkBucket, 
                   self.key).watermark_id
        except Exception as e:
            succ = False
        nose.tools.assert_true(succ)
    
    def tearDown(self):
        """clear env"""
        time.sleep(1)
        success = True
        try:
            response = self.client.list_watermarks()
        except Exception as e:
            success = False
        nose.tools.assert_true(success)

        if self.watermark_id:
            self.client.delete_watermark(self.watermark_id)

        if self.watermark_id2:
            self.client.delete_watermark(self.watermark_id2)

        #watermarks = response.watermarks
        #for each_value in watermarks:
        #    self.client.delete_watermark(each_value.watermark_id)

    def test_list_watermark_add_one(self):
        """test list watermark with add ont watermark"""
        success = True
        try:
            response = self.client.list_watermarks()
        except Exception as e:
            success = False
        nose.tools.assert_true(success)
        count1 = len(response.watermarks)
        
        try:
            self.watermark_id2 = self.client.create_watermark(self.watermarkBucket, 
                   self.key, 0, 0).watermark_id
        except Exception as e:
            success = False
        nose.tools.assert_true(success)

        try:
            response = self.client.list_watermarks()
        except Exception as e:
            success = False
        nose.tools.assert_true(success)
        count2 = len(response.watermarks)
            
        nose.tools.assert_equal(count1 + 1, count2)

    def test_list_watermark_delete_one(self):
        """test list watermark with delete watermark"""
        success = True
        try:
            response = self.client.list_watermarks()
        except Exception as e:
            success = False
        nose.tools.assert_true(success)
        count1 = len(response.watermarks)
        
        try:
            self.client.delete_watermark(self.watermark_id)
        except Exception as e:
            success = False
        nose.tools.assert_true(success)
        self.watermark_id = None

        try:
            response = self.client.list_watermarks()
        except Exception as e:
            success = False
        nose.tools.assert_true(success)
        count2 = len(response.watermarks)
            
        nose.tools.assert_greater_equal(count1, 1)
        nose.tools.assert_greater_equal(count2, 0)
        #nose.tools.assert_equal(count1 - 1, count2)
