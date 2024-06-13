#!/usr/bin/env python
# coding=utf8

import logging
import os
import sys
import unittest

import baidubce.services.sms.sms_client as sms
from QaConf import config1
from QaConf import config2
from baidubce.exception import BceHttpClientError

if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding('utf-8')

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

logging.basicConfig(level=logging.DEBUG, filename='./sms_sample.log', filemode='w')
LOG = logging.getLogger(__name__)


class TestSmsClientSendMessageNorQa(unittest.TestCase):

    def setUp(self):
        self.signature_id = 'sms-sign-PcsBjx12436'
        self.template_id = 'sms-tmpl-fGJBJe71978'
        self.sms_client1 = sms.SmsClient(config1)
        self.sms_client2 = sms.SmsClient(config2)

    def tearDown(self):
        pass

    def test_send_message(self):

        # 签名可用 模版可用
        response = self.sms_client1.send_message(signature_id=self.signature_id, template_id=self.template_id,
                                                 mobile='13800138000', content_var_dict={'content': "测试发送短信"})
        self.assertEqual('1000', response.code)

        # 签名可用 模版不可用
        try:
            self.sms_client1.send_message(signature_id="sms-sign", template_id=self.template_id, mobile='13800138000',
                                          content_var_dict={})
        except BceHttpClientError as e:
            self.assertIsNotNone(e)

        # 签名不可用 模版可用
        try:
            self.sms_client1.send_message(signature_id=self.signature_id, template_id="sms-tmpl", mobile='13800138000',
                                          content_var_dict={'content': "测试发送短信"})
        except BceHttpClientError as e:
            self.assertIsNotNone(e)
        # 签名不可用 模版不可用
        try:
            self.sms_client1.send_message(signature_id=self.signature_id, template_id=self.template_id,
                                          mobile='13800138000', content_var_dict={'code': "测试发送短信"})
        except BceHttpClientError as e:
            self.assertIsNotNone(e)

    def test_signature(self):

        # 创建成功
        response_create = self.sms_client2.create_signature(content="百度", content_type="Enterprise")
        signature_id = response_create.signature_id
        self.assertIsNotNone(signature_id)

        # 签名内容错误
        try:
            self.sms_client2.create_signature(content="百 度", content_type="Enterprise")
        except BceHttpClientError as e:
            self.assertIsNotNone(e)

        # 获取签名
        response_get = self.sms_client2.get_signature_detail(signature_id)
        self.assertEqual(signature_id, response_get.signature_id)

        # 更新签名
        self.sms_client2.update_signature(content="BaiduSms", content_type="Enterprise",
                                          country_type="DOMESTIC", signature_id=signature_id)
        response_get = self.sms_client2.get_signature_detail(signature_id)
        self.assertEqual("BaiduSms", response_get.content)

        # 删除签名
        self.sms_client2.delete_signature(signature_id)

        # 签名id错误
        try:
            self.sms_client2.delete_signature("sms-tmpl")
        except BceHttpClientError as e:
            self.assertIsNotNone(e)

    def test_template(self):

        # 创建成功
        response_create = self.sms_client2.create_template(name="百度短信", content="${content}", sms_type="normal",
                                                           country_type="GLOBAL", description="测试模板")
        template_id = response_create.template_id
        self.assertIsNotNone(template_id)

        # 国家类型错误
        try:
            self.sms_client2.create_template(name="百度短信", content="${content}", sms_type="normal",
                                             country_type="UNKNOWN", description="测试模板")
        except BceHttpClientError as e:
            self.assertIsNotNone(e)

        # 模板类型错误
        try:
            self.sms_client2.create_template(name="百度短信", content="${content}", sms_type="unknown",
                                             country_type="UNKNOWN", description="测试模板")
        except BceHttpClientError as e:
            self.assertIsNotNone(e)

        # 更新模板
        self.sms_client2.update_template(template_id=template_id, name="baidu sms", content="验证码${code}",
                                         sms_type="CommonNotice", country_type="DOMESTIC")
        # 获取模板
        response_get = self.sms_client2.get_template_detail(template_id=template_id)
        self.assertEqual("CommonNotice", response_get.sms_type)

        # 删除模板
        self.sms_client2.delete_template(template_id)

    def test_quota(self):

        # 获取配额信息
        response_get = self.sms_client2.query_quota_rate()
        self.assertIsNotNone(response_get)

        # 更新配额信息
        try:
            self.sms_client2.update_quota_rate(100, 100, 100, 100, 100)
        except BceHttpClientError as e:
            pass

    def test_black(self):
        # 创建手机号黑名单
        self.sms_client2.create_mobile_black("MerchantBlack", "17600000000",
                                             "DOMESTIC", sms_type="CommonNotice")
        self.sms_client2.create_mobile_black("MerchantBlack", "17600000000", "DOMESTIC")
        self.sms_client2.create_mobile_black("MerchantBlack", "+610490353986", "INTERNATIONAL")

        # 手机号查询
        blacklists = self.sms_client2.get_mobile_black(phone="17600000000", country_type="DOMESTIC")
        self.assertEqual(2, blacklists.total_count)
        blacklists2 = self.sms_client2.get_mobile_black(phone="+610490353986", country_type="INTERNATIONAL")
        self.assertEqual(1, blacklists2.total_count)

        # 手机号删除
        self.sms_client2.delete_mobile_black("17600000000")

        blacklists = self.sms_client2.get_mobile_black(phone="17600000000")
        self.assertEqual(0, blacklists.total_count)

    def test_statistics(self):
        # 获取统计信息 - 无数据，因此会有3个结果，所有数值为0
        response = self.sms_client2.list_statistics(
            start_time='2023-11-01',
            end_time='2023-11-02'
        )
        self.assertEqual(len(response.statistics_results), 3)
        print(response)

        # 获取统计信息 - 传入更多可选参数，例如签名
        response = self.sms_client2.list_statistics(
            start_time='2023-10-08',
            end_time='2023-10-09',
            signature_id='sms-sign-mock'
        )
        self.assertEqual(len(response.statistics_results), 3)

        # 获取统计信息 - 缺少必传参数，start_time
        try:
            self.sms_client2.list_statistics(
                end_time='2023-10-09',
                signature_id='sms-sign-mock'
            )
        except TypeError as e:
            self.assertEqual(type(e), TypeError)

        # 获取统计信息 - 时间参数格式错误
        try:
            self.sms_client2.list_statistics(
                start_time='2023-10-08 0',
                end_time='2023-10-09',
            )
        except BceHttpClientError as e:
            self.assertEqual(type(e), BceHttpClientError)

        # 查询时间早于1年前
        try:
            self.sms_client2.list_statistics(
                start_time='2022-10-08',
                end_time='2023-10-09',
            )
        except BceHttpClientError as e:
            self.assertEqual(type(e), BceHttpClientError)


if __name__ == '__main__':
    unittest.main()
