#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: test_delete_watermark.py
Date: 2015/06/24 10:42:24
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

class TestDeleteWatermark(mediaBase.MediaBase):
    """test delete watermark"""
    def __init__(self):
        """construction """
        mediaBase.MediaBase.__init__(self)
        self.watermark_id = 'wmk-jdiwe1956a3yzbkq'
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
        time.sleep(2)
        if self.watermark_id:
            success = True
            try:
                self.client.delete_watermark(self.watermark_id)
                self.watermark_id = None
            except Exception as e:
                success = False
            nose.tools.assert_true(success)
    
    def test_delete_watermark_exist(self):
        """delete exist watermark"""
        succ = True
        try:
            self.client.delete_watermark(self.watermark_id)
            self.watermark_id = None
        except Exception as e:
            succ = False
        nose.tools.assert_true(succ)

    def test_delete_watermark_not_exist(self):
        """delete not exist watermark"""
        succ = True
        try:
            self.client.delete_watermark('not_exist_watermark')
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'watermark: not_exist_watermark does not exist')
            else:
                assert True == False, 'not throw BceServerError '

    def test_delete_watermark_repeated(self):
        """ deleted watermark repeated"""
        succ = True
        try:
            self.client.delete_watermark(self.watermark_id)
            watermark_id = self.watermark_id
            self.watermark_id = None
            self.client.delete_watermark(watermark_id)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('watermark: ')
            else:
                assert True == False, 'not throw BceServerError '

    def test_delete_watermark_with_name_none(self):
        """delete watermark name none"""
        with nose.tools.assert_raises_regexp(ValueError, 
                'arg "watermark_id" should not be None'):
            self.client.delete_watermark(None)

    def test_delete_watermark_with_name_empty(self):
        """delete watermark name empty """
        with nose.tools.assert_raises_regexp(BceClientError, 
                'watermark_id can\'t be empty string'):
            self.client.delete_watermark('')
