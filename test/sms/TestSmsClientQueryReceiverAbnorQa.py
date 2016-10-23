#!/usr/bin/env python
#coding=utf8

import unittest
from baidubce.services.sms import client
from baidubce.services.sms.exception import * 
from QaConf import *
import logging
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


class TestSmsClientQueryReceiverAbnorQa(unittest.TestCase):
    data = [
            #phoneNumber为None
            [0, None, 'InvalidParam', 'err_message=phone_number empty'],
            #phoneNumber为空串
            [1, '', 'InvalidParam', 'err_message=phone_number empty'],
            #phoneNumber仅包含空白符
            [2, ' ', 'InvalidParam', 'err_message=phone_number empty'],
            #phoneNumber位数不足
            [3, '1', 'ServerError', 
                'status=403, message=parameter validator error: phoneNumber=1 is not \
                        a valid phone number'],
            #phoneNumber包含非数字字符
            [4, '1381111222x', 'ServerError', 
                'status=403, message=parameter validator error: phoneNumber=1381111222x \
                        is not a valid phone number'],
            #phoneNumber为逗号分隔的两个有效号码
            [5, '13811939405,13811939405', 'ServerError', 'status=403, \
                    message=parameter validator \
                    error: phoneNumber=13811939405,13811939405 is not a valid phone number'],
         ]

    def setUp(self):
        self.sms = client.SmsClient(SMS_HOST, SMS_AK, SMS_SK)

    def tearDown(self):
        pass

    def test(self):
        for tag, phoneNumber, exceptType, exceptMsg in self.data:
            print tag   #debug
            self.assertRaisesRegexp(eval(exceptType), exceptMsg, self.sms.query_receiver, phoneNumber)

if __name__ == '__main__':
    unittest.main()
