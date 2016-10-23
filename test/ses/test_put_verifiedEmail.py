#!/usr/bin/env python

"""
@author wanglinqing01@baidu.com
@date 2014/10/08
@brief put_verifiedEmail
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


class TestPutVerifiedEmail(bes_base_case.BaseTest):
    def __init__(self):
        super(self.__class__, self).__init__()

    def setUp(self):
        time.sleep(1)

    def tearDown(self):
        pass

    def test_put_verifiedEmail_normal(self):
        #print self.host
        cli = client.SesClient(self.host, self.ak, self.sk)
        resp = cli.create_verified_email("wanglinqing2010@126.com")
        #print resp.status
        assert resp.status == 200, 'status is not 200'

    def test_put_verifiedEmail_errorFormat(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        flag = False
        try:
            resp = cli.create_verified_email('123456789')
        except exception.ServerError as e:
            flag = True
            print 'have an exception'
            tracemsg = traceback.format_exc()
            #traceback.print_exc()
            #print tracemsg
            print e
        finally:
            assert flag == True, 'it should throw exception'

    def test_put_verifiedEmail_emptyEmail(self):
        cli = client.SesClient(self.host, self.ak, self.sk)
        flag = False
        try:
            resp = cli.create_verified_email("''")
        except exception.ServerError as e:
            flag = True
            print 'have an exception'
            tracemsg = traceback.format_exc()
            #traceback.print_exc()
            #print tracemsg
            print e
        finally:
            assert flag == True, 'it should throw exception'
