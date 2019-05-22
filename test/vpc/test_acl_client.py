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
This module for acl client test.
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
from baidubce.services.vpc import acl_client

vpc_id = ''
subnetId = ''
HOST = b''
AK = b''
SK = b''
acl_id = ''


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.
    :return:
    :rtype string
    """
    return str(uuid.uuid4())


generate_client_token = generate_client_token_by_uuid


class TestAclClient(unittest.TestCase):
    """
    unit test
    """

    def setUp(self):
        """
        set up
        """
        config = BceClientConfiguration(
            credentials=BceCredentials(AK, SK), endpoint=HOST)
        self.the_client = acl_client.AclClient(config)

    def test_list_acl_entrys(self):
        """
        test case for test list acl entrys
        """
        print(self.the_client.list_acl_entrys(vpc_id))

    def test_create_acl(self):
        """
        test case for create acl
        """
        client_token = generate_client_token()
        rule_list = []
        acl_rule = {
            'subnetId': subnetId,
            'protocol': 'tcp',
            'sourceIpAddress': '1.1.1.1',
            'destinationIpAddress': '2.2.2.2',
            'sourcePort': '123',
            'destinationPort': '456',
            'position': 100,
            'direction': 'ingress',
            'action': 'deny'
        }
        rule_list.append(acl_rule)

        self.assertEqual(
            type(self.the_client.create_acl(rule_list,
                                            client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_list_subnet_acl(self):
        """
        test case for list subnet acl
        """
        print(self.the_client.list_subnet_acl(subnetId))

    def test_delete_acl(self):
        """
        test case for delete acl
        """
        client_token = generate_client_token()

        self.assertEqual(
            type(self.the_client.delete_acl(acl_id,
                                            client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_update_acl(self):
        """
        test case for update acl
        """
        client_token = generate_client_token()

        self.assertEqual(
            type(self.the_client.update_acl(acl_id,
                                            protocol=b'udp',
                                            source_ip_address=b'2.1.1.1',
                                            client_token=client_token)),
            baidubce.bce_response.BceResponse)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    #suite.addTest(TestAclClient("test_list_acl_entrys"))
    #suite.addTest(TestAclClient("test_create_acl"))
    #suite.addTest(TestAclClient("test_list_subnet_acl"))
    #suite.addTest(TestAclClient("test_delete_acl"))
    #suite.addTest(TestAclClient("test_update_acl"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
