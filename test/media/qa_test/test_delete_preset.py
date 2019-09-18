#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: test_delete_preset.py
Date: 2015/06/29 14:44:40
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

class TestDeletePreset(mediaBase.MediaBase):
    """test delete preset"""
    def __init__(self):
        """construction """
        mediaBase.MediaBase.__init__(self)
        self.pre = self.prefix + 'deletepreset'
        self.preset_name = self.pre
        self.container = 'mp4'
        self.client = media_client.MediaClient(media_config.config)

    def setUp(self):
        """create env"""
        resp = self.client.create_preset(self.preset_name, self.container, True)
        nose.tools.assert_is_not_none(resp)

    def tearDown(self):
        """clear env"""
        result = self.client.list_presets()
        for each_val in result.presets:
            preset_name = each_val.preset_name
            if(preset_name.startswith(self.pre)):
                resp = self.client.delete_preset(preset_name)
                nose.tools.assert_is_not_none(resp)

    def test_delete_preset_exist(self):
        """delete exist preset"""
        resp = self.client.delete_preset(self.preset_name)
        nose.tools.assert_is_not_none(resp)

    def test_delete_preset_repeated(self):
        """delete preset repeated"""
        resp = self.client.delete_preset(self.preset_name)
        nose.tools.assert_is_not_none(resp)
        try:
            resp = self.client.delete_preset(self.preset_name)
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('The requested preset does not exist')
            else:
                assert True == False, 'not throw BceServerError'

    def test_delete_preset_not_exist(self):
        """delete preset not exist"""
        try:
            resp = self.client.delete_preset('not_exist_preset')
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('The requested preset does not exist')
            else:
                assert True == False, 'not throw BceServerError'

    def test_delete_preset_name_empty(self):
        """delete preset with name empty"""
        with nose.tools.assert_raises_regexp(BceClientError, 
                'preset_name can\'t be empty string'):
            resp = self.client.delete_preset('')

    def test_delete_preset_name_none(self):
        """delete preset with name none"""
        try:
            resp = self.client.delete_preset(None)
        except ValueError as e:
            assert e.message.startswith('arg "preset_name" should not be None')
