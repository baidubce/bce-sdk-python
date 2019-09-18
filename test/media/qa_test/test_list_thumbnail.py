#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: test_list_thumbnail.py
Date: 2015/06/25 15:38:40
"""
import os
import sys
import unittest
import json
import time
import datetime
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

class TestListThumbnail(mediaBase.MediaBase):
    """test create thumbnail"""
    def __init__(self):
        """construction """
        mediaBase.MediaBase.__init__(self)
        self.pre = self.prefix + 'listthumb'
        self.pipeline_name = self.pre
        self.key = '10s.mp4'
        self.client = media_client.MediaClient(media_config.config)

    def setUp(self):
        """create env"""
        time.sleep(1)
        succ = True
        try:
            resp = self.client.create_pipeline(self.pipeline_name, self.sourceBucket,
                   self.targetBucket)
        except Exception as e:
            print(e.message)
            succ = False
        finally:
            nose.tools.assert_true(succ)

    def tearDown(self):
        """clear env"""
        time.sleep(2)
        resp = self.client.list_pipelines()
        for each_pipeline in resp.pipelines:
            pipeline_name = each_pipeline.pipeline_name
            if (pipeline_name.startswith(self.pre)):
                resp = self.client.list_thumbnail_jobs_by_pipeline(pipeline_name)
                if resp.thumbnails:
                    for each_job in resp.thumbnails:
                        while(1):
                            resp = self.client.get_thumbnail_job(each_job.job_id)
                            if resp.job_status != 'SUCCESS' and resp.job_status != 'FAILED':
                                print('please wait ....\n')
                                time.sleep(5)
                            else:
                                break
                time.sleep(1)
                resp = self.client.delete_pipeline(pipeline_name)
    
    def test_list_thumbnail_job_with_pipeline(self):
        """list thumbnail job with pipelie """
        source = {'key': self.key}
        resp = self.client.list_thumbnail_jobs_by_pipeline(self.pipeline_name)
        before_len = len(resp.thumbnails)

        resp = self.client.create_thumbnail_job(self.pipeline_name, source)
        nose.tools.assert_is_not_none(resp.job_id)

        resp = self.client.list_thumbnail_jobs_by_pipeline(self.pipeline_name)
        after_len = len(resp.thumbnails)
        
        nose.tools.assert_equal(before_len + 1, after_len)
    
    def test_list_thumbnail_job_with_pipeline_status(self):
        """list thumbnail job with pipelie """
        source = {'key': self.key}
        resp = self.client.create_thumbnail_job(self.pipeline_name, source)
        nose.tools.assert_is_not_none(resp.job_id)
        job_id = resp.job_id
        
        resp = self.client.list_thumbnail_jobs_by_pipeline(self.pipeline_name, 
                end='2015-11-11T08:53:42Z')
        length1 = len(resp.thumbnails)
        nose.tools.assert_equal(length1, 0)
        
        resp = self.client.list_thumbnail_jobs_by_pipeline(self.pipeline_name, 
                begin='2015-11-11T08:53:42Z')
        length2 = len(resp.thumbnails)
        nose.tools.assert_greater_equal(length2, 1)
        
        while(1):
            resp = self.client.get_thumbnail_job(job_id)
            if resp.job_status != 'SUCCESS':
                print('please wait ....\n')
                time.sleep(5)
            else:
                break
        resp = self.client.list_thumbnail_jobs_by_pipeline(self.pipeline_name, 'SUCCESS')
        length3 = len(resp.thumbnails)
        nose.tools.assert_equal(length3, 1)
         
        resp = self.client.list_thumbnail_jobs_by_pipeline(self.pipeline_name, 'SUCCESS', 
                '2015-11-11T08:53:42Z', '2015-11-11T08:53:42Z')
        length4 = len(resp.thumbnails)
        nose.tools.assert_equal(length4, 0)
        
        resp = self.client.list_thumbnail_jobs_by_pipeline(self.pipeline_name, 'SUCCESS', 
                '2015-11-11T08:53:42Z', datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        length5 = len(resp.thumbnails)
        nose.tools.assert_equal(length5, 1)

    def test_list_thumbnail_job_with_pipeline_not_exist(self):
        """list thumbnail job with pipeline not exist"""
        try:
            resp_query = self.client.list_thumbnail_jobs_by_pipeline('not_exist_pipeline')
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('The requested pipeline does not exist')
            else:
                assert True == False, 'not throw BceServerError'

    def test_list_thumbnail_job_pipeline_name_none(self):
        """list thumbnail job name none"""
        try:
            resp_query = self.client.list_thumbnail_jobs_by_pipeline(None)
        except ValueError as e:
            assert e.message.startswith('arg "pipeline_name" should not be None')

    def test_list_thumbnail_job_pipeline_name_empty(self):
        """query thumbnail job name empty"""
        with nose.tools.assert_raises_regexp(BceClientError, 
                'pipeline_name can\'t be empty string'):
            resp_query = self.client.list_thumbnail_jobs_by_pipeline('')
