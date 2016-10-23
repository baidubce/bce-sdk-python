#!/usr/bin/env python

"""
@author wanglinqing01@baidu.com
@date 2014/10/08
@brief get verifiedEmail
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


class TestGetVerifiedEmail(bes_base_case.BaseTest):
    def __init__(self):
        super(self.__class__, self).__init__()

    def setUp(self):
        time.sleep(1)

    def tearDown(self):
        pass

    def test_get_verifiedEmail_normal(self):
        #print self.host
        cli = client.SesClient(self.host, self.ak, self.sk)
        email = 'wanglinqing01@baidu.com'
        resp = cli.get_verified_email(email)
        print resp
        assert resp.status == 200, 'status is not 200'
        print resp.body
        assert resp.body['detail']['status'] == 0, 'email is verified'

    def test_get_verifiedEmail_emailNotExist(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        email = 'wanglinqingNotExist@baidu.com'
        resp = cli.get_verified_email(email)
        print resp
        assert resp.status == 200, 'status is not 200'
        assert resp.body['detail']['status'] == 5, 'email is not verified'

    def test_get_verifiedEmail_emailIsEmpty(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        email = "''"
        resp = cli.get_verified_email(email)
        print resp
        assert resp.status == 200, 'status is not 200'
        assert resp.body['detail']['status'] == 5, 'email is not verified'

    def test_get_verifiedEmail_emailInt(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        email = 12345678
        resp = cli.get_verified_email(email)
        print resp
        assert resp.status == 200, 'status is not 200'
        assert resp.body['detail']['status'] == 5, 'email is not verified'
