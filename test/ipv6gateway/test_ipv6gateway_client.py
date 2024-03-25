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
Unit tests for ipv6gateway_client.
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
from baidubce.services.ipv6gateway import ipv6gateway_client
from baidubce.services.ipv6gateway import ipv6gateway_model

VPC_ID = b''
GATEWAY_ID = b''
EGRESS_ONLY_RULE_ID = b''
RATE_LIMIT_RULE_ID = b''

pre_paid_billing = ipv6gateway_model.Billing('Prepaid')
post_paid_billing = ipv6gateway_model.Billing('Postpaid')


class TestIPv6GatewayClient(unittest.TestCase):
    """
    Test class for ipv6gateway sdk client
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
        self.client = ipv6gateway_client.IPv6GatewayClient(config)

    def tearDown(self):
        """
        tear down
        """
        self.client = None

    def test_create_ipv6_gateway(self):
        """
        test case for creating ipv6 gateway
        """
        client_token = generate_client_token()
        name = 'ipv6_gateway_name' + client_token
        bandwidth = 10
        bce_response = self.client.create_ipv6_gateway(client_token=client_token, name=name,
                                                       vpc_id=VPC_ID, bandwidthInMbps=bandwidth,
                                                       billing=post_paid_billing)
        print(bce_response)
        self.assertEqual(type(bce_response), baidubce.bce_response.BceResponse)
        print(bce_response.ipv6_gateway_id)

    def test_list_ipv6_gateways(self):
        """
        test case for listing ipv6 gateways
        """
        print(self.client.list_ipv6_gateways(vpc_id=VPC_ID))

    def test_delete_ipv6_gateway(self):
        """
        test case for deleting ipv6 gateway
        """
        self.assertEqual(
            type(self.client.delete_ipv6_gateway(gateway_id=GATEWAY_ID)),
            baidubce.bce_response.BceResponse)

    def test_resize_ipv6_gateway(self):
        """
        test case for resize ipv6 gateway
        """
        bandwidth = 10
        self.assertEqual(
            type(self.client.resize_ipv6_gateway(gateway_id=GATEWAY_ID,
                                                 bandwidthInMbps=bandwidth)),
            baidubce.bce_response.BceResponse)

    def test_create_ipv6_gateway_egress_only_rule(self):
        """
        test case for creating ipv6 gateway egress only rule
        """
        cidr = '2400:da00:e003:d01::/64'
        bce_response = self.client.create_ipv6_gateway_egress_only_rule(gateway_id=GATEWAY_ID,
                                                                        cidr=cidr)
        print(bce_response)
        self.assertEqual(type(bce_response), baidubce.bce_response.BceResponse)
        print(bce_response.egress_only_rule_id)

    def test_list_ipv6_gateway_egress_only_rules(self):
        """
        test case for listing ipv6 gateway egress only rules
        """
        print(self.client.list_ipv6_gateway_egress_only_rules(gateway_id=GATEWAY_ID))

    def test_delete_ipv6_gateway_egress_only_rule(self):
        """
        test case for deleting ipv6 gateway egress only rule
        """
        self.assertEqual(
            type(self.client.delete_ipv6_gateway_egress_only_rule(gateway_id=GATEWAY_ID,
                                                                  egress_only_rule_id=EGRESS_ONLY_RULE_ID)),
            baidubce.bce_response.BceResponse)

    def test_create_ipv6_gateway_rate_limit_rule(self):
        """
        test case for creating ipv6 gateway rate limit rule
        """
        ipv6_address = '240c:4082:0:100::'
        ingress_bandwidth = 10
        egress_bandwidth = 10
        bce_response = self.client.create_ipv6_gateway_rate_limit_rule(gateway_id=GATEWAY_ID, ipv6_address=ipv6_address,
                                                                       ingress_bandwidth=ingress_bandwidth,
                                                                       egress_bandwidth=egress_bandwidth)
        print(bce_response)
        self.assertEqual(type(bce_response), baidubce.bce_response.BceResponse)
        print(bce_response.rate_limit_rule_id)

    def test_list_ipv6_gateway_rate_limit_rules(self):
        """
        test case for listing ipv6 gateway rate limit rules
        """
        print(self.client.list_ipv6_gateway_rate_limit_rules(gateway_id=GATEWAY_ID))

    def test_delete_ipv6_gateway_rate_limit_rule(self):
        """
        test case for deleting ipv6 gateway rate limit rule
        """
        self.assertEqual(
            type(self.client.delete_ipv6_gateway_rate_limit_rule(gateway_id=GATEWAY_ID,
                                                                 rate_limit_rule_id=RATE_LIMIT_RULE_ID)),
            baidubce.bce_response.BceResponse)

    def test_update_ipv6_gateway_rate_limit_rule(self):
        """
        test case for updating ipv6 gateway rate limit rule
        """
        ingress_bandwidth = 10
        egress_bandwidth = 10
        self.assertEqual(
            type(self.client.update_ipv6_gateway_rate_limit_rule(gateway_id=GATEWAY_ID,
                                                                 rate_limit_rule_id=RATE_LIMIT_RULE_ID,
                                                                 ingress_bandwidth=ingress_bandwidth,
                                                                 egress_bandwidth=egress_bandwidth)),
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
    # 2s 2b 3s 3bwait for start
    # suite.addTest(TestIPv6GatewayClient("test_create_ipv6_gateway"))
    # suite.addTest(TestIPv6GatewayClient("test_list_ipv6_gateways"))
    # suite.addTest(TestIPv6GatewayClient("test_delete_ipv6_gateway"))
    # suite.addTest(TestIPv6GatewayClient("test_resize_ipv6_gateway"))
    # suite.addTest(TestIPv6GatewayClient("test_create_ipv6_gateway_egress_only_rule"))
    # suite.addTest(TestIPv6GatewayClient("test_list_ipv6_gateway_egress_only_rules"))
    # suite.addTest(TestIPv6GatewayClient("test_delete_ipv6_gateway_egress_only_rule"))
    # suite.addTest(TestIPv6GatewayClient("test_create_ipv6_gateway_rate_limit_rule"))
    # suite.addTest(TestIPv6GatewayClient("test_list_ipv6_gateway_rate_limit_rules"))
    # suite.addTest(TestIPv6GatewayClient("test_delete_ipv6_gateway_rate_limit_rule"))
    # suite.addTest(TestIPv6GatewayClient("test_update_ipv6_gateway_rate_limit_rule"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
