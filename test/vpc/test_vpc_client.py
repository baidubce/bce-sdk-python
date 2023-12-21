# -*- coding: utf-8 -*-

# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
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

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

import baidubce
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.vpc import vpc_client

if sys.version < '3':
    reload(sys)
    sys.setdefaultencoding('utf-8')

# config parameters
vpc_id = 'vpc-51csm6rxs9mg'


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.
    :return:
    :rtype string
    """
    return str(uuid.uuid4())


generate_client_token = generate_client_token_by_uuid


class TestVpcClient(unittest.TestCase):
    """
    unit test
    """
    def setUp(self):
        """
        set up
        """
        HOST = b'bcc.bj.baidubce.com'
        AK = b''
        SK = b''
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
        self.the_client = vpc_client.VpcClient(config)

    def test_create_vpc(self):
        """
        test case for create_vpc
        """
        client_token = generate_client_token()
        vpc_name = 'test_vpc_name' + client_token
        vpc_cidr = '192.168.240.0/20'
        description = 'test_vpc_descrition' + client_token
        res = self.the_client.create_vpc(vpc_name,
                                            vpc_cidr,
                                            description,
                                            client_token=client_token)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_list_vpcs(self):
        """
        test case for list_vpcs
        """
        res = self.the_client.list_vpcs()
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_get_vpc(self):
        """
        test case for get_vpc
        """
        res = self.the_client.get_vpc(vpc_id)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_delete_vpc(self):
        """
        test case for delete_vpc
        """
        res = self.the_client.delete_vpc(vpc_id)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_update_vpc(self):
        """
        test case for delete_vpc
        """
        res = self.the_client.update_vpc(vpc_id, 'test_update_name', 'test_update_description')
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_get_vpc_ip(self):
        """
        test case for get private ip address info
        """
        res1 = self.the_client.get_private_ip_address_info(vpc_id,
                                                             private_ip_addresses=["192.168.240.3", "192.168.240.5"])
        self.assertEqual(type(res1), baidubce.bce_response.BceResponse)
        
        res2 = self.the_client.get_private_ip_address_info(vpc_id, private_ip_addresses=["192.168.240.3"])
        self.assertEqual(type(res2), baidubce.bce_response.BceResponse)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(TestVpcClient("test_create_vpc"))
    # suite.addTest(TestVpcClient("test_list_vpcs"))
    # suite.addTest(TestVpcClient("test_get_vpc"))
    # suite.addTest(TestVpcClient("test_delete_vpc"))
    suite.addTest(TestVpcClient("test_update_vpc"))
    runner = unittest.TextTestRunner()
    runner.run(suite)

