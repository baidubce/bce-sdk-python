#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: test_create_preset.py
Date: 2015/06/15 10:15:40
"""
import os
import sys
import unittest
import json
import time
import media_config
import re
import mediaBase
import random

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

class TestCreatePreset(mediaBase.MediaBase):
    """test create preset"""
    def __init__(self):
        """construction """
        mediaBase.MediaBase.__init__(self)
        self.pre = self.prefix + 'createpreset'
        self.preset_name = self.convertName(self.pre)
        self.container = 'mp4'
        self.client = media_client.MediaClient(media_config.config)
        self.key = 'watermark.jpg'
        self.watermark_id = None

    def setUp(self):
        """create env"""
        #time.sleep(1)
        succ = True
        try:
            self.watermark_id = self.client.create_watermark(self.watermarkBucket, 
                   self.key).watermark_id
        except Exception as e:
            print(e.message)
            succ = False
        nose.tools.assert_true(succ)

    def tearDown(self):
        """clear env"""
        result = self.client.list_presets()
        for each_val in result.presets:
            preset_name = each_val.preset_name
            if(preset_name.startswith(self.pre)):
                resp = self.client.delete_preset(preset_name)
                nose.tools.assert_is_not_none(resp)

        if self.watermark_id:
            resp = self.client.delete_watermark(self.watermark_id)
            nose.tools.assert_is_not_none(resp)
            self.watermark_id = None

        #result = self.client.list_watermarks()
        #for each_val in result.watermarks:
        #    resp = self.client.delete_watermark(each_val.watermark_id)
        #    nose.tools.assert_is_not_none(resp)

    def test_create_preset_with_name_none(self):
        """create preset with preset name none"""
        preset_name = None
        with nose.tools.assert_raises_regexp(ValueError, 
                'arg "preset_name" should not be None'):
            ret = self.client.create_preset(preset_name, self.container)

    def create_preset_with_name_different(self, name):
        """test create preset with nama different"""
        with nose.tools.assert_raises_regexp(BceHttpClientError, 
                'BceServerError: preset name must match pattern:'):
            ret = self.client.create_preset(name, self.container, True)

    def test_create_preset_with_name_empty(self):
        """create preset with preset name empty"""
        preset_name = ''
        with nose.tools.assert_raises_regexp(BceClientError, 
                'preset_name can\'t be empty string'):
            ret = self.client.create_preset(preset_name, self.container, True)

    def test_create_preset_with_container_empty(self):
        """create preset with preset container empty"""
        container = ''
        with nose.tools.assert_raises_regexp(BceClientError, 
                'container can\'t be empty string'):
            ret = self.client.create_preset(self.preset_name, container)

    def test_create_preset_with_container_ahls(self):
        """create preset with container a-hls"""
        container = 'a-hls'
        ret = self.client.create_preset(self.preset_name, container, True) 
        nose.tools.assert_is_not_none(ret)
    
    def test_create_preset_with_name_chinese(self):
        """create preset with chinese name"""
        preset_name = '创建模板'
        self.create_preset_with_name_different(preset_name)

    def test_create_preset_with_upper_letter(self):
        """create preset with upper case letter"""
        preset_name = 'CREATEPRESET'
        self.create_preset_with_name_different(preset_name)

    def test_create_preset_with_pure_digital(self):
        """create preset with pure digital"""
        preset_name = '123456'
        self.create_preset_with_name_different(preset_name)

    def test_create_preset_with_first_not_char(self):
        """create preset with name first not char"""
        preset_name = '123preset'
        self.create_preset_with_name_different(preset_name)

    def test_create_preset_with_mid_lined(self):
        """create preset with name include mid lined"""
        preset_name = 'preset-1-2'
        self.create_preset_with_name_different(preset_name)

    def test_create_preset_with_blank(self):
        """create preset with name include blank"""
        preset_name = 'preset name'
        self.create_preset_with_name_different(preset_name)

    def test_create_preset_with_name_more_40_chars(self):
        """create preset with name more than 40 cahrs"""
        preset_name = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        self.create_preset_with_name_different(preset_name)

    def test_create_preset_with_name_equal_40_chars(self):
        """create preset with name equal 40 chars"""
        print(len(self.preset_name))
        nose.tools.assert_equal(len(self.preset_name), 40)
        transmux = True
        resp = self.client.create_preset(self.preset_name, self.container, transmux)
        nose.tools.assert_is_not_none(resp)

###############test desc#################
    def random_str(self, random_len=8):
        """return random string"""
        str = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) - 1
        for i in range(random_len):
            str += chars[random.randint(0, length)]
        return str

    def test_create_preset_with_desc_more_128_chars(self):
        """create preset with description more than 128 cahrs"""
        transmux = True
        desc = self.random_str(129)
        with nose.tools.assert_raises_regexp(BceHttpClientError, 
                'BceServerError: description:description=size must be between 0 and 128'):
            resp = self.client.create_preset(self.preset_name, 
                   self.container, transmux, description=desc)

    def test_create_preset_with_desc_equal_128_chars(self):
        """create preset with description equal 128 chars"""
        transmux = True
        desc = self.random_str(128)
        resp = self.client.create_preset(self.preset_name, 
                self.container, transmux, description=desc)
        nose.tools.assert_is_not_none(resp)

    def test_create_preset_with_desc_special_chars(self):
        """create preset with description special chars"""
        transmux = True
        desc = '~=-@-45 //\vthis is a special desc 含有中文特殊字符~!@#$#$$%(()()@####\\'
        resp = self.client.create_preset(self.preset_name, 
                self.container, transmux, description=desc)
        nose.tools.assert_is_not_none(resp)

    def test_create_preset_with_none_desc(self):
        """create preset with description special chars"""
        transmux = True
        desc = None
        resp = self.client.create_preset(self.preset_name, 
                self.container, transmux, description=desc)
        nose.tools.assert_is_not_none(resp)

    def test_create_preset_none_container(self):
        """create preset with container none"""
        self.container = None
        try:
            resp = self.client.create_preset(self.preset_name, self.container, True)
        except ValueError as e:
            assert e.message.startswith('arg "container" should not be None')

    def test_create_preset_with_container_not_in_enum(self):
        """create preset with container not in enum"""
        transmux = True
        try:
            resp = self.client.create_preset(self.preset_name, 
                   'ceshimp4', transmux)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'Could not read JSON: Can not construct instance of')
            else:
                assert True == False, 'not throw BceServerError'

    def test_create_preset_with_transmux_is_false(self):
        """create preset with container is false"""
        audio = {'bitRateInBps': 25600}
        resp = self.client.create_preset(self.preset_name, 'mp3', audio=audio)
        nose.tools.assert_is_not_none(resp)

    def test_create_preset_with_transmux_not_in_enum(self):
        """create preset with transmux not in enum"""
        try:
            resp = self.client.create_preset(self.preset_name, 'mp4', 'test')
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'Could not read JSON: Can not construct instance of')
            else:
                assert True == False, 'not throw BceServerError'

    def test_create_preset_with_transmux_is_false_with_no_audio_and_video(self):
        """create preset with transmux is false with no audio and video"""
        try:
            resp = self.client.create_preset(self.preset_name, 'mp4')
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'video and audio cannot both be set to null when transmux equals false')
            else:
                assert True == False, 'not throw BceServerError'

############test clip###############
    def test_create_preset_with_clip_normal(self):
        """create preset with clip normal"""
        clip = {'startTimeInSecond': 0,
                'durationInSecond': 60
                }
        resp = self.client.create_preset(self.preset_name, self.container, True, clip=clip)
        nose.tools.assert_is_not_none(resp)

    def test_create_preset_with_clip_duration_equal_0(self):
        """create preset with clip duration equal 0"""
        clip = {'startTimeInSecond': 0,
                'durationInSecond': 0
                }
        try:
            resp = self.client.create_preset(self.preset_name, self.container, True, clip=clip)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'clip.durationInSecond:clip.durationInSecond=must be greater than or ')
            else:
                assert True == False, 'not throw BceServerError'

    def test_create_preset_with_startTimeInSecond_is_negative(self):
        """create preset with startTimeInSecond is negative"""
        clip = {'startTimeInSecond': -1,
                'durationInSecond': 60
                }
        try:
            resp = self.client.create_preset(self.preset_name, self.container, True, clip=clip)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'clip.startTimeInSecond:clip.startTimeInSecond=')
            else:
                assert True == False, 'not throw BceServerError'

    def test_create_preset_with_startTimeInSecond_is_positive(self):
        """create preset with startTimeInSecond is positive"""
        clip = {'startTimeInSecond': 10,
                'durationInSecond': 60
                }
        resp = self.client.create_preset(self.preset_name, self.container, True, clip=clip)
        nose.tools.assert_is_not_none(resp)

    def test_create_preset_with_startTimeInSecond_is_string(self):
        """create preset with startTimeInSecond is string"""
        clip = {'startTimeInSecond': 'abc',
                'durationInSecond': 60
                }
        try:
            resp = self.client.create_preset(self.preset_name, self.container, True, clip=clip)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'Could not read JSON: Can not construct instance of')
            else:
                assert True == False, 'not throw BceServerError'

    def test_create_preset_with_durationInSecond_is_negative(self):
        """create preset with durationInSecond is snegative"""
        clip = {'startTimeInSecond': 10,
                'durationInSecond': -1
                }
        try:
            resp = self.client.create_preset(self.preset_name, self.container, True, clip=clip)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'clip.durationInSecond:clip.durationInSecond=')
            else:
                assert True == False, 'not throw BceServerError'

    def test_create_preset_with_durationInSecond_is_string(self):
        """create preset with durationInSecond is string"""
        clip = {'startTimeInSecond': 10,
                'durationInSecond': 'abc'
                }
        try:
            resp = self.client.create_preset(self.preset_name, self.container, True, clip=clip)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'Could not read JSON: Can not construct instance of')
            else:
                assert True == False, 'not throw BceServerError'

################test audio################3
    
    def test_create_preset_with_audio_bitrateinbps_less_than_1000(self):
        """audio bitrateinbps less than 1000"""
        audio = {'bitRateInBps': 10}
        try:
            resp = self.client.create_preset(self.preset_name, self.container, audio=audio)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'audio.bitRateInBps:audio.bitRateInBps=must be greater than or equal')
            else:
                assert True == False, 'not throw BceServerError'

    def test_create_preset_with_audio_bitrateinbps_not_integer(self):
        """audio bitrateinbps not integer"""
        audio = {'bitRateInBps': 1000.34}
        resp = self.client.create_preset(self.preset_name, self.container, audio=audio)
        nose.tools.assert_is_not_none(resp)

    def test_create_preset_with_audio_bitrateinbps_is_none(self):
        """audio bitrateinbps none"""
        audio = {'sampleRateInHz': 22050}
        try:
            resp = self.client.create_preset(self.preset_name, self.container, audio=audio)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'audio.bitRateInBps:audio.bitRateInBps=may not be null')
            else:
                assert True == False, 'not throw BceServerError'

    def test_create_preset_with_audio_samplerateinhz_not_in_enum(self):
        """audio sampleRateInHz not in enum"""
        audio = {
            'bitRateInBps': 1989,
            'sampleRateInHz': 22051}
        try:
            resp = self.client.create_preset(self.preset_name, self.container, audio=audio)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'audio.sampleRateInHz should in [22050, 32000, 44100, 48000, 96000]')
            else:
                assert True == False, 'not throw BceServerError'

    def test_create_preset_with_audio_samplerateinhz_not_integer(self):
        """audio bitrateinbps not integer"""
        audio = {
            'bitRateInBps': 1989,
            'sampleRateInHz': 32000.56}
        resp = self.client.create_preset(self.preset_name, self.container, audio=audio)
        nose.tools.assert_is_not_none(resp)

    def test_create_preset_with_audio_channels_not_in_enum(self):
        """audio channel not in enum"""
        audio = { 
            'bitRateInBps': 1989,
            'sampleRateInHz': 44100,
            'channels': 5}
        try:
            resp = self.client.create_preset(self.preset_name, self.container, audio=audio)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'audio.channels:audio.channels=')
            else:
                assert True == False, 'not throw BceServerError'

    def test_create_preset_with_audio_chanel_not_integer(self):
        """audio bitrateinbps not integer"""
        audio = {
            'bitRateInBps': 1989,
            'sampleRateInHz': 48000,
            'channels': 2.89}
        resp = self.client.create_preset(self.preset_name, self.container, audio=audio)
        nose.tools.assert_is_not_none(resp)

    def test_create_preset_with_audio_normal(self):
        """audio normal"""
        audio = {
            'bitRateInBps': 1989,
            'sampleRateInHz': 96000,
            'channels': 1}
        resp = self.client.create_preset(self.preset_name, self.container, audio=audio)
        nose.tools.assert_is_not_none(resp)

#####################test video##############
    def test_create_preset_with_video_normal(self):
        """create preset with video normal"""
        video = {
            'bitRateInBps': 32000
        }
        resp = self.client.create_preset(self.preset_name, self.container, video=video)
        nose.tools.assert_is_not_none(resp)
    
    def test_create_preset_with_bitrateinbps_less_than_32000(self):
        """create preset with video bitrateinbps less than 32000"""
        video = {
            'bitRateInBps': 3200
        }
        try:
            resp = self.client.create_preset(self.preset_name, self.container, video=video)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'video.bitRateInBps:video.bitRateInBps=must be greater than or equal to ')
            else:
                assert True == False

    def test_create_preset_with_video_profile_not_in_enum(self):
        """create preset with video profile not in enum"""
        options = {'profile': 'baseline1'}
        video = {
            'codecOptions': options,
            'bitRateInBps': 32000
        }
        try:
            resp = self.client.create_preset(self.preset_name, self.container, video=video)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'Could not read JSON: Can not construct instance of ')
            else:
                assert True == False

    def test_create_preset_with_video_maxframerate_not_in_enum(self):
        """create preset with video max frame rate not in enum"""
        video = {
            'bitRateInBps': 32000,
            'maxFrameRate': 12
        }
        try:
            resp = self.client.create_preset(self.preset_name, self.container, video=video)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'video.maxFrameRate should in [10.0, 15.0, 20.0, 23.97, 24.0, 25')
            else:
                assert True == False

    def test_create_preset_with_video_maxwidth_less_128(self):
        """create preset with video max width less than 128"""
        video = {
            'bitRateInBps': 32000,
            'maxWidthInPixel': 127.5
        }
        try:
            resp = self.client.create_preset(self.preset_name, self.container, video=video)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'video.maxWidthInPixel:video.maxWidthInPixel=must be greater than or ')
            else:
                assert True == False

    def test_create_preset_with_video_maxwidth_more_4096(self):
        """create preset with video max width more than 4096"""
        video = {
            'bitRateInBps': 32000,
            'maxWidthInPixel': 4097
        }
        try:
            resp = self.client.create_preset(self.preset_name, self.container, video=video)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'video.maxWidthInPixel:video.maxWidthInPixel=must be less than or equal')
            else:
                assert True == False

    def test_create_preset_with_video_maxheight_less_96(self):
        """create preset with video max height less than 96"""
        video = {
            'bitRateInBps': 32000,
            'maxHeightInPixel': 95.9
        }
        try:
            resp = self.client.create_preset(self.preset_name, self.container, video=video)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'video.maxHeightInPixel:video.maxHeightInPixel=must be greater than or ')
            else:
                assert True == False

    def test_create_preset_with_video_maxheight_more_3072(self):
        """create preset with video max height more than 3072"""
        video = {
            'bitRateInBps': 32000,
            'maxHeightInPixel': 3073
        }
        try:
            resp = self.client.create_preset(self.preset_name, self.container, video=video)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'video.maxHeightInPixel:video.maxHeightInPixel=must be less than or ')
            else:
                assert True == False

    def test_create_preset_with_video_sizingpolicy_not_in_enum(self):
        """create preset with video sizing policy not in enum"""
        video = {
            'bitRateInBps': 32000,
            'sizingPolicy': 'shrinkToFit11'
        }
        try:
            resp = self.client.create_preset(self.preset_name, self.container, video=video)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'Could not read JSON: Can not construct instance of com.baidu.bce')
            else:
                assert True == False

####################test encryption############

    def test_create_preset_with_encryption_aeskey_more_than_16chars(self):
        """create preset with video sizing policy not in enum"""
        video = {
            'bitRateInBps': 32000,
            'sizingPolicy': 'shrinkToFit'
        }
        encryption = {
            'strategy': 'Fixed',
            'aesKey': 'abcdefghij1234567'
        }
        try:
            resp = self.client.create_preset(self.preset_name, 
                    self.container, video=video, encryption=encryption)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'encryption.aesKey:encryption.aesKey=must match')
            else:
                assert True == False

    def test_create_preset_with_encryption_steategy_none(self):
        """create preset with video sizing policy not in enum"""
        encryption = {
            'aesKey': 'abcdefghij123456'
        }
        try:
            resp = self.client.create_preset(self.preset_name, 
                    self.container, True, encryption=encryption)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'encryption.strategy:encryption.strategy=may not be null')
            else:
                assert True == False

################test other####################

    def test_create_preset_duplication(self):
        """duplication preset"""
        resp = self.client.create_preset(self.preset_name, self.container, True)
        nose.tools.assert_is_not_none(resp)
        try:
            resp = self.client.create_preset(self.preset_name, self.container, True)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'duplicated preset name:')
            else:
                assert True == False, 'not throw BceServerError'

    def test_create_preset_with_all_params(self):
        """create preset with all params"""
        desc = 'this is a description with creating preset all params'
        clip = {
            'startTimeInSecond':0,
            'durationInSecond': 50
        }
        audio = {
            'bitRateInBps': 1980,
            'sampleRateInHz': 32000,
            'channels': 1,
        }
        codecOptions = {'profile': 'baseline'}
        video = {
            'codec': 'h264',
            'codecOptions': codecOptions,
            'bitRateInBps': 32000,
            'maxFrameRate': 30,
            'maxWidthInPixel': 4096,
            'maxHeightInPixel': 96,
            'sizingPolicy': 'stretch'
        }
        encryption = {
            'aesKey': 'abcdefghij123456',
            'strategy': 'Fixed'
        }
        resp = self.client.create_preset(self.preset_name, self.container, False, 
                description=desc, clip=clip, audio=audio, video=video, 
                watermark_id=self.watermark_id, encryption=encryption)
        nose.tools.assert_is_not_none(resp)

    def test_create_preset_with_watermark(self):
        """test create preset with transmux true but have watermark"""
        try:
            resp = self.client.create_preset(self.preset_name, self.container, \
                True, watermark_id=self.watermark_id)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'watermark is not supported in Transmux mode')
            else:
                assert True == False, 'not throw BceServerError'

    def test_create_preset_with_watermark_deleted(self):
        """test create preset with watermark deleted"""
        resp = self.client.delete_watermark(self.watermark_id)
        codecOptions = {'profile': 'baseline'}
        video = {
            'codec': 'h264',
            'codecOptions': codecOptions,
            'bitRateInBps': 32000,
            'maxFrameRate': 30,
            'maxWidthInPixel': 4096,
            'maxHeightInPixel': 96,
            'sizingPolicy': 'stretch'
        }
        with nose.tools.assert_raises_regexp(BceHttpClientError, 
                'BceServerError: watermark: %s does not exist' % self.watermark_id):
            resp = self.client.create_preset(self.preset_name, self.container, \
                False, video=video, watermark_id=self.watermark_id)
            print(resp.content)
        self.watermark_id = None

    def test_create_preset_with_watermarkid_empty(self):
        """test create preset with watermarkid empty"""
        codecOptions = {'profile': 'baseline'}
        video = {
            'codec': 'h264',
            'codecOptions': codecOptions,
            'bitRateInBps': 32000,
            'maxFrameRate': 30,
            'maxWidthInPixel': 4096,
            'maxHeightInPixel': 96,
            'sizingPolicy': 'stretch'
        }
        try:
            resp = self.client.create_preset(self.preset_name, self.container, \
                False, video=video, watermark_id='')
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('watermark: ')
            else:
                assert True == False, 'not throw BceServerError'

    def test_create_preset_with_watermarkid_none(self):
        """test create preset with watermarkid none"""
        resp = self.client.create_preset(self.preset_name, self.container, 
                True, watermark_id=None)
        nose.tools.assert_is_not_none(resp)
