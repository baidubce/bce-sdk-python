#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.

"""
Unit tests for template_client.
"""

import os
import sys
import unittest
import uuid

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')
if sys.version < '3':
    reload(sys)
    sys.setdefaultencoding('utf-8')

import baidubce
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.vpc import template_client
from baidubce.services.vpc import template_model

IP_SET_ID = b''
IP_GROUP_ID = b''


class TestTemplateClient(unittest.TestCase):
    """
    Test class for template sdk client
    """
    def setUp(self):
        """
        set up
        """
        HOST = b''
        AK = b''
        SK = b''

        config = BceClientConfiguration(
            credentials=BceCredentials(AK, SK), endpoint=HOST)
        self.client = template_client.TemplateClient(config)

    def tearDown(self):
        """
        tear down
        """
        self.client = None

    # ==================== IpSet 相关测试 ====================

    def test_create_ip_set(self):
        """
        test case for creating ip set
        """
        client_token = generate_client_token()
        name = 'test_ip_set_' + client_token
        ip_version = 'IPv4'
        ip_address_info = [
            template_model.TemplateIpAddressInfo(ip_address='192.168.11.0/24', description='test1'),
            template_model.TemplateIpAddressInfo(ip_address='192.168.12.0/24', description='test2'),
        ]
        description = 'test ip set description'
        self.assertEqual(
            type(self.client.create_ip_set(
                name=name,
                ip_version=ip_version,
                ip_address_info=ip_address_info,
                description=description,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_ip_set_without_description(self):
        """
        test case for creating ip set without optional description
        """
        client_token = generate_client_token()
        name = 'test_ip_set_no_desc_' + client_token
        ip_version = 'IPv6'
        ip_address_info = [
            template_model.TemplateIpAddressInfo(ip_address='2001:db8::/32', description='ipv6 test'),
        ]
        self.assertEqual(
            type(self.client.create_ip_set(
                name=name,
                ip_version=ip_version,
                ip_address_info=ip_address_info,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_add_ip_address_to_ip_set(self):
        """
        test case for adding ip address to ip set
        """
        client_token = generate_client_token()
        ip_address_info = [
            template_model.TemplateIpAddressInfo(ip_address='10.0.1.0/24', description='added ip'),
        ]
        self.assertEqual(
            type(self.client.add_ip_address_to_ip_set(
                ip_set_id=IP_SET_ID,
                ip_address_info=ip_address_info,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_delete_ip_address(self):
        """
        test case for deleting ip address from ip set
        """
        client_token = generate_client_token()
        ip_address = ['10.0.1.0/24']
        self.assertEqual(
            type(self.client.delete_ip_address(
                ip_set_id=IP_SET_ID,
                ip_address=ip_address,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_update_ip_set(self):
        """
        test case for updating ip set
        """
        new_name = 'test_ip_set_updated'
        new_description = 'updated description'
        self.assertEqual(
            type(self.client.update_ip_set(
                ip_set_id=IP_SET_ID,
                name=new_name,
                description=new_description)),
            baidubce.bce_response.BceResponse)

    def test_update_ip_set_partial(self):
        """
        test case for updating ip set with only name
        """
        self.assertEqual(
            type(self.client.update_ip_set(
                ip_set_id=IP_SET_ID,
                name='partial_update_name')),
            baidubce.bce_response.BceResponse)

    def test_list_ip_set(self):
        """
        test case for listing ip sets
        """
        print(self.client.list_ip_set())

    def test_list_ip_set_with_options(self):
        """
        test case for listing ip sets with filter options
        """
        print(self.client.list_ip_set(ip_version='IPv4', max_keys=10))

    def test_get_ip_set_detail(self):
        """
        test case for getting ip set detail
        """
        print(self.client.get_ip_set_detail(ip_set_id=IP_SET_ID))

    def test_delete_ip_set(self):
        """
        test case for deleting ip set
        """
        self.assertEqual(
            type(self.client.delete_ip_set(ip_set_id=IP_SET_ID)),
            baidubce.bce_response.BceResponse)

    # ==================== IpGroup 相关测试 ====================

    def test_create_ip_group(self):
        """
        test case for creating ip group
        """
        client_token = generate_client_token()
        name = 'test_ip_group_' + client_token
        ip_version = 'IPv4'
        ip_set_ids = [IP_SET_ID]
        description = 'test ip group description'
        self.assertEqual(
            type(self.client.create_ip_group(
                name=name,
                ip_version=ip_version,
                ip_set_ids=ip_set_ids,
                description=description,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_ip_group_without_description(self):
        """
        test case for creating ip group without optional description
        """
        client_token = generate_client_token()
        name = 'test_ip_group_no_desc_' + client_token
        ip_version = 'IPv4'
        ip_set_ids = [IP_SET_ID]
        self.assertEqual(
            type(self.client.create_ip_group(
                name=name,
                ip_version=ip_version,
                ip_set_ids=ip_set_ids,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_bind_ip_set(self):
        """
        test case for binding ip set to ip group
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.client.bind_ip_set(
                ip_group_id=IP_GROUP_ID,
                ip_set_ids=[IP_SET_ID],
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_unbind_ip_set(self):
        """
        test case for unbinding ip set from ip group
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.client.unbind_ip_set(
                ip_group_id=IP_GROUP_ID,
                ip_set_ids=[IP_SET_ID],
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_update_ip_group(self):
        """
        test case for updating ip group
        """
        new_name = 'test_ip_group_updated'
        new_description = 'updated ip group description'
        self.assertEqual(
            type(self.client.update_ip_group(
                ip_group_id=IP_GROUP_ID,
                name=new_name,
                description=new_description)),
            baidubce.bce_response.BceResponse)

    def test_update_ip_group_partial(self):
        """
        test case for updating ip group with only description
        """
        self.assertEqual(
            type(self.client.update_ip_group(
                ip_group_id=IP_GROUP_ID,
                description='only description updated')),
            baidubce.bce_response.BceResponse)

    def test_list_ip_group(self):
        """
        test case for listing ip groups
        """
        print(self.client.list_ip_group())

    def test_list_ip_group_with_options(self):
        """
        test case for listing ip groups with filter options
        """
        print(self.client.list_ip_group(ip_version='IPv4', max_keys=10))

    def test_get_ip_group_detail(self):
        """
        test case for getting ip group detail
        """
        print(self.client.get_ip_group_detail(ip_group_id=IP_GROUP_ID))

    def test_delete_ip_group(self):
        """
        test case for deleting ip group
        """
        self.assertEqual(
            type(self.client.delete_ip_group(ip_group_id=IP_GROUP_ID)),
            baidubce.bce_response.BceResponse)


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.

    :return:
    :rtype string
    """
    return str(uuid.uuid4())


generate_client_token = generate_client_token_by_uuid


if __name__ == '__main__':
    suite = unittest.TestSuite()
    # IpSet
    #suite.addTest(TestTemplateClient("test_create_ip_set"))
    #suite.addTest(TestTemplateClient("test_create_ip_set_without_description"))
    #suite.addTest(TestTemplateClient("test_add_ip_address_to_ip_set"))
    #suite.addTest(TestTemplateClient("test_delete_ip_address"))
    #suite.addTest(TestTemplateClient("test_update_ip_set"))
    #suite.addTest(TestTemplateClient("test_update_ip_set_partial"))
    #suite.addTest(TestTemplateClient("test_list_ip_set"))
    #suite.addTest(TestTemplateClient("test_list_ip_set_with_options"))
    #suite.addTest(TestTemplateClient("test_get_ip_set_detail"))
    #suite.addTest(TestTemplateClient("test_delete_ip_set"))
    # IpGroup
    #suite.addTest(TestTemplateClient("test_create_ip_group"))
    #suite.addTest(TestTemplateClient("test_create_ip_group_without_description"))
    #suite.addTest(TestTemplateClient("test_bind_ip_set"))
    #suite.addTest(TestTemplateClient("test_unbind_ip_set"))
    #suite.addTest(TestTemplateClient("test_update_ip_group"))
    #suite.addTest(TestTemplateClient("test_update_ip_group_partial"))
    #suite.addTest(TestTemplateClient("test_list_ip_group"))
    #suite.addTest(TestTemplateClient("test_list_ip_group_with_options"))
    #suite.addTest(TestTemplateClient("test_get_ip_group_detail"))
    #suite.addTest(TestTemplateClient("test_delete_ip_group"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
