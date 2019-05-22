#!/usr/bin/env python
#coding=utf8

import unittest
from baidubce.services.sms import sms_client as sms
from baidubce.exception import BceServerError
from baidubce.exception import BceHttpClientError
from QaConf import *
import sys
import logging
import os


if sys.version_info[0] == 2 :
    reload(sys)
    sys.setdefaultencoding('utf-8')

__author__ = 'chsun'

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

import QaConf
from baidubce.services.sms import sms_client as sms
from baidubce import exception as ex


logging.basicConfig(level=logging.DEBUG, filename='./sms_sample.log', filemode='w')
LOG = logging.getLogger(__name__)
CONF = QaConf



class TestSmsClientSendMessageNorQa(unittest.TestCase):

    def setUp(self):
        self.sms = sms.SmsClient(CONF.config)
        # 签名
        self.invoke_id_valid = 'y2W4LRun-9sMD-MeGd'
        self.invoke_id_inValid = 'not-ready-invoke-id'
        # 模版
        self.template_valid = 'smsTpl:78d20e6c-201c-4f97-b57b-240e9dc7d831'
        self.template_inValid = 'smsTpl:ae63a600-1474-4d40-b8d8-9ed9f924bf3b'


    def tearDown(self):
        pass

    def test(self):
        # 签名可用 模版可用
        sendResponse = self.sms.send_message_2(self.invoke_id_valid,self.template_valid,'13261559193',{'code': "测试发送短信"})
        self.assertEqual('1000', sendResponse.code)
        # 签名可用 模版不可用
        try:
            sendResponse = self.sms.send_message_2(self.invoke_id_valid,self.template_inValid,'13261559193',{})
        except BceHttpClientError as e:
            self.assertEqual('模板不可用', e.last_error.args[0])
        # 签名不可用 模版可用
        try:
            sendResponse = self.sms.send_message_2(self.invoke_id_inValid,self.template_valid,'13261559193',{'code': "测试发送短信"})
        except BceHttpClientError as e:
            self.assertEqual('请求参数不正确', e.last_error.args[0])
        # 签名不可用 模版不可用
        try:
            sendResponse = self.sms.send_message_2(self.invoke_id_inValid,self.template_inValid,'13261559193',{'code': "测试发送短信"})
        except BceHttpClientError as e:
            self.assertEqual('请求参数不正确', e.last_error.args[0])

if __name__ == '__main__':
    unittest.main()
