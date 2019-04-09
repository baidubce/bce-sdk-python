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
from baidubce.services.subnet import subnet_client

if sys.version < '3':
    reload(sys)
    sys.setdefaultencoding('utf-8')

# config parameters
vpc_id = 'vpc-51csm6rxs9mg'
subnet_id = 'sbn-h2k40x2uw7cn'


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.
    :return:
    :rtype string
    """
    return str(uuid.uuid4())


generate_client_token = generate_client_token_by_uuid


class TestSubnetClient(unittest.TestCase):
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
        self.the_client = subnet_client.SubnetClient(config)

    def test_create_subnet(self):
        """
        test case for create_subnet
        """
        client_token = generate_client_token()
        subnet_name = 'test_subnet_name1' + client_token
        subnet_cidr = '192.168.0.64/26'
        self.assertEqual(
            type(self.the_client.create_subnet(subnet_name,
                                            'cn-bj-a',
                                            subnet_cidr,
                                            vpc_id,
                                            client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_list_subnets(self):
        """
        test case for list_subnets
        """
        print(self.the_client.list_subnets())

    def test_get_subnet(self):
        """
        test case for get_subnet
        """
        self.assertEqual(
            type(self.the_client.get_subnet(subnet_id)),
            baidubce.bce_response.BceResponse)

    def test_delete_subnet(self):
        """
        test case for delete_subnet
        """
        self.assertEqual(
            type(self.the_client.delete_subnet(subnet_id)),
            baidubce.bce_response.BceResponse)

    def test_update_subnet(self):
        """
        test case for delete_subnet
        """
        self.assertEqual(
            type(self.the_client.update_subnet(subnet_id, 'test_update_name1',
                                               'test_update_description1')),
            baidubce.bce_response.BceResponse)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(TestSubnetClient("test_create_subnet"))
    # suite.addTest(TestSubnetClient("test_list_subnets"))
    # suite.addTest(TestSubnetClient("test_get_subnet"))
    # suite.addTest(TestSubnetClient("test_delete_subnet"))
    suite.addTest(TestSubnetClient("test_update_subnet"))
    runner = unittest.TextTestRunner()
    runner.run(suite)


