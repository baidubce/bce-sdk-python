#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: test_list_preset.py
Date: 2015/06/29 14:27:40
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

class TestListPreset(mediaBase.MediaBase):
    """test List preset"""
    def __init__(self):
        """construction """
        mediaBase.MediaBase.__init__(self)
        self.pre = self.prefix + 'createthumb'
        self.preset_name = self.pre
        self.container = 'mp4'
        self.client = media_client.MediaClient(media_config.config)

    def setUp(self):
        """create env"""
        resp = self.client.create_preset(self.preset_name, self.container, True)
        nose.tools.assert_true(resp)

    def tearDown(self):
        """clear env"""
        result = self.client.list_presets()
        for each_val in result.presets:
            preset_name = each_val.preset_name
            if(preset_name.startswith(self.pre)):
                resp = self.client.delete_preset(preset_name)
                nose.tools.assert_is_not_none(resp)

    def test_list_preset_with_add_one(self):
        """list preset with add one"""
        resp = self.client.list_presets()
        before_len = len(resp.presets)
        preset_name = self.convertName(self.pre)
        resp = self.client.create_preset(preset_name, self.container, True)
        nose.tools.assert_true(resp)

        resp = self.client.list_presets()
        after_len = len(resp.presets)

        assert after_len == before_len + 1

    def test_list_preset_with_delete_one(self):
        """list preset with delete one"""
        resp = self.client.list_presets()
        before_len = len(resp.presets)

        resp = self.client.delete_preset(self.preset_name)
        nose.tools.assert_true(resp)

        resp = self.client.list_presets()
        after_len = len(resp.presets)

        assert after_len == before_len - 1
