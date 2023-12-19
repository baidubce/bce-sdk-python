# -*- coding: utf-8 -*-

# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""
This module for test.
"""

import os
import sys
import unittest
import uuid
import json

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    import unittest.mock as mock
else:
    import mock as mock

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.eni import eni_client
from baidubce.services.eni import eni_model


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.
    :return:
    :rtype string
    """
    return str(uuid.uuid4())


generate_client_token = generate_client_token_by_uuid

class MockHttpResponse(object):
    """
    Mock HttpResponse
    """

    def __init__(self, status, result=None, header_list=None):
        self.status = status
        self.result = result
        self.header_list = header_list

    def read(self):
        """
        mock HttpResponse.read()

        :return: self.content
        """
        return self.result

    def getheaders(self):
        """
        mock HttpResponse.getheaders()

        :return: self.header_list
        """
        return self.header_list

    def close(self):
        """
        mock HttpResponse.close()
        """
        return

def mock_send_http_request():
    mock_http_response = MockHttpResponse(
            200,
            result=json.dumps({}),
            header_list=[
                ('x-bce-request-id', '7869616F-7A68-6977-656E-406261696475'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
    send_http_request = mock.Mock(return_value=mock_http_response)
    return send_http_request

class TestEniClient(unittest.TestCase):
    """
    unit test
    """
    def setUp(self):
        """
        set up
        """
        HOST = b'host'
        AK = b'ak'
        SK = b'sk'
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
        self.the_client = eni_client.EniClient(config)

    def test_create_eni(self):
        """
        test case for create_eni
        """
        self.the_client._send_request = mock_send_http_request()
        eni_ip_list = [eni_model.EniIPSet(public_ip="", private_ip="10.0.1.115", primary=True), 
                       eni_model.EniIPSet()]
        res = self.the_client.create_eni(name="eni-1", subnet_id="sbn-d63m7t0bbwt5", 
                                         security_group_ids=["g-92600fd1grhr"],
                                         eni_ip_address_list=eni_ip_list)  # 创建eni
        self.assertEqual(res.status, 200)

    def test_delete_eni(self):
        """
        test case for create_eni
        """
        self.the_client._send_request = mock_send_http_request()
        res = self.the_client.delete_eni(eni_id="eni-id-1")  # 删除eni
        self.assertEqual(res.status, 200)

    def test_update_eni(self):
        """
        test case for update_eni
        """
        self.the_client._send_request = mock_send_http_request()
        res = self.the_client.update_eni(eni_id="eni-id-1", name="eni-update-1", 
                                         description="update eni test")  # 更新eni
        self.assertEqual(res.status, 200)

    def test_list_eni(self):
        """
        test case for list_eni
        """
        self.the_client._send_request = mock_send_http_request()
        res = self.the_client.list_eni(vpc_id="vpc-id-1", instance_id="vm-id-1", name="eni-1", 
                                       private_ip_address_list=["10.0.1.115", "10.0.1.116"], 
                                       marker="eni-id-1", max_keys=2)  # 查询弹性网卡列表
        self.assertEqual(res.status, 200)

    def test_add_private_ip(self):
        """
        test case for add_private_ip
        """
        self.the_client._send_request = mock_send_http_request()
        # 增加弹性网卡内网IP
        res = self.the_client.add_private_ip(eni_id="eni-id-1", 
                                             is_ipv6=True, private_ip_address="240c:4081:8005:5e04::9")
        self.assertEqual(res.status, 200)

    def test_delete_private_ip(self):
        """
        test case for delete_private_ip
        """
        self.the_client._send_request = mock_send_http_request()
        # 删除弹性网卡内网IP
        res = self.the_client.delete_private_ip(eni_id="eni-id-1", 
                                                private_ip_address="240c:4081:8005:5e04::8")
        self.assertEqual(res.status, 200)

    def test_get_eni_details(self):
        """
        test case for get_eni_details
        """
        self.the_client._send_request = mock_send_http_request()
        res = self.the_client.get_eni_details(eni_id="eni-7bqg7jf0m88f")  # 查询指定的弹性网卡
        self.assertEqual(res.status, 200)

    def test_attach_eni_instance(self):
        """
        test case for attach_eni_instance
        """
        self.the_client._send_request = mock_send_http_request()
        # 弹性网卡挂载云主机
        res = self.the_client.attach_eni_instance(eni_id="eni-7bqg7jf0m88f", instance_id="i-Dqf1k9ul")
        self.assertEqual(res.status, 200)

    def test_detach_eni_instance(self):
        """
        test case for detach_eni_instance
        """
        self.the_client._send_request = mock_send_http_request()
        # 弹性网卡卸载云主机
        res = self.the_client.detach_eni_instance(eni_id="eni-7bqg7jf0m88f", instance_id="i-Dqf1k9ul")
        self.assertEqual(res.status, 200)

    def test_update_eni_security_group(self):
        """
        test case for update_eni_security_group
        """
        self.the_client._send_request = mock_send_http_request()
        # 弹性网卡更新普通安全组
        res = self.the_client.update_eni_security_group(eni_id="eni-7bqg7jf0m88f", 
                                                        security_group_ids=["g-jpppuref4vbh", "g-f8u628jzeq84"])
        self.assertEqual(res.status, 200)

    def test_update_eni_enterprise_security_group(self):
        """
        test case for update_eni_enterprise_security_group
        """
        self.the_client._send_request = mock_send_http_request()
        # 弹性网卡更新企业安全组
        res = self.the_client.update_eni_enterprise_security_group(
            eni_id="eni-7bqg7jf0m88f", 
            enterprise_security_group_ids=["esg-1atxb1iqd1e2"])
        self.assertEqual(res.status, 200)

    def test_batch_add_private_ip(self):
        """
        test case for attach_eni_instance
        """
        self.the_client._send_request = mock_send_http_request()
        # 批量增加弹性网卡内网IP
        res = self.the_client.batch_add_private_ip(eni_id="eni-7bqg7jf0m88f", 
                                                   is_ipv6=True, 
                                                   private_ip_address_list=["240c:4081:8005:5e04::0a", 
                                                                            "240c:4081:8005:5e04::0b"])
        self.assertEqual(res.status, 200)

    def test_batch_delete_private_ip(self):
        """
        test case for batch_delete_private_ip
        """
        self.the_client._send_request = mock_send_http_request()
        # 批量删除弹性网卡内网IP
        res = self.the_client.batch_delete_private_ip(eni_id="eni-7bqg7jf0m88f", 
                                                       private_ip_address_list=["240c:4081:8005:5e04::0a", 
                                                                                "240c:4081:8005:5e04::0b"])
        self.assertEqual(res.status, 200)

    def test_get_eni_status(self):
        """
        test case for get_eni_status
        """
        self.the_client._send_request = mock_send_http_request()
        res = self.the_client.get_eni_status(eni_id="eni-7bqg7jf0m88f")  # 查询弹性网卡状态 
        self.assertEqual(res.status, 200)

    def test_bind_eni_public_ip(self):
        """
        test case for bind_eni_public_ip
        """
        self.the_client._send_request = mock_send_http_request()
        res = self.the_client.bind_eni_public_ip(eni_id="eni-7bqg7jf0m88f", privat_ip_address="10.0.1.5", 
                                                  public_ip_address="120.48.142.121")  # 弹性网卡绑定EIP
        self.assertEqual(res.status, 200)

    def test_unbind_eni_public_ip(self):
        """
        test case for unbind_eni_public_ip
        """
        self.the_client._send_request = mock_send_http_request()
        # 弹性网卡解绑EIP
        res = self.the_client.unbind_eni_public_ip(eni_id="eni-7bqg7jf0m88f", public_ip_address="120.48.142.121")
        self.assertEqual(res.status, 200)

if __name__ == "__main__":
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(TestEniClient("test_update_eni"))
    
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

