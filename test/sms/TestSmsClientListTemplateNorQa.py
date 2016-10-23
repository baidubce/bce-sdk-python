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


class TestSmsClientListTemplateNorQa(unittest.TestCase):
    data = [
            #单字符
            [0, 'x', 'y'],
            #name最多字符
            [1, 'x123456789x123456789x123456789x1', 'y'],
            #content最多字符
            [2, 'x2', 'x123456789x123456789x123456789x123456789x123456789x123456789x123456789'],
            #中文字符
            [3, 'x模板名', 'y模板内容'],
            #带变量的内容
            [4, 'x3', 'y${yk1}y${yk2}'],
            #特殊字符
            [5, 'x*', 'y*'],
         ]

    dataDeletedTemplate = [
                            [0, 'x', 'y'],
                        ]

    dataValidTemplate = [
                            [0, 'x', 'y'],
                        ]

    def setUp(self):
        self.sms = client.SmsClient(SMS_HOST, SMS_AK, SMS_SK)
        self.tIdList = []
        templates = self.sms.list_template().templates
        for tag, name, content in self.data:
            if(name in templates):
                self.sms.delete_template(templates[name].templateId)
        for tag, name, content in self.dataDeletedTemplate:
            if(name in templates):
                self.sms.delete_template(templates[name].templateId)
        for tag, name, content in self.dataValidTemplate:
            if(name in templates):
                self.sms.delete_template(templates[name].templateId)

    def tearDown(self):
        for tId in self.tIdList:
            self.sms.delete_template(tId)

    def test(self):
        for tag, name, content in self.data:
            print tag	#debug
            beforeLength = len(self.sms.list_template().templates)
            cResponse = self.sms.create_template(name, content)
            tId = cResponse.get_template_id()
            self.tIdList.append(tId)
            lResponse = self.sms.list_template()
            afterLength = len(lResponse.templates)

            self.assertEqual(200, lResponse.status)
            self.assertEqual(beforeLength + 1, afterLength)

    def testDeletedTemplate(self):
        for tag, name, content in self.dataDeletedTemplate:
            print tag	#debug
            beforeLength = len(self.sms.list_template().templates)
            cResponse = self.sms.create_template(name, content)
            tId = cResponse.get_template_id()
            self.sms.delete_template(tId)
            lResponse = self.sms.list_template()
            afterLength = len(lResponse.templates)

            self.assertEqual(200, lResponse.status)
            self.assertEqual(beforeLength, afterLength)

    def testValidTemplate(self):
        for tag, name, content in self.dataValidTemplate:
            print tag	#debug
            beforeLength = len(self.sms.list_template().templates)
            cResponse = self.sms.create_template(name, content)
            tId = cResponse.get_template_id()
            self.tIdList.append(tId)

            self.sms.enable_template(tId)

            lResponse = self.sms.list_template()
            afterLength = len(lResponse.templates)

            self.assertEqual(200, lResponse.status)
            self.assertEqual(beforeLength + 1, afterLength)

    def testInvalidTemplate(self):
        pass	#TODO

if __name__ == '__main__':
    unittest.main()
