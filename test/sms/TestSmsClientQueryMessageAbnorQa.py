#!/usr/bin/env python
#coding=utf8

import unittest
from baidubce.services.sms import client
from baidubce.services.sms.exception import *
from baidubce.exception import *
from QaConf import *
import logging
import random
import string
import time
import sys 
reload(sys)
sys.setdefaultencoding('utf8')

__author__ = 'zhangguiying01'

logger = logging.getLogger("baidubce.services.bos.client")
fh = logging.FileHandler("test_client.log")
fh.setLevel(logging.ERROR)

formatter = logging.Formatter(
        fmt="%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s",
            datefmt="%m-%d %H:%M:%S")
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)


class TestSmsClientQueryMessageAbnorQa(unittest.TestCase):
    data = [
            #messageId为None
            [0, None, 'InvalidParam', 'err_message=invalid message_id'],
            #messageId为空串
            [1, '', 'InvalidParam', 'err_message=invalid message_id'],
            #messageId仅包含空白符
            [2, ' ', 'RequestFailed', 'status=400, message=messageId is null or empty'],
            #messageId为不存在的id
            [3, 'notExistIdxxxx', 'RequestFailed', 'status=400, message=no record found'],
         ]

    def setUp(self):
        self.sms = client.SmsClient(SMS_HOST, SMS_AK, SMS_SK)

    def tearDown(self):
        pass

    def test(self):
        for tag, mId, exceptType, exceptMsg in self.data:
            print tag	#debug
            self.assertRaisesRegexp(eval(exceptType), exceptMsg, self.sms.query_message, mId)

if __name__ == '__main__':
    unittest.main()
