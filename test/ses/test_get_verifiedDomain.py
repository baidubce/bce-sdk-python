#!/usr/bin/env python

"""
@author wangzheng11@baidu.com
@date 2014/10/08
@brief get verifieddomain
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


class TestGetVerifiedDomain(bes_base_case.BaseTest):
    def __init__(self):
        super(self.__class__, self).__init__()

    def setUp(self):
        time.sleep(1)

    def tearDown(self):
        pass

    def test_get_verifiedDomain_normal(self):
        #print self.host
        cli = client.SesClient(self.host, self.ak, self.sk)
        domain = 'baidu.com'
        resp = cli.get_domain_info(domain)
        print resp
        assert resp.status == 200, 'status is not 200'
        #print resp.body
        assert len(resp.body['detail']) >= 1 

    def test_get_verifiedDomain_badFormat(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        domain = 'asdfg'
        res = cli.get_domain_info(domain)
        #print res
        assert res.status == 200
        assert len(res.body['detail']) >= 1

    def test_get_verifiedDomain_empty(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        domain = "''"
        res = cli.get_domain_info(domain)
        assert res.status == 200
        assert len(res.body['detail']) >= 1
