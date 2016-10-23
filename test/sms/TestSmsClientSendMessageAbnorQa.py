#!/usr/bin/env python
#coding=utf8

import unittest
from baidubce.services.sms import client
from baidubce.services.sms.exception import *
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


class TestSmsClientSendMessageAbnorQa(unittest.TestCase):
    data = [
            #templateId为None
            [0, None, ['13811939405'], {}, 'InvalidParam', 'err_message=invalid template_id'],
            #templateId为空串
            [1, '', ['13811939405'], {}, 'InvalidParam', 'err_message=invalid template_id'],
            #templateId仅包含空白符
            [2, ' ', ['13811939405'], {}, 'ServerError', 
                'status=403, message=parameter:smsTplId can not be empty'],
            #templateId不存在
            [3, 'smsTpl:notExistId944df8a9833153babc5930', ['13811939405'], {}, 'ServerError', 
                'status=403, message=no records in database'],
         ]

    dataProcessingTemplate = [
            #模板为PROCESSING状态
            [0, 'x', 'y', ['13811939405'], {}, 'ServerError', 
                'template is deleted or in process or invalid'],
         ]

    dataDeletedTemplate = [
            #模板已删除
            [0, 'x', 'y', ['13811939405'], {}, 
                'ServerError', 'status=403, message=no records in database'],
         ]

    dataReceiverContentMap = [
            #receiver为None
            [0, 'x', 'y', None, {}, 'InvalidParam', 'err_message=invalid receiver'],
            #receiver为空列表
            [1, 'x1', 'y', [], {}, 'InvalidParam', 'err_message=invalid receiver'],
            #receiver为空串
            [2, 'x2', 'y', [''], {}, 'ServerError', 'status=403, \
                    message=parameter validator error: receiver= is not a valid phone number'],
            #receiver仅包含空白符
            [3, 'x3', 'y', [' '], {}, 'ServerError', 'status=403, \
                    message=parameter validator error: receiver=  is not a valid phone number'],
            #receiver包含非数字字符
            [4, 'x4', 'y', ['1381111222x'], {}, 'ServerError', 'status=403, \
                    message=parameter validator error: \
                    receiver=1381111222x is not a valid phone number'],
            #receiver位数不足11位
            [5, 'x5', 'y', ['1'], {}, 'ServerError', 'status=403, \
                    message=parameter validator error: receiver=1 is not a valid phone number'],
            #部分receiver位数不足11位
            [6, 'x6', 'y', ['13811939405', '1'], {}, 'ServerError', 'status=403, \
                    message=parameter validator error: receiver=1 is not a valid phone number'],
            #contentMap为None
            [7, 'x7', 'y', ['13811939405'], None, 'InvalidParam', 'err_message=invalid content_map'],
            #contentMap不符合json格式
            [8, 'x8', 'y', ['13811939405'], {'zzz'}, 'TypeError', "not JSON serializable"],
            #模板1个变量，contentMap 0个变量值
            [9, 'x9', 'python-sms-sdk-test(1个变量):${var1}', ['13811939405'], {}, 'ServerError',
                    'status=403, message=var map not match template'],
            #模板2个变量，contentMap 1个变量值
            [10, 'x10', 'python-sms-sdk-test(2个变量):${var1};${var2}', ['13811939405'], 
                {"var1": "参数1"}, 'ServerError', 'status=403, message=var map not match template'],
            #模板1个变量，contentMap长度超限
            [11, 'x11', 'python-sms-sdk-test(1个变量):${var1}', ['13811939405'], {"var1": "x" * 185},
                    'ServerError', 
                    "status=500, message=message's content is too large, not allow to > 210 chars"],
         ]

    def setUp(self):
        self.sms = client.SmsClient(SMS_HOST, SMS_AK, SMS_SK)
        self.tIdList = []
        templates = self.sms.list_template().templates
        for tag, name, content, receiver, contentMap, exceptType, exceptMsg in self.dataProcessingTemplate:
            if(name in templates):
                self.sms.delete_template(templates[name].templateId)
        for tag, name, content, receiver, contentMap, exceptType, exceptMsg in self.dataDeletedTemplate:
            if(name in templates):
                self.sms.delete_template(templates[name].templateId)
        for tag, name, content, receiver, contentMap, exceptType, exceptMsg in self.dataReceiverContentMap:
            if(name in templates):
                self.sms.delete_template(templates[name].templateId)

    def tearDown(self):
        for tId in self.tIdList:
            self.sms.delete_template(tId)

    def test(self):
        for tag, tId, receiver, contentMap, exceptType, exceptMsg in self.data:
            print tag	#debug
            self.assertRaisesRegexp(eval(exceptType), exceptMsg, self.sms.send_message, tId, receiver, contentMap)

    def testProcessingTemplate(self):
        for tag, name, content, receiver, contentMap, exceptType, exceptMsg in self.dataProcessingTemplate:
            print tag	#debug
            cResponse = self.sms.create_template(name, content)
            tId = cResponse.get_template_id()
            self.tIdList.append(tId)

            self.assertRaisesRegexp(eval(exceptType), exceptMsg, self.sms.send_message, tId, receiver, contentMap)

    def testDeletedTemplate(self):
        for tag, name, content, receiver, contentMap, exceptType, exceptMsg in self.dataDeletedTemplate:
            print tag	#debug
            cResponse = self.sms.create_template(name, content)
            tId = cResponse.get_template_id()

            self.sms.delete_template(tId)

            self.assertRaisesRegexp(eval(exceptType), exceptMsg, self.sms.send_message, tId, receiver, contentMap)

    def testInvalidTemplate(self):
        pass	#TODO

    def testReceiverContentMap(self):
        for tag, name, content, receiver, contentMap, exceptType, exceptMsg in self.dataReceiverContentMap:
            print tag	#debug
            cResponse = self.sms.create_template(name, content)
            tId = cResponse.get_template_id()
            self.tIdList.append(tId)

            self.sms.enable_template(tId)

            self.assertRaisesRegexp(eval(exceptType), exceptMsg, self.sms.send_message, tId, receiver, contentMap)

if __name__ == '__main__':
    unittest.main()
