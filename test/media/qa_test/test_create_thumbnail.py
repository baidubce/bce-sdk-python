#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: test_create_thumbnail.py
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
from nose.tools import assert_raises
from nose.tools import assert_is_none
from nose.tools import raises

class TestCreateThumbnail(mediaBase.MediaBase):
    """test create thumbnail"""
    def __init__(self):
        """construction """
        mediaBase.MediaBase.__init__(self)
        self.pre = self.prefix + 'createthumb'
        self.pipeline_name = self.pre
        self.container = 'mp4'
        self.capacity = 1
        self.key = '10s.mp4'
        self.key_prefix = '/00mingxioutput'
        self.target_format = 'jpg'
        self.sizing_policy = 'keep'
        self.width_in_pixel = 640
        self.height_in_pixel = 400
        self.mode = 'manual'
        self.start_time_in_second = 0
        self.end_time_in_second = 50
        self.interval_in_second = 10
        self.client = media_client.MediaClient(media_config.config)

    def setUp(self):
        """create env"""
        time.sleep(2)
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
                resp = self.client.delete_pipeline(pipeline_name)
    
    def test_create_thumbnail_normal(self):
        """create thumbnail normal"""
        source = {'key': self.key}
        target = {'keyPrefix': self.key_prefix,
                  'format': self.target_format,
                  'sizingPolicy': self.sizing_policy,
                  'widthInPixel': self.width_in_pixel,
                  'heightInPixel': self.height_in_pixel,
                 }
        capture = {'mode': self.mode,
                    'startTimeInSecond': self.start_time_in_second,
                    'endTimeInSecond': self.end_time_in_second,
                    'intervalInSecond': self.interval_in_second
                  }
        resp = self.client.create_thumbnail_job(self.pipeline_name, source, target, capture)
        nose.tools.assert_is_not_none(resp.job_id)
    
    def test_create_thumbnail_with_pipeline_deleted(self):
        """create thumbnail with delete pipeline"""
        resp = self.client.delete_pipeline(self.pipeline_name)
        nose.tools.assert_is_not_none(resp)
        source = {'key': self.key} 
        try:
            self.client.create_thumbnail_job(self.pipeline_name, source)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('pipeline has been deleted')
            else:
                assert True == False, 'not throw BceServerError'

    def test_create_thumbnail_with_pipeline_not_exist(self):
        """create thumbnail with pipeline not exist"""
        source = {'key': self.key} 
        try:
            self.client.create_thumbnail_job('not_exist_pipeline', source)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('The requested pipeline does not exist')
            else:
                assert True == False, 'not throw BceServerError'
    
    def test_create_thumbnail_with_pipeline_none(self):
        """create thumbnail with pipeline none"""
        source = {'key': self.key} 
        try:
            self.client.create_thumbnail_job(None, source)
        except ValueError as e:
            assert e.message.startswith('arg "pipeline_name" should not be None')

    def test_create_thumbnail_with_pipeline_empty(self):
        """create thumbnail with pipeline empty"""
        source = {'key': self.key}
        with nose.tools.assert_raises_regexp(BceClientError, 
                'pipeline_name can\'t be empty string'):
            self.client.create_thumbnail_job('', source)
    
    def test_create_thumbnail_with_key_is_chiness(self):
        """create thumbnail job with key is chiness"""
        self.key = 'test--*--中文.mp4'
        source = {'key': self.key}
        resp = self.client.create_thumbnail_job(self.pipeline_name, source)
        nose.tools.assert_is_not_none(resp)

    def test_create_thumbnail_with_key_is_multiple_chars(self):
        """create thumbnail job with key is multiple chars"""
        self.key = 'job_测试_123.mp4'
        source = {'key': self.key}
        resp = self.client.create_thumbnail_job(self.pipeline_name, source)
        nose.tools.assert_is_not_none(resp)

    def test_create_thumbnail_with_key_not_exist(self):
        """create thumbnail with key not exist"""
        source = {'key': 'not_exist.mp4'} 
        try:
            self.client.create_thumbnail_job(self.pipeline_name, source)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('bos object: not_exist.mp4 does not exist')
            else:
                assert True == False, 'not throw BceServerError'

    def test_create_thumbnail_with_key_include_folder(self):
        """create thumbnail with key include folder"""
        source = {'key': 'media/info/jobtest.mp4'} 
        resp = self.client.create_thumbnail_job(self.pipeline_name, source)
        nose.tools.assert_is_not_none(resp)

    def test_create_thumbnail_with_key_long_name(self):
        """create thumbnail with key long name"""
        source = {'key': 'longname12longname12longname12longname12longname12longname12.mp4'} 
        resp = self.client.create_thumbnail_job(self.pipeline_name, source)
        nose.tools.assert_is_not_none(resp)

    def test_create_thumbnail_keyprefix_none(self):
        """create thumbnail with key prefix is none"""
        source = {'key': self.key}
        resp = self.client.create_thumbnail_job(self.pipeline_name, source)
        nose.tools.assert_is_not_none(resp.job_id)

    def test_create_thumbnail_keyprefix_keydot(self):
        """create thumbnail with key prefix key dot"""
        source = {'key': 'test.thumbnail.csdn.mp4'}
        resp = self.client.create_thumbnail_job(self.pipeline_name, source)
        nose.tools.assert_is_not_none(resp.job_id)

    def test_create_thumbnail_format_png(self):
        """create thumbnail with png pic"""
        source = {'key': self.key}
        target = {'keyPrefix': self.key_prefix,
                  'format': 'png',
                  'sizingPolicy': self.sizing_policy,
                  'widthInPixel': self.width_in_pixel,
                  'heightInPixel': self.height_in_pixel,
                 }
        resp = self.client.create_thumbnail_job(self.pipeline_name, source, target)
        nose.tools.assert_is_not_none(resp.job_id)

    def test_create_thumbnail_format_not_in_enum(self):
        """create thumbnail format not in enum"""
        source = {'key': self.key}
        target = {'keyPrefix': self.key_prefix,
                  'format': 'txt',
                  'sizingPolicy': self.sizing_policy,
                  'widthInPixel': self.width_in_pixel,
                  'heightInPixel': self.height_in_pixel,
                 }
        try: 
            resp = self.client.create_thumbnail_job(self.pipeline_name, source, target)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('Could not read JSON: Can not construct')
            else:
                assert True == False

    def test_create_thumbnail_sizingpolicy_in_enum(self):
        """create thumbnail with png pic"""
        source = {'key': self.key}
        target = {'keyPrefix': self.key_prefix,
                  'format': 'png',
                  'sizingPolicy': 'shrinkToFit',
                  'widthInPixel': self.width_in_pixel,
                  'heightInPixel': self.height_in_pixel,
                 }
        resp = self.client.create_thumbnail_job(self.pipeline_name, source, target)
        nose.tools.assert_is_not_none(resp.job_id)

    def test_create_thumbnail_sizingpolicy_not_in_enum(self):
        """create thumbnail format not in enum"""
        source = {'key': self.key}
        target = {'keyPrefix': self.key_prefix,
                  'format': 'png',
                  'sizingPolicy': 'notsizing',
                  'widthInPixel': self.width_in_pixel,
                  'heightInPixel': self.height_in_pixel,
                 }
        try: 
            resp = self.client.create_thumbnail_job(self.pipeline_name, source, target)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('Could not read JSON: Can not construct')
            else:
                assert True == False

    def test_create_thumbnail_widthinpixel_equal_2000(self):
        """create thumbnail with width pixel equal 2000"""
        source = {'key': self.key}
        target = {'keyPrefix': self.key_prefix,
                  'format': 'png',
                  'sizingPolicy': 'shrinkToFit',
                  'widthInPixel': 2000,
                  'heightInPixel': self.height_in_pixel,
                 }
        resp = self.client.create_thumbnail_job(self.pipeline_name, source, target)
        nose.tools.assert_is_not_none(resp.job_id)

    def test_create_thumbnail_widthinpixel_lessthan_10(self):
        """create thumbnail with width pixel less than 10"""
        source = {'key': self.key}
        target = {'keyPrefix': self.key_prefix,
                  'format': 'png',
                  'sizingPolicy': 'shrinkToFit',
                  'widthInPixel': 5,
                  'heightInPixel': self.height_in_pixel,
                 }
        try: 
            resp = self.client.create_thumbnail_job(self.pipeline_name, source, target)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('target.widthInPixel:target.widthInPixel=')
            else:
                assert True == False

    def test_create_thumbnail_widthinpixel_morethan_2000(self):
        """create thumbnail with width pixel more than 2000"""
        source = {'key': self.key}
        target = {'keyPrefix': self.key_prefix,
                  'format': 'png',
                  'sizingPolicy': 'shrinkToFit',
                  'widthInPixel': 2001,
                  'heightInPixel': self.height_in_pixel,
                 }
        try: 
            resp = self.client.create_thumbnail_job(self.pipeline_name, source, target)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('target.widthInPixel:target.widthInPixel=')
            else:
                assert True == False

    def test_create_thumbnail_heightinpixel_equal_2000(self):
        """create thumbnail withheight pixel equal 2000"""
        source = {'key': self.key}
        target = {'keyPrefix': self.key_prefix,
                  'format': 'png',
                  'sizingPolicy': 'shrinkToFit',
                  'widthInPixel': self.width_in_pixel,
                  'heightInPixel': 2000,
                 }
        resp = self.client.create_thumbnail_job(self.pipeline_name, source, target)
        nose.tools.assert_is_not_none(resp.job_id)

    def test_create_thumbnail_heightinpixel_lessthan_10(self):
        """create thumbnail with height pixel less than 10"""
        source = {'key': self.key}
        target = {'keyPrefix': self.key_prefix,
                  'format': 'png',
                  'sizingPolicy': 'shrinkToFit',
                  'widthInPixel': self.width_in_pixel,
                  'heightInPixel': 5,
                 }
        try: 
            resp = self.client.create_thumbnail_job(self.pipeline_name, source, target)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('target.heightInPixel:target.heightInPixel=')
            else:
                assert True == False

    def test_create_thumbnail_heightinpixel_morethan_2000(self):
        """create thumbnail with height pixel more than 2000"""
        source = {'key': self.key}
        target = {'keyPrefix': self.key_prefix,
                  'format': 'png',
                  'sizingPolicy': 'shrinkToFit',
                  'widthInPixel': self.width_in_pixel,
                  'heightInPixel': 2001,
                 }
        try: 
            resp = self.client.create_thumbnail_job(self.pipeline_name, source, target)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('target.heightInPixel:target.heightInPixel=')
            else:
                assert True == False

    def test_create_thumbnail_mode_is_auto(self):
        """create thumbnail with mode is auto"""
        source = {'key': self.key}
        capture = {'mode': 'auto'}
        resp = self.client.create_thumbnail_job(self.pipeline_name, source, capture=capture)
        nose.tools.assert_is_not_none(resp.job_id)

    def test_create_thumbnail_mode_not_in_enum(self):
        """create thumbnail with mode not in enum"""
        source = {'key': self.key}
        capture = {'mode': 'notmode'}
        try: 
            resp = self.client.create_thumbnail_job(self.pipeline_name, source, capture=capture)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('Could not read JSON: Can not')
            else:
                assert True == False

    def test_create_thumbnail_start_time_lessthan_0(self):
        """create thumbnail with start time less than 0"""
        source = {'key': self.key}
        capture = {'startTimeInSecond': -1}
        try: 
            resp = self.client.create_thumbnail_job(self.pipeline_name, source, capture=capture)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'capture.startTimeInSecond:capture.startTimeInSecond')
            else:
                assert True == False

    def test_create_thumbnail_start_time_float(self):
        """create thumbnail with start time float"""
        source = {'key': self.key}
        capture = {
            'mode': 'manual',
            'startTimeInSecond': 1.25,
            'endTimeInSecond': 50,
            'intervalInSecond': 10}
        resp = self.client.create_thumbnail_job(self.pipeline_name, source, capture=capture)
        nose.tools.assert_is_not_none(resp.job_id)

    def test_create_thumbnail_mode_manual_none_starttime(self):
        """create thumbnail mode is manual with start time is none"""
        source = {'key': self.key}
        capture = {
            'mode': 'manual'
                    }
        try: 
            resp = self.client.create_thumbnail_job(self.pipeline_name, source, capture=capture)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('start time is required in manual mode')
            else:
                assert True == False

    def test_create_thumbnail_end_time_lessthan_0(self):
        """create thumbnail with end time less than 0"""
        source = {'key': self.key}
        capture = {
            'mode': 'auto',
            'startTimeInSecond': 0,
            'endTimeInSecond': -1,
            'intervalInSecond': 10
            }
        try: 
            resp = self.client.create_thumbnail_job(self.pipeline_name, source, capture=capture)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'capture.endTimeInSecond:capture.endTimeInSecond')
            else:
                assert True == False

    def test_create_thumbnail_end_time_float(self):
        """create thumbnail with end time float"""
        source = {'key': self.key}
        capture = {
            'mode': 'manual',
            'startTimeInSecond': 1,
            'endTimeInSecond': 48.34,
            'intervalInSecond': 10}
        resp = self.client.create_thumbnail_job(self.pipeline_name, source, capture=capture)
        nose.tools.assert_is_not_none(resp.job_id)

    def test_create_thumbnail_mode_auto_with_starttime(self):
        """create thumbnail mode is auto with end time"""
        source = {'key': self.key}
        capture = {
            'mode': 'auto',
            'startTimeInSecond': 10
                    }
        try: 
            resp = self.client.create_thumbnail_job(self.pipeline_name, source, capture=capture)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                    'cannot specify start time, end time, interval or frame number in auto mode')
            else:
                assert True == False

    def test_create_thumbnail_mode_auto_with_endtime(self):
        """create thumbnail mode is auto with end time"""
        source = {'key': self.key}
        capture = {
            'mode': 'auto',
            'endTimeInSecond': 10
                    }
        try: 
            resp = self.client.create_thumbnail_job(self.pipeline_name, source, capture=capture)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                    'cannot specify start time, end time, interval or frame number in auto mode')
            else:
                assert True == False

    def test_create_thumbnail_mode_auto_with_interval(self):
        """create thumbnail mode is auto with interval time"""
        source = {'key': self.key}
        capture = {
            'mode': 'auto',
            'intervalInSecond': 10
                    }
        try: 
            resp = self.client.create_thumbnail_job(self.pipeline_name, source, capture=capture)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                    'cannot specify start time, end time, interval or frame number in auto mode')
            else:
                assert True == False

    def test_create_thumbnail_mode_manual_with_null_endtime(self):
        """create thumbnail mode is manual with end time none"""
        source = {'key': self.key}
        capture = {
            'mode': 'manual',
            'startTimeInSecond': 10
                    }
        resp = self.client.create_thumbnail_job(self.pipeline_name, source, capture=capture)
        nose.tools.assert_is_not_none(resp.job_id)

    def test_create_thumbnail_mode_manual_with_endtime_less_starttime(self):
        """create thumbnail mode is manual with endtime less than start time"""
        source = {'key': self.key}
        capture = {
            'mode': 'manual',
            'startTimeInSecond':20,
            'endTimeInSecond':10,
            'intervalInSecond': 5
                    }
        try: 
            resp = self.client.create_thumbnail_job(self.pipeline_name, source, capture=capture)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('start time cannot larger than end time')
            else:
                assert True == False

    def test_create_thumbnail_mode_manual_endtime_null(self):
        """create thumbnail mode is manual with endtime null"""
        source = {'key': self.key}
        capture = {
            'mode': 'manual',
            'startTimeInSecond':100,
            'intervalInSecond': 5
                    }
        resp = self.client.create_thumbnail_job(self.pipeline_name, source, capture=capture)
        nose.tools.assert_is_not_none(resp.job_id)

    def test_create_thumbnail_mode_manual_interval_null(self):
        """create thumbnail mode is manual with interval null"""
        source = {'key': '测试视频.mp4'}
        capture = {
            'mode': 'manual',
            'startTimeInSecond':10,
            'endTimeInSecond': 20
                    }
        resp = self.client.create_thumbnail_job(self.pipeline_name, source, capture=capture)
        print(resp)
        nose.tools.assert_is_not_none(resp.job_id)

    def test_create_thumbnail_interval_less_0(self):
        """create thumbnail mode is manual with interver null"""
        source = {'key': self.key}
        capture = {
            'mode': 'manual',
            'startTimeInSecond':1,
            'endTimeInSecond':50,
            'intervalInSecond': -1
                    }
        try: 
            resp = self.client.create_thumbnail_job(self.pipeline_name, source, capture=capture)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'capture.intervalInSecond:capture.intervalInSecond')
            else:
                assert True == False

    def test_create_thumbnail_interval_float(self):
        """create thumbnail mode is manual with interver float"""
        source = {'key': self.key}
        capture = {
            'mode': 'manual',
            'startTimeInSecond':1,
            'endTimeInSecond':50,
            'intervalInSecond': 1.56
                    }
        resp = self.client.create_thumbnail_job(self.pipeline_name, source, capture=capture)
        nose.tools.assert_is_not_none(resp.job_id)

    def test_create_thumbnail_start_equal_end(self):
        """create thumbnail start time equal end time"""
        source = {'key': self.key}
        capture = {
            'mode': 'manual',
            'startTimeInSecond':10,
            'endTimeInSecond':10,
            'intervalInSecond': 1.56
                    }
        resp = self.client.create_thumbnail_job(self.pipeline_name, source, capture=capture)
        nose.tools.assert_is_not_none(resp.job_id)
