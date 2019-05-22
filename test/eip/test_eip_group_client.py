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
Unit tests for eip_group_client.
"""

import unittest
import uuid

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.eip import eip_group_client
from baidubce.services.eip import eip_group_model

EIP_GRP_ID = ''
EIP_GRP_NAME = ''
EIP_GROUP_STATUS = ''
MARKER = ''
MAX_KEYS = 500

pre_paid_billing = eip_group_model.Billing('Prepaid')


class TestEipGroupClient(unittest.TestCase):
    """
    Test class for eip group sdk client
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
        self.client = eip_group_client.EipGroupClient(config)

    def tearDown(self):
        """
        tear down
        """
        self.client = None

    def test_create_eip_group_without_name(self):
        """
        test case for creating EIP group without name
        """
        client_token = generate_client_token()
        self.client.create_eip_group(client_token=client_token,
                                     eip_count=2, bandwidth_in_mbps=10,
                                     billing=pre_paid_billing,
                                     name=None, config=None)

    def test_create_eip_group_with_name(self):
        """
        test case for creating EIP group without name
        """
        name = 'test_eip_group'
        self.client.create_eip_group(eip_count=2,
                                     bandwidth_in_mbps=10,
                                     name=name, config=None)

    def test_list_eip_groups(self):
        """
        test case for listing EIP groups
        """
        print((self.client.list_eip_groups(max_keys=1)))

    def test_list_eip_groups_with_detailed_options(self):
        """
        test case for listing EIP group with detailed options
        """
        print((self.client.list_eip_groups(id=EIP_GRP_ID, name=EIP_GRP_NAME,
                                           status=EIP_GROUP_STATUS,
                                           marker=MARKER,
                                           max_keys=MAX_KEYS)))

    def test_get_eip_group(self):
        """
        test case for getting EIP Group details
        """
        print((self.client.get_eip_group(id=EIP_GRP_ID)))

    def test_update_eip_group(self):
        """
        test case for updating EIP group name
        """
        name = 'test_eip_group_new'
        self.client.update_eip_group(id=EIP_GRP_ID, name=name)

    def test_resize_eip_group_bandwidth(self):
        """
        test case for scaling EIP group bandwidth
        """
        self.client.resize_eip_group_bandwidth(id=EIP_GRP_ID,
                                               bandwidth_in_mbps=40)

    def test_resize_eip_group_count(self):
        """
        test case for scaling EIP group count
        """
        client_token = generate_client_token()
        self.client.resize_eip_group_count(id=EIP_GRP_ID,
                                           client_token=client_token,
                                           eip_add_count=1)

    def test_purchase_reserved_eip_group(self):
        """
        test case for renewing EIP group with prepaid billing
        """
        client_token = generate_client_token()
        self.client.purchase_reserved_eip_group(
            id=EIP_GRP_ID, client_token=client_token)


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

    # suite.addTest(TestEipGroupClient("test_create_eip_group_without_name"))
    # suite.addTest(TestEipGroupClient("test_create_eip_group_with_name"))
    # suite.addTest(TestEipGroupClient("test_list_eip_groups"))
    # suite.addTest(TestEipGroupClient("test_list_eip_groups_with_detailed_options"))
    # suite.addTest(TestEipGroupClient("test_get_eip_group"))
    # suite.addTest(TestEipGroupClient("test_update_eip_group"))
    # suite.addTest(TestEipGroupClient("test_resize_eip_group_bandwidth"))
    # suite.addTest(TestEipGroupClient("test_resize_eip_group_count"))
    # suite.addTest(TestEipGroupClient("test_purchase_reserved_eip_group"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
