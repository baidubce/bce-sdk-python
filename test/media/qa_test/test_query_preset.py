#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright 2015 Baidu, Inc.
# 
########################################################################
 
"""
File: test_query_preset.py
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

class TestQueryPreset(mediaBase.MediaBase):
    """test query preset"""
    def __init__(self):
        """construction """
        mediaBase.MediaBase.__init__(self)
        self.pre = self.prefix + 'querypreset'
        self.preset_name = self.pre
        self.container = 'mp4'
        self.client = media_client.MediaClient(media_config.config)
        self.key = 'watermark.jpg'

    def setUp(self):
        """create env"""
        time.sleep(1)
        resp = self.client.create_preset(self.preset_name, self.container, True)
        nose.tools.assert_true(resp)

    def tearDown(self):
        """clear env"""
        time.sleep(1)
        result = self.client.list_presets()
        for each_val in result.presets:
            preset_name = each_val.preset_name
            if(preset_name.startswith(self.pre)):
                resp = self.client.delete_preset(preset_name)
                nose.tools.assert_is_not_none(resp)

    def test_query_preset_exist(self):
        """query exist preset"""
        resp = self.client.get_preset(self.preset_name)
        assert resp.state == 'ACTIVE'
        assert resp.preset_name == self.preset_name

    def test_query_preset_deleted(self):
        """query deleted preset"""
        resp = self.client.delete_preset(self.preset_name)
        nose.tools.assert_is_not_none(resp)
        resp = self.client.get_preset(self.preset_name)
        assert resp.state == 'INACTIVE'
        assert resp.preset_name == self.preset_name

    def test_query_preset_not_exist(self):
        """query not exist preset"""
        try:
            resp = self.client.get_preset('not_exist_preset')
        except BceHttpClientError as e:
            if isinstance(e.last_error, BceServerError):
                assert e.last_error.message.startswith('The requested preset does not exist')
            else:
                assert True == False, 'not throw BceServerError'

    def test_query_preset_param_none(self):
        """query preset with params is none"""
        try:
            resp = self.client.get_preset(None)
        except ValueError as e:
            assert e.message.startswith('arg "preset_name" should not be None')

    def test_query_preset_param_empty(self):
        """query preset with params is empty"""
        with nose.tools.assert_raises_regexp(BceClientError, 
                'preset_name can\'t be empty string'):
            resp = self.client.get_preset('')
