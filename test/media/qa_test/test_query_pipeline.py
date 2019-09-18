#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: test_query_pipeline.py
Date: 2015/06/12 13:34:00
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
from nose import tools
from nose.tools import assert_raises
from nose.tools import assert_is_none
from nose.tools import raises

class TestQueryPipeline(mediaBase.MediaBase):
    """test create pipeline"""
    def __init__(self):
        """construction """
        mediaBase.MediaBase.__init__(self)
        self.pre = self.prefix + 'querypipe'
        #self.pipeline_name = self.convertName(self.pre)
        self.pipeline_name = self.pre
        self.client = media_client.MediaClient(media_config.config)

    def setUp(self):
        """create env"""
        ret = self.client.create_pipeline(self.pipeline_name, self.sourceBucket, self.targetBucket)
        nose.tools.assert_is_not_none(ret)

    def tearDown(self):
        """clear env"""
        result = self.client.list_pipelines()
        for each_val in result.pipelines:
            pipeline_name = each_val.pipeline_name
            if(pipeline_name.startswith(self.pre)):
                resp = self.client.delete_pipeline(pipeline_name)
                nose.tools.assert_is_not_none(resp)

    def test_query_pipeline_exsit(self):
        """query exsit pipeline"""
        resp = self.client.get_pipeline(self.pipeline_name)
        nose.tools.assert_is_not_none(resp)
        nose.tools.assert_equal(resp.state, 'ACTIVE')
        nose.tools.assert_equal(resp.pipeline_name, self.pipeline_name)

    def test_query_pipeline_is_deleted(self):
        """query deleted pipeline"""
        resp = self.client.delete_pipeline(self.pipeline_name)
        nose.tools.assert_is_not_none(resp)
        resp = self.client.get_pipeline(self.pipeline_name)
        nose.tools.assert_equal(resp.state, 'INACTIVE')
    
    def test_query_pipeline_is_name_empty(self):
        """pipeline name is empty"""
        with nose.tools.assert_raises_regexp(BceClientError, 
                'pipeline_name can\'t be empty string'):
            resp = self.client.get_pipeline('')
    
    def test_query_pipeline_is_name_none(self):
        """pipeline name is  none"""
        with nose.tools.assert_raises_regexp(ValueError, 
                'arg "pipeline_name" should not be None'):
            self.client.get_pipeline(None)

    def test_query_pipeline_not_exist(self):
        """pipeline name is not exist"""
        pipeline_name = 'not_exist_pipeline'
        try:
            self.client.get_pipeline(pipeline_name)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('The requested pipeline does not exist')
            else:
                assert True == False
