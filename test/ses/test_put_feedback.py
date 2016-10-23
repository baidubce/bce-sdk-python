#!/usr/bin/env python

"""
@author wanglinqing01@baidu.com
@date 2014/10/08
@brief set feedback
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


class TestPutFeedback(bes_base_case.BaseTest):
    def __init__(self):
        super(self.__class__, self).__init__()

    def setUp(self):
        time.sleep(1)

    def tearDown(self):
        pass

    def test_put_feedback_normal(self):
        #print self.host
        cli = client.SesClient(self.host, self.ak, self.sk)
        email = 'wanglinqing2010@126.com'
        resp = cli.set_feedback(email, True)
        #resp.show()
        assert resp.status == 200, 'status is not 200'

    def test_put_feedback_onlyEmail(self):
        #print self.host
        cli = client.SesClient(self.host, self.ak, self.sk)
        email = 'wanglinqing2010@126.com'
        resp = cli.set_feedback(email)
        #resp.show()
        assert resp.status == 200, 'status is not 200'

    def test_put_feedback_emptyEmail(self):
        #print self.host
        cli = client.SesClient(self.host, self.ak, self.sk)
        email = "''"
        resp = cli.set_feedback(email)
        #resp.show()
        assert resp.status == 200, 'status is not 200'
