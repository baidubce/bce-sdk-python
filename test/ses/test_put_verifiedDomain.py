#!/usr/bin/env python

"""
@author wangzheng11@baidu.com
@date 2014/10/08
@brief put_verifiedDomain
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


class TestPutVerifiedDomain(bes_base_case.BaseTest):
    def __init__(self):
        super(self.__class__, self).__init__()

    def setUp(self):
        time.sleep(1)

    def tearDown(self):
        pass

    def test_put_verifiedDomain(self):
        #print self.host
        cli = client.SesClient(self.host, self.ak, self.sk)
        domain = 'baidu.com'
        resp = cli.create_verified_domain(domain)
        #print resp.status
        print resp
        assert resp.status == 200, 'status not 200'

        #get domain
        response = cli.get_domain_info(domain)
        #response.show()
        assert response.status == 200

    def test_put_verifiedDomain_badFormat(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        flag = False
        try:
            domain = 'asdfgh'
            res = cli.create_verified_domain(domain)           
        except exception.ServerError as ex:
            flag = True
            info = traceback.format_exc()
            #print traceback.format_exc()
            print ex          
        finally:
            assert flag == True

    def test_put_verifiedDomain_Empty(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        flag = False
        try:
            domain = "''"
            res = cli.create_verified_domain("domain")
        except exception.ServerError as e:
            flag = True
            info = traceback.format_exc()
            print e
        finally:
            assert flag == True  
