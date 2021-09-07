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
Unit tests for eip_bp_client.
"""

import unittest
import uuid

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.eip import eip_tp_client

Reservation_length = 1
Capacity = '10G'
Deduct_Policy = 'FullTimeDurationPackage'
Package_Type = 'WebOutBytes'
MARKER = ''
MAX_KEYS = 1000
ID = 'tp-87V5cnkwqO'


class TestEipTpClient(unittest.TestCase):
    """
    Test class for eip_tp sdk client
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
        self.client = eip_tp_client.EipTpClient(config)

    def tearDown(self):
        """
        tear down
        """
        self.client = None

    def test_create_eip_tp(self):
        """
        test case for creating eip_tp
        """
        client_token = generate_client_token()
        return self.client.create_eip_tp(client_token=client_token,
                                         reservation_length=Reservation_length,
                                         capacity=Capacity, deduct_policy=Deduct_Policy,
                                         package_type=Package_Type, config=None)

    def test_get_eip_tp_detail(self):
        """
        test case for getting eip_tp detail
        """
        print(self.client.get_eip_tp_detail(id=ID, config=None))

    def test_list_eip_tps(self):
        """
        test case for listing eip_tps
        """
        print(self.client.list_eip_tps(deduct_policy="TimeDurationPackage", config=None))


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
    suite.addTest(TestEipTpClient("test_create_eip_tp"))
    suite.addTest(TestEipTpClient("test_get_eip_tp_detail"))
    suite.addTest(TestEipTpClient("test_list_eip_tps"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
