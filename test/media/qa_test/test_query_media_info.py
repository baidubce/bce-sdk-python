#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: test_query_media_info.py
Date: 2015/06/25 18:55:00
"""
import os
import sys
import unittest
import json
import time
import media_config
import re
import mediaBase

_NOW_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
_COMMON_PATH = _NOW_PATH + '../../../'
sys.path.insert(0, _COMMON_PATH)

from baidubce.services.media import media_client
from baidubce.exception import BceHttpClientError
from baidubce.exception import BceServerError
from baidubce.exception import BceClientError
import nose

class TestQueryMediaInfo(mediaBase.MediaBase):
    """test create pipeline"""
    def __init__(self):
        """construction """
        mediaBase.MediaBase.__init__(self)
        self.client = media_client.MediaClient(media_config.config)

    def setUp(self):
        """create env"""

    def tearDown(self):
        """clear env"""

    def test_query_media_info_english_name(self):
        """query media info with english name"""
        resp = self.client.get_mediainfo_of_file(self.sourceBucket, '10s.mp4')
        nose.tools.assert_is_not_none(resp)
    
    def test_query_media_info_object_contain_folder(self):
        """query media info with object contain folder"""
        resp = self.client.get_mediainfo_of_file(self.sourceBucket, '/media/info/jobtest.mp4')
        nose.tools.assert_is_not_none(resp)

    def test_query_media_info_object_chiness_name(self):
        """query media info with object chiness name"""
        resp = self.client.get_mediainfo_of_file(self.sourceBucket, '作业测试.mp3')
        nose.tools.assert_is_not_none(resp)

    def test_query_media_info_object_special_chars(self):
        """query media info with object chiness name"""
        resp = self.client.get_mediainfo_of_file(self.sourceBucket, 'job_测试_123.mp4')
        nose.tools.assert_is_not_none(resp)

    def test_query_media_info_object_not_exist(self):
        """query media info bucket not exist"""
        try:
            resp = self.client.get_mediainfo_of_file(self.sourceBucket, 'not_exist.mp4')
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('bos object: not_exist.mp4 does not exist')
            else:
                assert True == False, 'not throw BceServerError'

    def test_query_media_info_bucket_not_exist(self):
        """query media info bucket not exist"""
        try:
            resp = self.client.get_mediainfo_of_file('no-input', 'hd.mp4')
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        "Bucket no-input doesn't exist or isn't in bj region")
                #assert e.last_error.message.startswith('you have no access to bucket: no-input')
            else:
                assert True == False, 'not throw BceServerError'

    def test_query_media_info_bucket_is_empty(self):
        """query media info bucket is empty"""
        with nose.tools.assert_raises_regexp(BceClientError, 'bucket can\'t be empty string'):
            resp = self.client.get_mediainfo_of_file('', 'hd.mp4')

    def test_query_media_info_key_is_empty(self):
        """query media info key is empty"""
        with nose.tools.assert_raises_regexp(BceClientError, 'key can\'t be empty string'):
            resp = self.client.get_mediainfo_of_file(self.sourceBucket, '')

    def test_query_media_info_bucket_is_none(self):
        """query media info bucket not exist"""
        try:
            resp = self.client.get_mediainfo_of_file(None, 'hd.mp4')
        except ValueError as e:
            assert e.message.startswith('arg "bucket" should not be None')
