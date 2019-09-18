#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: test_delete_pipeline.py
Date: 2015/06/12 15:57:40
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

class TestDeletePipeline(mediaBase.MediaBase):
    """test delete pipeline"""
    def __init__(self):
        """construction """
        mediaBase.MediaBase.__init__(self)
        self.pre = self.prefix + 'deletepipe'
        self.pipeline_name = self.pre
        self.client = media_client.MediaClient(media_config.config)

    def setUp(self):
        """create env"""
        time.sleep(1)
        ret = self.client.create_pipeline(self.pipeline_name, self.sourceBucket, self.targetBucket)
        nose.tools.assert_is_not_none(ret)

    def tearDown(self):
        """clear env"""
        time.sleep(1)
        result = self.client.list_pipelines()
        for each_val in result.pipelines:
            pipeline_name = each_val.pipeline_name
            if(pipeline_name.startswith(self.pre)):
                resp = self.client.delete_pipeline(pipeline_name)
                nose.tools.assert_is_not_none(resp)
    
    def test_delete_pipeline_exist(self):
        """delete exist pipeline"""
        ret = self.client.delete_pipeline(self.pipeline_name)
        nose.tools.assert_is_not_none(ret)
    
    def test_delete_pipeline_not_exist(self):
        """delete not exist pipeline"""
        pipeline_name = 'pipeline_name_not_exist'
        try:
            self.client.delete_pipeline(pipeline_name)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('The requested pipeline does not exist')
            else:
                assert True == False, 'not throw bceservererror'

    def test_delete_pipeline_repeated(self):
        """delete pipeline repeated"""
        ret = self.client.delete_pipeline(self.pipeline_name)
        nose.tools.assert_is_not_none(ret)
        with nose.tools.assert_raises_regexp(BceHttpClientError, 
                'BceServerError: The requested pipeline does not exist'):
            ret = self.client.delete_pipeline(self.pipeline_name)

    def test_delete_pipeline_with_name_is_empty(self):
        """delete pipeline with name is empty"""
        pipeline_name = ''
        with nose.tools.assert_raises_regexp(BceClientError, 
                'pipeline_name can\'t be empty string'):
            self.client.delete_pipeline(pipeline_name)

    def test_delete_pipeline_with_name_is_none(self):
        """delete pipeline with name is none"""
        with nose.tools.assert_raises_regexp(ValueError,
                'arg "pipeline_name" should not be None'):
            self.client.delete_pipeline(None)
