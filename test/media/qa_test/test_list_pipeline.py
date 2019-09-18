#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: test_list_pipeline.py
Date: 2015/06/12 13:01:00
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

class TestListPipeline(mediaBase.MediaBase):
    """test list pipeline"""
    def __init__(self):
        """construction """
        mediaBase.MediaBase.__init__(self)
        self.pre = self.prefix + 'listpipe'
        self.pipeline_name = self.pre
        self.client = media_client.MediaClient(media_config.config)

    def setUp(self):
        """create env"""
        ret = self.client.create_pipeline(self.pipeline_name, self.sourceBucket, self.targetBucket)
        nose.tools.assert_is_not_none(ret)

    def tearDown(self):
        """clear env"""
        time.sleep(2)
        result = self.client.list_pipelines()
        for each_val in result.pipelines:
            pipeline_name = each_val.pipeline_name
            if(pipeline_name.startswith(self.pre)):
                resp = self.client.delete_pipeline(pipeline_name)
                nose.tools.assert_is_not_none(resp)

    def test_list_pipeline_add_one(self):
        """list pipeline with add one"""
        response = self.client.list_pipelines()
        exsit = False
        for pipeline in response.pipelines:
            if pipeline.pipeline_name == self.pipeline_name:
                exsit = True
                break
        nose.tools.assert_true(exsit)

    def test_list_pipeline_delete_one(self):
        """list pipeline with delete one"""
        response = self.client.delete_pipeline(self.pipeline_name)
        nose.tools.assert_is_not_none(response)

        response = self.client.list_pipelines()
        exsit = False
        for pipeline in response.pipelines:
            if pipeline.pipeline_name == self.pipeline_name:
                exsit = True
                break
        nose.tools.assert_false(exsit)
