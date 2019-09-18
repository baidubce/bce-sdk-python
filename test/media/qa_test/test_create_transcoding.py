#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: test_create_transcoding.py
Date: 2015/06/29 15:15:40
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

class TestCreateTranscoding(mediaBase.MediaBase):
    """test create transcoding"""
    def __init__(self):
        """construction """
        mediaBase.MediaBase.__init__(self)
        self.pre = self.prefix + 'createjob'
        self.pipeline_name = self.pre
        self.preset_name = 'bce.video_mp4_640x360_520kbps'
        self.container = 'mp4'
        self.source_key = '10s.mp4'
        self.target_key = 'job_test_result.mp4'
        self.watermark = '120X90.jpg'
        self.capacity = 1
        self.watermark_id = None
        self.client = media_client.MediaClient(media_config.config)

    def setUp(self):
        """create env"""
        time.sleep(2)
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
        time.sleep(2)
        try:
            resp = self.client.create_preset(self.preset_name, self.container, True)
        except Exception as e:
            print(e.message)
            succ = False
        finally:
            nose.tools.assert_true(succ)

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
                time.sleep(1)
                resp = self.client.delete_pipeline(pipeline_name)
        
        #delete preset
        time.sleep(2)
        resp = self.client.list_presets()
        for each_preset in resp.presets:
            preset_name = each_preset.preset_name
            if (preset_name.startswith(self.pre)):
                resp = self.client.delete_preset(preset_name)
                nose.tools.assert_is_not_none(resp)
        
        #delete watermark
        if self.watermark_id:
            resp = self.client.delete_watermark(self.watermark_id)
            nose.tools.assert_is_not_none(resp)

    def test_create_transcoding_normal(self):
        """create transcoding normal"""
        source = {'sourceKey': self.source_key}
        target = {'targetKey': self.target_key, 'presetName': self.preset_name}
        resp = self.client.create_job(self.pipeline_name, source, target)
        nose.tools.assert_is_not_none(resp.job_id)
    
    def test_create_transcoding_with_preset_ahls(self):
        """create job with containser a-hls """
        container = 'a-hls'
        self.preset_name = self.convertName(self.pre)
        ret = self.client.create_preset(self.preset_name, container, True)
        nose.tools.assert_is_not_none(ret)
        source = {'sourceKey': self.source_key}
        target = {'targetKey': self.target_key, 'presetName': self.preset_name}
        resp = self.client.create_job(self.pipeline_name, source, target)
        nose.tools.assert_is_not_none(resp.job_id)

    def test_create_transcoding_file_name_chinese(self):
        """create transcoding with file name is chinese"""
        source = {'sourceKey': '中文名称测试.mp4'}
        target = {'targetKey': '中文名称测试_结果.mp4', 'presetName': self.preset_name}
        resp = self.client.create_job(self.pipeline_name, source, target)
        nose.tools.assert_is_not_none(resp.job_id)

    def test_create_transcoding_file_name_spacial_chars(self):
        """create transcoding with file name has spacial chars"""
        source = {'sourceKey': 'test--*--中文.mp4'}
        target = {'targetKey': 'test--*--中文.mp4',
                  'presetName': self.preset_name}
        resp = self.client.create_job(self.pipeline_name, source, target)
        nose.tools.assert_is_not_none(resp.job_id)

    def test_create_transcoding_file_name_include_folder(self):
        """create transcoding with file name include folder"""
        source = {'sourceKey': 'media/info/jobtest.mp4'}
        target = {'targetKey': '测试视频结果/\<> *?"|.mp4',
                  'presetName': self.preset_name}
        resp = self.client.create_job(self.pipeline_name, source, target)
        nose.tools.assert_is_not_none(resp.job_id)

    def test_create_transcoding_file_name_too_long(self):
        """create transcoding with file name too long """
        source = {'sourceKey': 'longname12longname12longname12longname12longname12longname12.mp4'}
        target = {'targetKey': 'longname_测试视频结果.mp4',
                  'presetName': self.preset_name}
        resp = self.client.create_job(self.pipeline_name, source, target)
        nose.tools.assert_is_not_none(resp.job_id)

    def test_create_transcoding_pipeline_name_none(self):
        """create transcoding with pipeline name none """
        source = {'sourceKey': 'hd.mp4'}
        target = {'targetKey': 'test_result.mp4',
                  'presetName': self.preset_name}
        with nose.tools.assert_raises_regexp(ValueError, 
                'arg "pipeline_name" should not be None'):
            resp = self.client.create_job(None, source, target)

    def test_create_transcoding_pipeline_name_empty(self):
        """create transcoding with pipeline name empty """
        source = {'sourceKey': 'hd.mp4'}
        target = {'targetKey': 'test_result.mp4',
                  'presetName': self.preset_name}
        with nose.tools.assert_raises_regexp(BceClientError, 
                'pipeline_name can\'t be empty string'):
            resp = self.client.create_job('', source, target)

    def test_create_transcoding_pipeline_full(self):
        """create transcoding with pipeline capacity is full """
        source = {'sourceKey': 'hd.mp4'}
        target = {'targetKey': 'test_result.mp4',
                  'presetName': self.preset_name}
        resp = self.client.create_job(self.pipeline_name, source, target)
        nose.tools.assert_is_not_none(resp.job_id)
        with nose.tools.assert_raises_regexp(BceHttpClientError, 
                'BceServerError: pipeline is full'):
            resp = self.client.create_job(self.pipeline_name, source, target)

    def test_create_transcoding_file_not_exist(self):
        """create transcoding with file not exist"""
        source = {'sourceKey': 'job_test_not_exist_hd.mp4'}
        target = {'targetKey': 'test_result.mp4',
                  'presetName': self.preset_name}
        with nose.tools.assert_raises_regexp(BceHttpClientError, 
                'BceServerError: bos object: job_test_not_exist_hd.mp4 does not exist'):
            resp = self.client.create_job(self.pipeline_name, source, target)

    def test_create_transcoding_preset_not_exist(self):
        """create transcoding with preset not exist"""
        source = {'sourceKey': 'hd.mp4'}
        target = {'targetKey': 'test_result.mp4',
                  'presetName': 'not_exist_preset'}
        with nose.tools.assert_raises_regexp(BceHttpClientError, 
                'BceServerError: The requested preset does not exist'):
            resp = self.client.create_job(self.pipeline_name, source, target)

    def test_create_transcoding_pipeline_not_exist(self):
        """create transcoding with pipeline not exist"""
        source = {'sourceKey': 'hd.mp4'}
        target = {'targetKey': 'test_result.mp4',
                  'presetName': self.preset_name}
        with nose.tools.assert_raises_regexp(BceHttpClientError, 
                'BceServerError: The requested pipeline does not exist'):
            resp = self.client.create_job('not_exist_pipeline', source, target)

    def test_create_transcoding_pipeline_deleted(self):
        """create transcoding with pipeline deleted"""
        source = {'sourceKey': 'hd.mp4'}
        target = {'targetKey': 'test_result.mp4',
                  'presetName': self.preset_name}
        self.client.delete_pipeline(self.pipeline_name)
        with nose.tools.assert_raises_regexp(BceHttpClientError, 
                'BceServerError: pipeline has been deleted'):
            resp = self.client.create_job(self.pipeline_name, source, target)

    def test_create_transcoding_preset_deleted(self):
        """create transcoding with preset deleted"""
        source = {'sourceKey': 'hd.mp4'}
        target = {'targetKey': 'test_result.mp4',
                  'presetName': self.preset_name}
        self.client.delete_preset(self.preset_name)
        with nose.tools.assert_raises_regexp(BceHttpClientError, 
                'BceServerError: preset has been deleted'):
            resp = self.client.create_job(self.pipeline_name, source, target)

    def _test_create_transcoding_required_param_empty(self):
        """create transcoding with required param empty"""
        source = {'sourceKey': 'hd.mp4'}
        target = {'targetKey': 'test_result.mp4',
                  'presetName': self.preset_name}
        with nose.tools.assert_raises_regexp(BceHttpClientError, 
                'BceServerError: The requested pipeline does not exist'):
            resp = self.client.create_job('', source, target)

    def test_create_transcoding_watermark_normal(self):
        """create transcoding with watermark normal"""
        self.watermark_id = self.client.create_watermark(self.watermarkBucket, \
                'logo.gif').watermark_id
        nose.tools.assert_is_not_none(self.watermark_id)

        self.preset_name = self.convertName(self.pre)
        desc = 'this is a preset of testing watermark'
        clip = {'startTimeInSecond': 0, 'durationInSecond': 50}
        audio = {'bitRateInBps': 63000}
        video = {'bitRateInBps': 454000}
        resp = self.client.create_preset(self.preset_name, self.container, 
                False, clip=clip, description=desc, audio=audio, 
                video=video, watermark_id=self.watermark_id)

        source = {'sourceKey': 'hd.mp4'}
        target = {'targetKey': 'test_result.mp4',
                  'presetName': self.preset_name}
        resp = self.client.create_job(self.pipeline_name, source, target)

    def create_watermark_with_position(self, vAlignment, hAlignment, vOffset, hOffset, targetkey):
        """create watermark with position"""
        self.watermark_id = self.client.create_watermark(self.watermarkBucket, 
                'logo.gif', vAlignment, hAlignment, vOffset, hOffset).watermark_id
        nose.tools.assert_is_not_none(self.watermark_id)

        self.preset_name = self.convertName(self.pre)
        desc = 'this is a preset of testing watermark'
        clip = {'startTimeInSecond': 0, 'durationInSecond': 50}
        audio = {'bitRateInBps': 63000}
        video = {'bitRateInBps': 454000}
        resp = self.client.create_preset(self.preset_name, self.container, 
                False, clip=clip, description=desc, audio=audio, 
                video=video, watermark_id=self.watermark_id)

        source = {'sourceKey': 'hd.mp4'}
        target = {'targetKey': targetkey,
                  'presetName': self.preset_name}
        resp = self.client.create_job(self.pipeline_name, source, target)
        return resp
        
    def test_create_transcoding_with_watermark_lefttop_offset_0_0(self):
        """test watermark left top offset (0,0)"""
        resp = self.create_watermark_with_position('top', 'left', 0, 0, 'left_top_result_0_0.mp4')
        nose.tools.assert_is_not_none(resp.job_id)
