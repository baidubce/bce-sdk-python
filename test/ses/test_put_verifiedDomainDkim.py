#!/usr/bin/env python

"""
@author wangzheng11@baidu.com
@date 2014/10/08
@brief put_verifiedDomainDkim
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


class TestPutVerifiedDomainDkim(bes_base_case.BaseTest):
    def __init__(self):
        super(self.__class__, self).__init__()

    def setUp(self):
        time.sleep(1)

    def tearDown(self):
        pass

    def test_put_verifiedDomainDkim(self):
        #print self.host
        cli = client.SesClient(self.host, self.ak, self.sk)
        domain = 'qq.com'
        response = cli.create_verified_domain(domain)
        print response
        assert response.status == 200

        resp = cli.create_domain_dkim(domain)
        #print resp.status
        #resp.show()
        assert resp.status == 200, 'status not 200'
        #print resp.body
        assert len(resp.body['token']['keys'][0]) >= 1

    def test_put_verifiedDomainDkim_badFormat(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        flag = False
        try:
            domain = 'asdfg'
            res = cli.create_domain_dkim(domain)
        except ServerError as ex:
            flag = True
            info = traceback.format_exc()
            print ex
        finally:
            assert flag == True

    def test_put_verifiedDomainDkim_empty(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        flag = False
        try:
            domain = "''"
            res = cli.create_domain_dkim(domain)
        except ServerError as e:
            flag = True
            info = traceback.format_exc()
            print e
        finally:
            assert flag == True
