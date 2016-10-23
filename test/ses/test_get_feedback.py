#!/usr/bin/env python

"""
@author wanglinqing01@baidu.com
@date 2014/10/08
@brief get feedback
"""

import os
import sys
import json
import time

_NOW_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
_BCE_PATH = _NOW_PATH + '../'
sys.path.insert(0, _BCE_PATH)

import bes_base_case
from baidubce.services.ses import client


class TestGetFeedback(bes_base_case.BaseTest):
    def __init__(self):
        super(self.__class__, self).__init__()

    def setUp(self):
        time.sleep(1)

    def tearDown(self):
        pass

    def test_get_feedback_normal(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        #set feedback
        email = 'wanglinqing2010@126.com'
        resp_set = cli.set_feedback(email, True)
        assert resp_set.status == 200, 'status is not 200'

        #check data
        resp = cli.get_feedback()
        assert resp.status == 200, 'status is not 200'
        assert resp.body['email'] == email
        assert resp.body['enabled'] == True

    def test_get_feedback_setEmail(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        #set feedback
        email = 'wanglinqing2010@baidu.com'
        resp_set = cli.set_feedback(email)
        assert resp_set.status == 200, 'status is not 200'

        #check data
        resp = cli.get_feedback()
        assert resp.status == 200, 'status is not 200'
        assert resp.body['email'] == email
        assert resp.body['enabled'] == False
