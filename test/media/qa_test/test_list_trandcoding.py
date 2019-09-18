#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: test_list_transcoding.py
Date: 2015/07/2 14:09:40
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

class TestListTranscoding(mediaBase.MediaBase):
    """test list transcoding"""
    def __init__(self):
        """construction """
        mediaBase.MediaBase.__init__(self)
        self.pre = self.prefix + 'listjob'
        self.pipeline_name = self.pre
        self.preset_name = self.pipeline_name
        self.container = 'mp4'
        self.source_key = 'hd.mp4'
        self.target_key = 'job_test_result.mp4'
        self.capacity = 1
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

        try:
            resp = self.client.create_preset(self.preset_name, self.container, True)
        except Exception as e:
            print(e.message)
            succ = False
        finally:
            nose.tools.assert_true(succ)

        try:
            source = {'sourceKey': self.source_key}
            target = {'targetKey': self.target_key, 'presetName': self.preset_name}
            resp = self.client.create_job(self.pipeline_name, source, target)
        except Exception as e:
            print(e.message)
            succ = False
        finally:
            pass
#            nose.tools.assert_is_not_none(resp.job_id)
#            self.job_id = resp.job_id

    def tearDown(self):
        """clear env"""
        #delete pipeline
        time.sleep(1)
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
        resp = self.client.list_presets()
        for each_preset in resp.presets:
            preset_name = each_preset.preset_name
            if (preset_name.startswith(self.pre)):
                resp = self.client.delete_preset(preset_name)
                nose.tools.assert_is_not_none(resp)

    def test_list_transcoding_job_with_pipeline(self):
        """list transcoding job with pipeline"""
        resp = self.client.list_jobs(self.pipeline_name)
        nose.tools.assert_is_not_none(resp)
        assert len(resp.jobs) == self.capacity

    def test_list_transcoding_job_with_pipeline_none(self):
        """list transcoding job with pipeline name none"""
        with nose.tools.assert_raises_regexp(ValueError, 
                'arg "pipeline_name" should not be None'):
            resp = self.client.list_jobs(None)

    def test_list_transcoding_job_with_pipeline_empty(self):
        """list transcoding job with pipeline name empty"""
        with nose.tools.assert_raises_regexp(BceClientError, 
                'pipeline_name can\'t be empty string'):
            resp = self.client.list_jobs('')
    
    def test_list_transcoding_job_with_pipeline_jobstatus(self):
        """list transcoding job with pipelineName and jobStatus"""
        resp = self.client.list_jobs(self.pipeline_name, 'PENDING')
        nose.tools.assert_is_not_none(resp)
        assert len(resp.jobs) == self.capacity
        time.sleep(1) 
        resp = self.client.list_jobs(self.pipeline_name, 
                begin=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        nose.tools.assert_is_not_none(resp)
        assert len(resp.jobs) == 0

        resp = self.client.list_jobs(self.pipeline_name, 
                end=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        nose.tools.assert_is_not_none(resp)
        assert len(resp.jobs) == 1
