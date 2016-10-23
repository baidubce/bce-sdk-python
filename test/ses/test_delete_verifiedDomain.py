#!/usr/bin/env python

"""
@author wangzheng11@baidu.com
@date 2014/10/08
@brief delete_verifiedDomain
"""

import os
import sys
import time


_NOW_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
_BCE_PATH = _NOW_PATH + '../'
sys.path.insert(0, _BCE_PATH)

import bes_base_case
from baidubce.services.ses import client
from baidubce.exception import *


class TestDeleteVerifiedDomain(bes_base_case.BaseTest):
    def __init__(self):
        super(self.__class__, self).__init__()

    def setUp(self):
        time.sleep(1)

    def tearDown(self):
        pass

    def test_delete_verifiedDomain(self):
        #print self.host
        cli = client.SesClient(self.host, self.ak, self.sk)
        domain = 'baidu.com'
        #create verified_domain
        resp = cli.create_verified_domain(domain)
        #print resp.status
        #print resp
        assert resp.status == 200, 'status not 200'

        response = cli.delete_domain(domain)
        #print resp
        assert response.status == 200

    def test_delete_verifiedDomain_badFormat(self):
        cli = client.SesClient(self.host, self.ak, self.sk)

        domain = 'asdfg'
        res = cli.delete_domain(domain)
        #print res.status
        assert res.status == 200

    def test_delete_verifiedDomain_empty(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        domain = "''"
        res = cli.delete_domain(domain)
        assert res.status == 200
