#!/usr/bin/env python
#coding=utf8

import unittest
import time
from baidubce.services.sms import client
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


class TestSmsClientQueryReceiverNorQa(unittest.TestCase):
    data = [
            [0, '13811112222', 0],
         ]

    def setUp(self):
        self.sms = client.SmsClient(SMS_HOST, SMS_AK, SMS_SK)

    def tearDown(self):
        pass

    def test(self):
        for tag, phoneNumber, receivedToday in self.data:
            qResponse = self.sms.query_receiver(phoneNumber)
            #TODO
            self.assertEqual(200, qResponse.status)
            self.assertEqual(10000, qResponse.receiver_stat.maxReceivePerPhoneNumberDay)
            self.assertEqual(receivedToday, qResponse.receiver_stat.receivedToday)

if __name__ == '__main__':
    unittest.main()
