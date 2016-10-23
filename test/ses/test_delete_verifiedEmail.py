#!/usr/bin/env python

"""
@author wanglinqing01@baidu.com
@date 2014/10/08
@brief delete verifiedEmail
"""

import os
import sys
import time
import traceback

_NOW_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
_BCE_PATH = _NOW_PATH + '../'
sys.path.insert(0, _BCE_PATH)

import bes_base_case
from baidubce.services.ses import client
from baidubce import exception


class TestDeleteVerifiedEmail(bes_base_case.BaseTest):
    def __init__(self):
        super(self.__class__, self).__init__()

    def setUp(self):
        time.sleep(1)

    def tearDown(self):
        pass

    def test_delete_verifiedEmail_normal(self):
        #print self.host
        cli = client.SesClient(self.host, self.ak, self.sk)
        email = 'wanglinqing2010@126.com'
        resp = cli.delete_verified_email(email)
        #print resp.status
        assert resp.status == 200, 'status is not 200'

    def test_delete_verifiedEmail_abnormal(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        email = "''"
        resp = cli.delete_verified_email(email)
        assert resp.status == 200, 'status is not 200'
