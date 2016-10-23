#!/usr/bin/env python

"""
@author wanglinqing01@baidu.com
@date 2014/10/08
@brief get quota
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


class TestGetQuota(bes_base_case.BaseTest):
    def __init__(self):
        super(self.__class__, self).__init__()

    def setUp(self):
        time.sleep(1)

    def tearDown(self):
        pass

    def test_get_quota_normal(self):
        #get quota
        cli = client.SesClient(self.host, self.ak, self.sk)
        resp = cli.get_quota()
        print resp.__str__()
        assert resp.status == 200, 'status is not 200'
        maxPerDay = resp.body['maxPerDay']
        maxPerSecond = resp.body['maxPerSecond']
        usedToday = resp.body['usedToday']

        #send email
        email = 'wanglinqing01@baidu.com'
        resp = cli.send_mail(mail_from=email, to_addr=['wanglinqing01@baidu.com'], subject="send email", text="ses python sdk send email")
        assert resp.status == 200, 'status is not 200'

        #get quota
        resp = cli.get_quota()
        assert resp.status == 200, 'status is not 200'
        assert maxPerDay == resp.body['maxPerDay']
        assert maxPerSecond == resp.body['maxPerSecond']
        new_usedToday = int(usedToday) + 1
        assert str(new_usedToday) == resp.body['usedToday']
