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


class TestSmsClientGetTemplateNorQa(unittest.TestCase):
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

    dataValidTemplate = [
            #单字符
            [0, 'x', 'y'],
         ]

    def setUp(self):
        self.sms = client.SmsClient(SMS_HOST, SMS_AK, SMS_SK)
        self.tIdList = []
        templates = self.sms.list_template().templates
        for tag, name, content in self.data:
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
            expCreateTime = time.mktime(time.localtime())
            expUpdateTime = expCreateTime
            cResponse = self.sms.create_template(name, content)
            tId = cResponse.get_template_id()
            self.tIdList.append(tId)
            gResponse = self.sms.get_template(tId)

            actCreateTime = time.mktime(time.strptime(gResponse.template.createTime, '%Y-%m-%dT%H:%M:%SZ'))
            actUpdateTime = time.mktime(time.strptime(gResponse.template.updateTime, '%Y-%m-%dT%H:%M:%SZ'))

            self.assertEqual(200, gResponse.status)
            self.assertEqual(name, gResponse.template.name)
            self.assertEqual(content, gResponse.template.content)
            self.assertEqual('PROCESSING', gResponse.template.status)
            self.assertTrue((actCreateTime - expCreateTime) < 3)
            self.assertTrue((actUpdateTime - expUpdateTime) < 3)

    def testValidTemplate(self):
        for tag, name, content in self.dataValidTemplate:
            print tag	#debug
            expCreateTime = time.mktime(time.localtime())
            cResponse = self.sms.create_template(name, content)
            tId = cResponse.get_template_id()
            self.tIdList.append(tId)

            time.sleep(4)
            expUpdateTime = time.mktime(time.localtime())
            self.sms.enable_template(tId)

            gResponse = self.sms.get_template(tId)

            actCreateTime = time.mktime(time.strptime(gResponse.template.createTime, '%Y-%m-%dT%H:%M:%SZ'))
            actUpdateTime = time.mktime(time.strptime(gResponse.template.updateTime, '%Y-%m-%dT%H:%M:%SZ'))

            self.assertEqual(200, gResponse.status)
            self.assertEqual(name, gResponse.template.name)
            self.assertEqual(content, gResponse.template.content)
            self.assertEqual('VALID', gResponse.template.status)
            self.assertTrue((actCreateTime - expCreateTime) < 3)
            self.assertTrue((actUpdateTime - expUpdateTime) < 3)

    def testInvalidTemplate(self):
        pass	#TODO

if __name__ == '__main__':
    unittest.main()
