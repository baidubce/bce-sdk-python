#!/usr/bin/env python

"""
@author wanglinqing01@baidu.com
@date 2014/10/08
@brief get check recipientBlacklist
"""

import os
import sys
import json

_NOW_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
_BCE_PATH = _NOW_PATH + '../'
sys.path.insert(0, _BCE_PATH)

import bes_base_case
from baidubce.services.ses import client


class TestGetiCheckRecipientBlacklist(bes_base_case.BaseTest):
    def __init__(self):
        super(self.__class__, self).__init__()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_check_recipientBlacklist_normal(self):
        #print self.host
        cli = client.SesClient(self.host, self.ak, self.sk)
        email = 'wanglinqing2014@baidu.com'
        resp = cli.check_recipientblacklist(email)
        #print resp
        assert resp.status == 200, 'status is not 200'
        print resp.body
        #wanglinqing2014@baidu.com in blacklist
        assert resp.body['exist'] == False, 'email is in blacklist'
