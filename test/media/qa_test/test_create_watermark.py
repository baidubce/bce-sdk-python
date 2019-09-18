#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: test_create_watermark.py
Date: 2015/06/15 10:21:24
"""

import os
import re
import sys
import time

_NOW_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
_COMMON_PATH = _NOW_PATH + '../../../'
sys.path.insert(0, _COMMON_PATH)

import mediaBase
import media_config
from baidubce.services.media import media_client
from baidubce.exception import BceHttpClientError
from baidubce.exception import BceServerError
from baidubce.exception import BceClientError

import nose
from nose.tools import raises

class TestCreateWatermark(mediaBase.MediaBase):
    """test create watermark"""
    def __init__(self):
        """construction """
        mediaBase.MediaBase.__init__(self)
        self.watermark_id = None
        self.key = '120X90.jpg'
        self.client = media_client.MediaClient(media_config.config)

    def setUp(self):
        """create env"""
        time.sleep(2)
    
    def tearDown(self):
        """clear env"""
        time.sleep(2)
        if self.watermark_id:
            success = True
            try:
                self.client.delete_watermark(self.watermark_id)
                self.watermark_id = None
            except Exception as e:
                success = False
            nose.tools.assert_true(success)

    def test_create_watermark_normal(self):
        """create watermark normal"""
        success = True
        try:
            self.watermark_id = self.client.create_watermark(self.watermarkBucket, 
                    self.key).watermark_id
        except Exception as e:
            success = False
        nose.tools.assert_true(success)
    
    def test_create_watermark_with_bucket_chiness_name(self):
        """create watermark with chiness name"""
        try:
            self.watermark_id = self.client.create_watermark('中文bucket', 
                self.key).watermark_id
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        "Bucket 中文bucket doesn't exist or isn't in bj region")
            else:
                assert True == False, 'not throw bceServerError'

    def test_create_watermark_with_bucket_not_exist(self):
        """create watermark with bucket not exist"""
        try:
            self.watermark_id = self.client.create_watermark('not_exist_bucket', 
                self.key).watermark_id
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                       "Bucket not_exist_bucket doesn't exist or isn't in bj region")
            else:
                assert True == False, 'not throw bceServerError'
    
    def test_create_watermark_with_JPG_Picture(self):
        """create watermark with jpg picture"""
        self.watermark_id = self.client.create_watermark(self.watermarkBucket, 
                self.key).watermark_id
        nose.tools.assert_is_not_none(self.watermark_id)

    def test_create_watermark_with_BMP_Picture(self):
        """create watermark with bmp picture"""
        self.watermark_id = self.client.create_watermark(self.watermarkBucket, 
                '水印图片.bmp').watermark_id
        nose.tools.assert_is_not_none(self.watermark_id)

    def test_create_watermark_with_PNG_Picture(self):
        """create watermark with png picture"""
        self.watermark_id = self.client.create_watermark(self.watermarkBucket, 
                '/pic/水印图片.png').watermark_id
        nose.tools.assert_is_not_none(self.watermark_id)

    def test_create_watermark_with_TIF_Picture(self):
        """create watermark with tif picture"""
        self.watermark_id = self.client.create_watermark(self.watermarkBucket, 
                '水印图片.tif').watermark_id
        nose.tools.assert_is_not_none(self.watermark_id)

    def test_create_watermark_with_PBM_Picture(self):
        """create watermark with pbm picture"""
        self.watermark_id = self.client.create_watermark(self.watermarkBucket, 
                'logo2.pbm').watermark_id
        nose.tools.assert_is_not_none(self.watermark_id)

    def test_create_watermark_with_GIF_Picture(self):
        """create watermark with gif picture"""
        self.watermark_id = self.client.create_watermark(self.watermarkBucket, 
                'logo.gif').watermark_id
        nose.tools.assert_is_not_none(self.watermark_id)
    
    def test_create_watermark_with_not_picture(self):
        """create watermark with not picture"""
        try:
            self.watermark_id = self.client.create_watermark(self.watermarkBucket, 
                '/watermark/testpic.txt').watermark_id
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('invalid watermark format, only')
            else:
                assert True == False, 'not throw bceServerError'

    def test_create_watermark_with_not_exist_picture(self):
        """create watermark with not exist picture"""
        key = '/watermark/notexistpic.jpg'
        try:
            self.watermark_id = self.client.create_watermark(self.watermarkBucket, 
                key,).watermark_id
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('bos object: %s does not exist' % key)
            else:
                assert True == False, 'not throw bceServerError'
    
    def test_create_watermark_verticaloffsetinpixel_negative(self):
        """create watermark vertical offset in pixel negative"""
        try:
            self.watermark_id = self.client.create_watermark(self.watermarkBucket, 
                'watermark/logo.gif', vertical_offset_in_pixel=-1, 
                hori_offset_in_pixel=0).watermark_id
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith(
                        'verticalOffsetInPixel:verticalOffsetInPixel')
            else:
                assert True == False, 'not throw bceServerError'
    
    def test_create_watermark_verticaloffsetinpixel_string(self):
        """create watermark vertical off set pixel is string"""
        try:
            self.watermark_id = self.client.create_watermark(self.watermarkBucket, 
                'watermark/logo.gif', vertical_offset_in_pixel='13.21', 
                hori_offset_in_pixel=0).watermark_id
        except TypeError as e:
            assert e.message.startswith('arg "vertical_offset_in_pixel"= ')

    def test_create_watermark_horizontaloffsetinpixel_negative(self):
        """create watermark horizontal offset in pixel negative"""
        with nose.tools.assert_raises_regexp(BceHttpClientError, 
            'horizontalOffsetInPixel:horizontalOffsetInPixel=must be greater than or equal to 0'):
            self.watermark_id = self.client.create_watermark(self.watermarkBucket, 
                'watermark/logo.gif', vertical_offset_in_pixel=0, 
                hori_offset_in_pixel=-1).watermark_id

    def test_create_watermark_with_watermark_bucket_none(self):
        """create watermark with watermark bucket none"""
        with nose.tools.assert_raises_regexp(ValueError, 
                'arg "bucket" should not be None'):
            self.watermark_id = self.client.create_watermark(None, 
                'watermark/logo.gif').watermark_id

    def test_create_watermark_with_watermark_key_none(self):
        """create watermark with watermark key none"""
        with nose.tools.assert_raises_regexp(ValueError, 
                'arg "key" should not be None'):
            self.watermark_id = self.client.create_watermark(self.watermarkBucket, 
                    None).watermark_id

    def test_create_watermark_with_watermark_bucket_empty(self):
        """create watermark with watermark bucket '' """
        with nose.tools.assert_raises_regexp(BceClientError, 
                'bucket can\'t be empty string'):
            self.watermark_id = self.client.create_watermark('', 
                'watermark/logo.gif').watermark_id

    def test_create_watermark_with_watermark_key_empty(self):
        """create watermark with watermark key '' """
        with nose.tools.assert_raises_regexp(BceClientError, 
                'key can\'t be empty string'):
            self.watermark_id = self.client.create_watermark(self.watermarkBucket, 
                '').watermark_id
