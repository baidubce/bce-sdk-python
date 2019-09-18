#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: test_create_pipeline.py
Date: 2015/06/10 15:15:40
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
from nose.tools import raises

class TestCreatePipeline(mediaBase.MediaBase):
    """test create pipeline"""
    def __init__(self):
        """construction """
        mediaBase.MediaBase.__init__(self)
        self.pre = self.prefix + 'createpipe'
        self.pipeline_name = self.convertName(self.pre)
        self.client = media_client.MediaClient(media_config.config)

    def setUp(self):
        """create env"""
        time.sleep(2)

    def tearDown(self):
        """clear env"""
        time.sleep(2)
        result = self.client.list_pipelines()
        for each_val in result.pipelines:
            pipeline_name = each_val.pipeline_name
            if(pipeline_name.startswith(self.pre)):
                resp = self.client.delete_pipeline(pipeline_name)
    
    def test_create_pipeline_normal(self):
        """create pipeline normal"""
        desc = "it's a test pipeline!!!"
        capacity = {'capacity': 1}
        ret = self.client.create_pipeline(self.pipeline_name, self.sourceBucket, 
                   self.targetBucket, description=desc, pipeline_config=capacity)
        nose.tools.assert_is_not_none(ret)
    
    def test_create_pipeline_with_name_none(self):
        """create pipeline with pipeline name is none"""
        desc = "it's a test pipeline!!!"
        capacity = {'capacity': 1}
        try:
            resp = self.client.create_pipeline(None, self.sourceBucket, 
                   self.targetBucket, description=desc, pipeline_config=capacity)
        except ValueError as e:
            assert e.message.startswith('arg "pipeline_name" should not be None')

    def test_create_pipeline_with_name_empty(self):
        """create pipeline with pipeline name is empty"""
        desc = "it's a test pipeline!!!"
        capacity = {'capacity': 1}
        with nose.tools.assert_raises_regexp(BceClientError, 
                "pipeline_name can't be empty string"):
            resp = self.client.create_pipeline('', self.sourceBucket, 
                   self.targetBucket, description=desc, pipeline_config=capacity)

    def test_create_pipeline_capacityIs100(self):
        """all params are normal,sum(capacity) is 100"""
        capacity = {'capacity': 101}
        pipeline_name = self.convertName(self.pre)
        used = 0
        try:
            ret = self.client.create_pipeline(pipeline_name, 
                    self.sourceBucket, self.targetBucket, pipeline_config=capacity)
        except BceHttpClientError as e:
            msg = e.last_error.message
            print(msg)
            used = msg.split(':')[2]
            print(used)

        pipeline_name = self.convertName(self.pre)
        capacity = {'capacity': 100 - int(used)}
        ret = self.client.create_pipeline(pipeline_name, self.sourceBucket, 
                    self.targetBucket, pipeline_config=capacity)
        nose.tools.assert_is_not_none(ret)

    def test_create_pipeline_capacityIs_more100(self):
        """all params are normal,sum(capacity) is more than 100"""
        err = None
        capacity1 = {'capacity': 41}
        capacity2 = {'capacity': 60}
        pipeline_name1 = self.convertName(self.pre)
        time.sleep(1)
        pipeline_name2 = self.convertName(self.pre)
        with nose.tools.assert_raises_regexp(BceHttpClientError, 
                'BceServerError: total pipeline size exceed free quota:100, current used:41'):
            ret = self.client.create_pipeline(pipeline_name1, self.sourceBucket, 
                    self.targetBucket, pipeline_config=capacity1)
            ret = self.client.create_pipeline(pipeline_name2, self.sourceBucket, 
                    self.targetBucket, pipeline_config=capacity2)

    def test_create_pipeline_desc_include_chinese(self):
        """all param are normal,desc include chinese"""
        desc = "It's time to create pipeline for DescIncludeChinese.描述包含中文."
        ret = self.client.create_pipeline(self.pipeline_name, self.sourceBucket, 
                   self.targetBucket, description=desc)
        nose.tools.assert_is_not_none(ret)

    def test_create_pipeline_all_required_params(self):
        """all required params"""
        ret = self.client.create_pipeline(self.pipeline_name, self.sourceBucket, 
                   self.targetBucket)
        nose.tools.assert_is_not_none(ret)

    def test_create_pipeline_capacity_float(self):
        """capacity isn't int, float to int"""
        capacity = {'capacity': 3.5}
        ret = self.client.create_pipeline(self.pipeline_name, self.sourceBucket, 
                   self.targetBucket, pipeline_config=capacity)
        nose.tools.assert_is_not_none(ret)

    def test_create_pipeline_required_param_null(self):
        """required params is null"""
        self.sourceBucket = None
        with nose.tools.assert_raises_regexp(ValueError, 
                'arg "source_bucket" should not be None'):
            self.client.create_pipeline(self.pipeline_name, 
                   self.sourceBucket, self.targetBucket)
    
    def test_create_pipeline_required_param_empty(self):
        """required param is "" """
        self.sourceBucket = ''
        with nose.tools.assert_raises_regexp(BceClientError, 
                "source_bucket can't be empty string"):
            self.client.create_pipeline(self.pipeline_name, self.sourceBucket, self.targetBucket)
    
    def test_create_pipeline_bucket_without_permission(self):
        """create pipeline with bucket not exsit"""
        sourceBucket = 'sdk-input-' + str(int(time.time()))
        targetBucket = 'sdk-output-' + str(int(time.time()))
        try:
            ret = self.client.create_pipeline(self.pipeline_name, sourceBucket, targetBucket)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        "Bucket " + sourceBucket + " doesn't exist or isn't in bj region")
    
    def test_create_pipeline_duplicName(self):
        """create pipeline duplication name"""
        ret = self.client.create_pipeline(self.pipeline_name, self.sourceBucket, self.targetBucket)
        nose.tools.assert_is_not_none(ret)
        try:
            ret = self.client.create_pipeline(self.pipeline_name, 
                    self.sourceBucket, self.targetBucket)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('duplicated pipeline name')

    def test_create_pipeline_name_is_chinese(self):
        """pipeline name is chinese  """
        self.pipeline_name = '创建中文队列'
        with nose.tools.assert_raises_regexp(BceHttpClientError, 
                'BceServerError: pipelineName:pipelineName=must match'):
            self.client.create_pipeline(self.pipeline_name, self.sourceBucket, self.targetBucket)

    def test_create_pipeline_name_is_upercase(self):
        """pipeline name is upercase  """
        self.pipeline_name = 'CREATEPIPELINE'
        try:
            self.client.create_pipeline(self.pipeline_name, self.sourceBucket, self.targetBucket)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('pipelineName:pipelineName=must match')

    def test_create_pipeline_name_is_number(self):
        """pipeline name is number  """
        self.pipeline_name = '123456'
        try:
            self.client.create_pipeline(self.pipeline_name, self.sourceBucket, self.targetBucket)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('pipelineName:pipelineName=must match')

    def test_create_pipeline_name_not_start_with_letter(self):
        """pipeline name not start with letter  """
        self.pipeline_name = '_createpipeline1234'
        try:
            self.client.create_pipeline(self.pipeline_name, self.sourceBucket, self.targetBucket)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('pipelineName:pipelineName=must match')

    def test_create_pipeline_name_include_midline(self):
        """pipeline name include midline  """
        self.pipeline_name = 'createpipeline-1234'
        try:
            self.client.create_pipeline(self.pipeline_name, self.sourceBucket, self.targetBucket)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('pipelineName:pipelineName=must match')
    
    def test_create_pipeline_name_include_space(self):
        """pipeline name include space"""
        self.pipeline_name = 'createpipeline 1234'
        try:
            self.client.create_pipeline(self.pipeline_name, self.sourceBucket, self.targetBucket)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('pipelineName:pipelineName=must match')

    def test_create_pipeline_name_longer_than_40(self):
        """pipeline name longer than 40 chars"""
        self.pipeline_name = self.pipeline_name + '012'
        print(len(self.pipeline_name))
        assert len(self.pipeline_name) == 41, 'pipelineName length is not 41'
        try:
            self.client.create_pipeline(self.pipeline_name, self.sourceBucket, self.targetBucket)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('pipelineName:pipelineName=must match')

    def test_create_pipeline_capacity_larger_than_100(self):
        """pipeline capacity larger than 100"""
        capacity = {'capacity': 101}
        try:
            self.client.create_pipeline(self.pipeline_name, self.sourceBucket, self.targetBucket,\
                pipeline_config=capacity)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('total pipeline size exceed free quota:100')
            
    def test_create_pipeline_capacity_equal_0(self):
        """pipeline capacity equal 0"""
        capacity = {'capacity': 0}
        try:
            self.client.create_pipeline(self.pipeline_name, self.sourceBucket, self.targetBucket,\
                pipeline_config=capacity)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'config.capacity:config.capacity=must be greater than or equal to 1')

    def test_create_pipeline_capacity_less_than_0(self):
        """pipeline capacity less than 0"""
        capacity = {'capacity': -1}
        try:
            self.client.create_pipeline(self.pipeline_name, self.sourceBucket, self.targetBucket,
                pipeline_config=capacity)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'config.capacity:config.capacity=must be greater than or equal to 1')

    def test_create_pipeline_capacity_not_int(self):
        """pipeline capacity not int  ==>(3.5 == 3)"""
        capacity = {'capacity': 3.5}
        ret = self.client.create_pipeline(self.pipeline_name, self.sourceBucket, self.targetBucket,
                pipeline_config=capacity)
        nose.tools.assert_is_not_none(ret)

    def test_create_pipeline_desc_longer_than_128(self):
        """pipeline capacity less than 0"""
        desc = 'It is time to create pipeline for DescLongerThen128.\
               It is time to create pipeline for DescLongerThen128.0123456798765432100123456789.'
        try:
            self.client.create_pipeline(self.pipeline_name, self.sourceBucket, self.targetBucket,\
                description=desc)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'description:description=size must be between 0 and 128')


