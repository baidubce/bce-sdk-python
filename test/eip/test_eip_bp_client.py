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
from baidubce.services.eip import eip_bp_client

EIP = '100.88.9.120'
Create_BandwidthInMbps = 1
Resize_BandwidthInMbps = 2
ID = ''
Name = 'test'
New_Name = 'test1'
Auto_Release_Time = '2020-05-30T00:00:00Z'
New_Auto_Release_Time = '2020-05-30T12:00:00Z'
MARKER = ''
MAX_KEYS = 500


class TestEipBpClient(unittest.TestCase):
    """
    Test class for eip_bp sdk client
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
        self.client = eip_bp_client.EipBpClient(config)

    def tearDown(self):
        """
        tear down
        """
        self.client = None

    def test_create_eip_bp(self):
        """
        test case for creating eip_bp
        """
        client_token = generate_client_token()
        return self.client.create_eip_bp(client_token=client_token,
                                         bandwidth_in_mbps=Create_BandwidthInMbps,
                                         eip=EIP, eip_group_Id=None, autoReleaseTime=Auto_Release_Time,
                                         name=Name, config=None)

    def test_resize_eip_bp(self):
        """
        test case for resizing eip_bp
        """
        client_token = generate_client_token()
        self.client.resize_eip_bp(client_token=client_token,
                                  id=ID, new_bandwidth_in_mbps=Resize_BandwidthInMbps, config=None)

    def test_get_eip_bp_detail(self):
        """
        test case for getting eip_bp detail
        """
        print(self.client.get_eip_bp_detail(id=ID, config=None))

    def test_list_eip_bps(self):
        """
        test case for listing eip_bps
        """
        print(self.client.list_eip_bps(config=None))

    def test_update_eip_bp_autoReleaseTime(self):
        """
        test case for updating eip_bp's autoReleaseTime
        """
        client_token = generate_client_token()
        self.client.update_eip_bp_autoReleaseTime(client_token=client_token,
                                                  id=ID, auto_release_time=New_Auto_Release_Time,
                                                  config=None)

    def test_rename_eip_bp(self):
        """
        test case for updating eip_bp's name
        """
        client_token = generate_client_token()
        self.client.rename_eip_bp(client_token=client_token,
                                  id=ID, name=New_Name, config=None)

    def test_release_eip_bp(self):
        """
        test case for updating eip_bp's name
        """
        client_token = generate_client_token()
        self.client.release_eip_bp(client_token=client_token, id=ID)


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
    # suite.addTest(TestEipBpClient("test_create_eip_bp"))
    # suite.addTest(TestEipBpClient("test_resize_eip_bp"))
    # suite.addTest(TestEipBpClient("test_get_eip_bp_detail"))
    # suite.addTest(TestEipBpClient("test_list_eip_bps"))
    # suite.addTest(TestEipBpClient("test_update_eip_bp_autoReleaseTime"))
    # suite.addTest(TestEipBpClient("test_rename_eip_bp"))
    # suite.addTest(TestEipBpClient("test_release_eip_bp"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
