#!/usr/bin/env python
#coding=utf8

import unittest
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


class TestSmsClientCreateTemplateNorQa(unittest.TestCase):
    data = [
            #单字符
            ['x', 'y'],
            #多字符
            ['x1', 'y1'],
            #最多字符
            ['x123456789x123456789x123456789x1', 'x123456789x123456789x123456789x123456789x123456789x123456789x123456789'],
            #中文字符
            ['x模板名', 'y模板内容'],
            #带变量的内容
            ['x2', 'y${yk1}y${yk2}'],
            #特殊字符
            ['x*', 'y*'],
         ]

    def setUp(self):
        self.sms = client.SmsClient(SMS_HOST, SMS_AK, SMS_SK)
        self.tIdList = []
        templates = self.sms.list_template().templates
        for name, content in self.data:
            if(name in templates):
                self.sms.delete_template(templates[name].templateId)

    def tearDown(self):
        for tId in self.tIdList:
            self.sms.delete_template(tId)

    def test(self):
        for name, content in self.data:
            cResponse = self.sms.create_template(name, content)
            tId = cResponse.get_template_id()
            self.tIdList.append(tId)
            gResponse = self.sms.get_template(tId)

            self.assertEqual(200, cResponse.status)
            self.assertEqual(name, gResponse.template.name)
            self.assertEqual(content, gResponse.template.content)

if __name__ == '__main__':
    unittest.main()
