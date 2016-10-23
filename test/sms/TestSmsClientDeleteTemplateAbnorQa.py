#!/usr/bin/env python
#coding=utf8

import unittest
from baidubce.services.sms import client
from baidubce.services.sms.exception import * 
#from baidubce.exception import *
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


class TestSmsClientDeleteTemplateAbnorQa(unittest.TestCase):
    data = [
            #templateId为None
            [0, None, 'InvalidParam', 'err_message=invalid template_id'],
            #templateId为空串
            [1, '', 'InvalidParam', 'err_message=invalid template_id'],
            #templateId仅包含空白符
            [2, ' ', 'InvalidParam', 'err_message=invalid template_id'],
            #不存在的templateId
            [3, 'smsTpl:notExistId944df8a9833153babc5930', 'ServerError', 
                'status=403, message=template does not exist'],
         ]

    dataDeletedTemplate = [
                        [0, 'x', 'y', 'ServerError', 'status=403, message=template does not exist'],
                        ]

    def setUp(self):
        self.sms = client.SmsClient(SMS_HOST, SMS_AK, SMS_SK)
        self.tIdList = []
        templates = self.sms.list_template().templates
        for tag, name, content, exceptType, exceptMsg in self.dataDeletedTemplate:
            if(name in templates):
                self.sms.delete_template(templates[name].templateId)

    def tearDown(self):
        for tId in self.tIdList:
            self.sms.delete_template(tId)

    def test(self):
        for tag, tId, exceptType, exceptMsg in self.data:
            print tag   #debug
            self.assertRaisesRegexp(eval(exceptType), exceptMsg, self.sms.delete_template, tId)

    def testDeletedTemplate(self):
        for tag, name, content, exceptType, exceptMsg in self.dataDeletedTemplate:
            tId = None
            try:
                print tag   #debug
                cResponse = self.sms.create_template(name, content)
                tId = cResponse.get_template_id()
                dResponse = self.sms.delete_template(tId)
                self.assertEqual(200, dResponse.status)
            except ServerError as e:
                print 'data prepare faild'
                print e
                self.tIdList.append(tId)
            self.assertRaisesRegexp(eval(exceptType), exceptMsg, self.sms.delete_template, tId)

if __name__ == '__main__':
    unittest.main()
