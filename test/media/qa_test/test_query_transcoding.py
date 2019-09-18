#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: test_query_transcoding.py
Date: 2015/07/2 11:09:40
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

class TestQueryTranscoding(mediaBase.MediaBase):
    """test create transcoding"""
    def __init__(self):
        """construction """
        mediaBase.MediaBase.__init__(self)
        self.pre = self.prefix + 'queryjob'
        self.pipeline_name = self.convertName(self.pre)
        self.preset_name = self.pipeline_name
        self.container = 'mp4'
        self.source_key = 'hd.mp4'
        self.target_key = 'job_test_result.mp4'
        self.watermark = 'watermark.jpg'
        self.capacity = 1
        self.job_id = None
        self.client = media_client.MediaClient(media_config.config)

    def setUp(self):
        """create env"""
        time.sleep(1)
        succ = True
        config = {'capacity': self.capacity}
        try:
            resp = self.client.create_pipeline(self.pipeline_name, self.sourceBucket,
                   self.targetBucket, pipeline_config=config)
        except Exception as e:
            print(e.message)
            succ = False
        finally:
            nose.tools.assert_true(succ)

        succ = True
        try:
            resp = self.client.create_preset(self.preset_name, self.container, True)
        except Exception as e:
            print(e.message)
            succ = False
        finally:
            nose.tools.assert_true(succ)

        succ = True
        try:
            source = {'sourceKey': self.source_key}
            target = {'targetKey': self.target_key, 'presetName': self.preset_name}
            resp = self.client.create_job(self.pipeline_name, source, target)
        except Exception as e:
            print(e.message)
            succ = False
        finally:
            nose.tools.assert_is_not_none(resp.job_id)
            self.job_id = resp.job_id

    def tearDown(self):
        """clear env"""
        #delete pipeline
        time.sleep(2)
        resp = self.client.list_pipelines()
        for each_pipeline in resp.pipelines:
            pipeline_name = each_pipeline.pipeline_name
            if (pipeline_name.startswith(self.pre)):
                resp = self.client.list_jobs(pipeline_name)
                if resp.jobs:
                    for each_job in resp.jobs:
                        while(1):
                            resp = self.client.get_job(each_job.job_id)
                            if resp.job_status != 'SUCCESS' and resp.job_status != 'FAILED':
                                print('please wait ....\n')
                                time.sleep(5)
                            else:
                                break
                resp = self.client.delete_pipeline(pipeline_name)

        #delete preset
        time.sleep(2)
        resp = self.client.list_presets()
        for each_preset in resp.presets:
            preset_name = each_preset.preset_name
            if (preset_name.startswith(self.pre)):
                resp = self.client.delete_preset(preset_name)
                nose.tools.assert_is_not_none(resp)

    def test_query_transcoding_normal_exist_job(self):
        """query exist transcoding job"""
        resp = self.client.get_job(self.job_id)
        nose.tools.assert_is_not_none(resp)
    
    def test_query_transcoding_with_not_exist_job(self):
        """query not exist transcoding job"""
        with nose.tools.assert_raises_regexp(BceHttpClientError, 
                'The requested job does not exist'):
            resp = self.client.get_job('query_not_exist_job')
    
    def test_query_transcoding_with_params_none(self):
        """query not exist transcoding job"""
        with nose.tools.assert_raises_regexp(ValueError, 
                'arg "job_id" should not be None'):
            resp = self.client.get_job(None)

    def test_query_transcoding_with_params_empty(self):
        """query not exist transcoding job"""
        with nose.tools.assert_raises_regexp(BceClientError, 
                'job_id can\'t be empty string'):
            resp = self.client.get_job('')
            print(resp) 
