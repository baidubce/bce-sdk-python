#!/usr/bin/env python
#coding=utf8

import unittest
from baidubce.services.sms import client
from baidubce.services.sms.exception import ServerError
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


class TestSmsClientDeleteTemplateNorQa(unittest.TestCase):
    data = [
            ['x', 'y'],
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

    def testDeleteProcessingTemplate(self):
        for name, content in self.data:
            try:
                cResponse = self.sms.create_template(name, content)	#创建模板
                tId = cResponse.get_template_id()
                gResponse = self.sms.get_template(tId)
                self.assertEqual(tId, gResponse.template.templateId)	#确认模板创建成功
                dResponse = self.sms.delete_template(tId)		#删除模板
                self.assertEqual(200, dResponse.status)	#确认返回值正确
            except ServerError:
                print 'data prepare failed'
                self.tIdList.append(tId)

            #确认无法获取模板，证明模板已成功删除
            self.assertRaisesRegexp(ServerError, 'status=403, message=no records in database', 
                    self.sms.get_template, tId)

    def testDeleteValidTemplate(self):
        for name, content in self.data:
            try:
                cResponse = self.sms.create_template(name, content)	#创建模板
                tId = cResponse.get_template_id()
                self.sms.enable_template(tId)
                gResponse = self.sms.get_template(tId)
                self.assertEqual('VALID', gResponse.template.status)	#确认模板创建成功
                dResponse = self.sms.delete_template(tId)		#删除模板
                self.assertEqual(200, dResponse.status)	#确认返回值正确
            except ServerError:
                print 'data prepare failed'
                self.tIdList.append(tId)

            #确认无法获取模板，证明模板已成功删除
            self.assertRaisesRegexp(ServerError, 'status=403, message=no records in database', 
                    self.sms.get_template, tId)

    def testDeleteInvalidTemplate(self):
        pass	#TODO

if __name__ == '__main__':
    unittest.main()
