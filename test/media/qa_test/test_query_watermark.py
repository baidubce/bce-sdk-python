#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: test_create_watermark.py
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

class TestQueryWatermark(mediaBase.MediaBase):
    """test create watermark"""
    def __init__(self):
        """construction """
        mediaBase.MediaBase.__init__(self)
        self.watermark_id = 'wmk-jdkwykir3c2ezuag'
        self.key = '120X90.jpg'
        self.client = media_client.MediaClient(media_config.config)

    def setUp(self):
        """create env"""
        time.sleep(2)
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
    
    def test_query_watermark_exist(self):
        """query exist watermark"""
        succ = True
        try:
            self.client.get_watermark(self.watermark_id)
        except Exception as e:
            succ = False
        nose.tools.assert_true(succ)

    def test_query_watermark_not_exist(self):
        """query not exist watermark"""
        succ = True
        try:
            self.client.get_watermark('not_exist_watermark')
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'watermark: not_exist_watermark does not exist')
            else:
                assert True == False, 'not throw BceServerError '

    def test_query_watermark_deleted(self):
        """query deleted watermark"""
        succ = True
        try:
            self.client.delete_watermark(self.watermark_id)
            watermark_id = self.watermark_id
            self.watermark_id = None
            self.client.get_watermark(watermark_id)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('watermark: ')
            else:
                assert True == False, 'not throw BceServerError '

    def test_query_watermark_with_watermark_none(self):
        """query watermark with watermark name is none"""
        with nose.tools.assert_raises_regexp(ValueError, 
                'arg "watermark_id" should not be None'):
            self.client.get_watermark(None)

    def test_query_watermark_with_watermark_empty(self):
        """query watermark with watermark name is empty"""
        with nose.tools.assert_raises_regexp(BceClientError, 
                'watermark_id can\'t be empty string'):
            self.client.get_watermark('')
