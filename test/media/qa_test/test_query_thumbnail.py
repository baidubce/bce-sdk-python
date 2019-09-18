#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: test_query_thumbnail.py
Date: 2015/06/25 15:15:40
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

class TestQueryThumbnail(mediaBase.MediaBase):
    """test create thumbnail"""
    def __init__(self):
        """construction """
        mediaBase.MediaBase.__init__(self)
        self.pre = self.prefix + 'querythumb'
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
        time.sleep(1)
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
                resp = self.client.delete_pipeline(pipeline_name)
    
    def test_query_thumbnail_job_exist(self):
        """query thumbnail with job exist"""
        source = {'key': self.key}
        resp = self.client.create_thumbnail_job(self.pipeline_name, source)
        nose.tools.assert_is_not_none(resp.job_id)
        job_id = ''
        if self.PY3:
            job_id = resp.job_id
        else:
            job_id = resp.job_id.encode(encoding='UTF-8')

        resp_query = self.client.get_thumbnail_job(job_id)
        nose.tools.assert_equal(job_id, resp_query.job_id)
    
    def test_query_thumbnail_job_not_exist(self):
        """query thumbnail job not exist"""
        try:
            resp_query = self.client.get_thumbnail_job('not_exist_job')
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                print(e.last_error.message)
                assert e.last_error.message.startswith('The requested thumbnail does not exist')
            else:
                assert True == False, 'not throw BceServerError'

    def test_query_thumbnail_job_name_none(self):
        """query thumbnail job name none"""
        try:
            resp_query = self.client.get_thumbnail_job(None)
        except ValueError as e:
            assert e.message.startswith('arg "job_id" should not be None')

    def test_query_thumbnail_job_name_empty(self):
        """query thumbnail job name empty"""
        with nose.tools.assert_raises_regexp(BceClientError, 
                'job_id can\'t be empty string'):
            resp_query = self.client.get_thumbnail_job('')
