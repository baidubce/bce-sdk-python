#!/usr/bin/env python

"""
@author wangzheng11@baidu.com
@date 2014/10/08
@brief put_disableDomainDkim
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
from baidubce.exception import *


class TestPutDisableDomainDkim(bes_base_case.BaseTest):
    def __init__(self):
        super(self.__class__, self).__init__()

    def setUp(self):
        time.sleep(1)

    def tearDown(self):
        pass

    def test_put_disableDomainDkim(self):
        #print self.host
        cli = client.SesClient(self.host, self.ak, self.sk)
        domain = 'baidu.com'
        response = cli.create_verified_domain(domain)
        #response.show()
        assert response.status == 200

        resp = cli.disable_domain_dkim(domain)
        #print resp
        assert resp.status == 200, 'status not 200'

        rsp = cli.get_domain_info(domain)
        #print rsp.body 
        assert rsp.body['detail']['dkim_attr']['dkim_enabled'] == False 
