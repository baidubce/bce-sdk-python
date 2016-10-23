#!/usr/bin/env python
#coding=utf8

import unittest
from baidubce.services.sms import client
from QaConf import *
import logging
import random
import string
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


class TestSmsClientSendMessageNorQa(unittest.TestCase):
    data = [
            #模板带1个变量
            [0, 'x', 'python-sms-sdk-test(1个变量):${var1}', ['13811939405'], {"var1": "参数1"}, 1],
            #模板带2个变量
            [1, 'x1', 'python-sms-sdk-test(2个变量):${var1};${var2}', ['13811939405'], {"var1": "参数1", "var2": "参数2"}, 1],
            #模板带0个变量
            [2, 'x2', 'python-sms-sdk-test:无变量', ['13811939405'], {}, 1],
            #2个接收者
            [3, 'x3', 'python-sms-sdk-test(接收2遍):无变量', ['13811939405', '13811939405'], {}, 2],
            #contentVar中含空白符
            [4, 'x4', 'python-sms-sdk-test(contentVar含空白符):无变量', ['13811939405'], {}, 1],
            #模板不含变量，contentVar提供多余变量值
            [5, 'x5', 'python-sms-sdk-test(contentVar提供多余变量):无变量', ['13811939405'], {"var1": "参数1"}, 1],
            #contentVar最大长度
            [6, 'x6', 'python-sms-sdk-test(contentVar最大长度):${var1}', ['13811939405'], {"var1": "x" * 173 + "e"}, 1],
         ]

    def setUp(self):
        self.sms = client.SmsClient(SMS_HOST, SMS_AK, SMS_SK)
        self.tIdList = []
        templates = self.sms.list_template().templates
        for tag, name, content, receiver, contentMap, sendCount in self.data:
            if(name in templates):
                self.sms.delete_template(templates[name].templateId)

    def tearDown(self):
        for tId in self.tIdList:
            self.sms.delete_template(tId)

    def test(self):
        for tag, name, content, receiver, contentMap, sendCount in self.data:
            print tag	#debug
            cResponse = self.sms.create_template(name, content)
            tId = cResponse.get_template_id()
            self.tIdList.append(tId)

            self.sms.enable_template(tId)

            sResponse = self.sms.send_message(tId, receiver, contentMap)

            self.assertEqual(200, sResponse.status)
            self.assertIsNotNone(sResponse.send_stat.messageId)
            self.assertEqual(sendCount, sResponse.send_stat.sendStat.sendCount)
            self.assertEqual(sendCount, sResponse.send_stat.sendStat.successCount)
            self.assertListEqual([], sResponse.send_stat.sendStat.failList)

if __name__ == '__main__':
    unittest.main()
