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
This module for ipv6 blb test.
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
from baidubce.services.blb import blb_client

vpc_id = ''
subnetId = ''
HOST = b''
AK = b''
SK = b''
blbId = b''
bccId = ''
certID = ''


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.
    :return:
    :rtype string
    """
    return str(uuid.uuid4())


generate_client_token = generate_client_token_by_uuid


class TestIpv6BlbClient(unittest.TestCase):
    """
    unit test
    """

    def setUp(self):
        """
        set up
        """
        config = BceClientConfiguration(
            credentials=BceCredentials(AK, SK), endpoint=HOST)
        self.the_client = blb_client.BlbClient(config)

    def test_create_loadbalancer(self):
        """
        test case for create_loadbalancer
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.create_ipv6_loadbalancer(
                name='test_blb_hzf', vpc_id=vpc_id, subnet_id=subnetId,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_describe_loadbalancers(self):
        """
        test case for describe_loadbalancers
        """
        print(self.the_client.describe_ipv6_loadbalancers())

    
if __name__ == "__main__":
    suite = unittest.TestSuite()
    runner = unittest.TextTestRunner()
    runner.run(suite)
