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


class TestSmsClientCreateTemplateAbnorQa(unittest.TestCase):
    data = [
            #name为None
            [0, None, 'y', 'InvalidParam', 'err_message=empty name'],
            #name为空串
            [1, '', 'y', 'InvalidParam', 'err_message=empty name'],
            #name仅包含空白符
            [2, ' ', 'y', 'InvalidParam', 'err_message=invalid name'],
            #name长度超限
            [3, 'x123456789x123456789x123456789x12', 'y', 'InvalidParam', \
                    'err_message=invalid name'],
            #content为None
            [4, 'x', None, 'InvalidParam', 'err_message=empty content'],
            #content为空串
            [5, 'x', '', 'InvalidParam', 'err_message=empty content'],
            #content仅包含空白符
            [6, 'x', ' ', 'InvalidParam', 'err_message=invalid content'],
            #content长度超限
            [7, 'x', 'x123456789x123456789x123456789x123456789x123456789x123456789x123456789x', 
                'InvalidParam', 'err_message=invalid content'],
         ]

    dataDuplicateName = [
                        [0, 'x', 'y', 'x', 'ServerError', 'status=400, message=\
                                template name exists'],
                        [1, 'x2', 'y', 'X2', 'ServerError', 'status=400, message=\
                                template name exists'],
                        ]

    def setUp(self):
        self.sms = client.SmsClient(SMS_HOST, SMS_AK, SMS_SK)
        self.tIdList = []
        templates = self.sms.list_template().templates
        for tag, name, content, anotherName, exceptType, exceptMsg in self.dataDuplicateName:
            if(name in templates):
                self.sms.delete_template(templates[name].templateId)

    def tearDown(self):
        for tId in self.tIdList:
            self.sms.delete_template(tId)

    def test(self):
        for tag, name, content, exceptType, exceptMsg in self.data:
            print "%s,%s,%s,%s,%s" % (tag, name, content, exceptType, exceptMsg)   #debug
            self.assertRaisesRegexp(eval(exceptType), exceptMsg, 
                    self.sms.create_template, name, content)

    def testDuplicateName(self):
        for tag, name, content, anotherName, exceptType, exceptMsg in self.dataDuplicateName:
            print tag   #debug
            cResponse = self.sms.create_template(name, content)
            tId = cResponse.get_template_id()
            self.tIdList.append(tId)
            #self.assertRaisesRegexp(eval(exceptType), exceptMsg, self.sms.create_template, anotherName, content)
            self.assertRaises(eval(exceptType), self.sms.create_template, anotherName, content)

if __name__ == '__main__':
    unittest.main()
