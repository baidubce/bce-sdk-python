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
Unit tests for nat_client.
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
from baidubce.services.vpc import nat_client
from baidubce.services.vpc import nat_model

VPC_ID = b''
EIP = ['']
SHARED_EIP = ['']
NEW_SHARED_EIP = ['']
NAT_ID = b''
NAME = b''
IP = ''

pre_paid_billing = nat_model.Billing('Prepaid')
post_paid_billing = nat_model.Billing('Postpaid')


class TestNatClient(unittest.TestCase):
    """
    Test class for nat sdk client
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
        self.client = nat_client.NatClient(config)

    def tearDown(self):
        """
        tear down
        """
        self.client = None

    def test_create_nat_without_eips(self):
        """
        test case for creating nat without eips option
        """
        client_token = generate_client_token()
        name = 'nat_without_EIPs' + client_token
        spec = b'small'
        self.assertEqual(
            type(self.client.create_nat(client_token=client_token, name=name,
                                        vpc_id=VPC_ID, spec=spec,
                                        billing=post_paid_billing)),
            baidubce.bce_response.BceResponse)

    def test_create_nat_with_eip(self):
        """
        test case for creating nat with eips option
        """
        client_token = generate_client_token()
        name = 'nat_EIP' + client_token
        # self.assertEqual(
        #     type(self.client.create_nat(client_token=client_token, name=name,
        #                                 vpc_id=VPC_ID, spec='small',
        #                                 billing=pre_paid_billing,
        #                                 eips = EIP)),
        #     baidubce.bce_response.BceResponse)
        self.client.create_nat(client_token=client_token, name=name,
                               vpc_id=VPC_ID, spec='small',
                               eips=EIP)

    def test_create_nat_with_shared_eip(self):
        """
        test case for creating nat with shared eips
        """
        client_token = generate_client_token()
        name = 'nat_shared_EIP' + client_token
        self.assertEqual(
            type(self.client.create_nat(client_token=client_token, name=name,
                                        vpc_id=VPC_ID, spec='medium',
                                        eips=SHARED_EIP)),
            baidubce.bce_response.BceResponse)

    def test_create_nat_with_eip_postpaid(self):
        """
        test case for creating nat using postpaid billing
        """
        client_token = generate_client_token()
        name = 'nat_EIP' + client_token
        self.assertEqual(
            type(self.client.create_nat(client_token=client_token, name=name,
                                        vpc_id=VPC_ID, spec='small',
                                        billing=post_paid_billing, eips=EIP)),
            baidubce.bce_response.BceResponse)

    def test_list_nats(self):
        """
        test case for listing nat gws
        """
        # self.assertEqual(
        #     type(self.client.list_nats(vpc_id=VPC_ID)),
        #     baidubce.bce_response.BceResponse)

        print(self.client.list_nats(vpc_id=VPC_ID))

    def test_list_nats_with_detailed_options(self):
        """
        test case for listing nat gws with detailed options
        """
        # self.assertEqual(
        #     type(self.client.list_nats(vpc_id=VPC_ID, nat_id=NAT_ID,
        #                                name=NAME,ip=IP)),
        #     baidubce.bce_response.BceResponse)
        print(self.client.list_nats(vpc_id=VPC_ID, nat_id=NAT_ID,
                                    name=NAME, ip=IP))

    def test_get_nat(self):
        """
        test case for getting nat details
        """
        # self.assertEqual(
        #     type(self.client.get_nat(nat_id=NAT_ID)),
        #     baidubce.bce_response.BceResponse)

        print(self.client.get_nat(nat_id=NAT_ID))

    def test_update_nat(self):
        """
        test case for updating nat name
        """
        new_name = b'test_nat_new'
        self.assertEqual(
            type(self.client.update_nat(nat_id=NAT_ID, name=new_name)),
            baidubce.bce_response.BceResponse)


    def test_bind_eip_eip(self):
        """
        test case for binding nat with EIP
        """
        self.assertEqual(
            type(self.client.bind_eip(nat_id=NAT_ID, eips=EIP)),
            baidubce.bce_response.BceResponse)

    def test_bind_eip_shared_eip(self):
        """
        test case for binding nat with shared EIP
        """
        self.assertEqual(
            type(self.client.bind_eip(nat_id=NAT_ID, eips=SHARED_EIP)),
            baidubce.bce_response.BceResponse)

    def test_unbond_eip(self):
        """
        test case for unbinding EIP
        """
        self.assertEqual(
            type(self.client.unbind_eip(nat_id=NAT_ID, eips=EIP)),
            baidubce.bce_response.BceResponse)

    def test_unbond_shared_eip(self):
        """
        test case for unbinding shared eips
        """
        self.assertEqual(
            type(self.client.unbind_eip(nat_id=NAT_ID, eips=SHARED_EIP)),
            baidubce.bce_response.BceResponse)

    def test_delete_nat(self):
        """
        test case for deleting nat
        """
        self.assertEqual(
            type(self.client.delete_nat(nat_id=NAT_ID)),
            baidubce.bce_response.BceResponse)

    def test_purchase_reserved_nat(self):
        """
        test case for renewing nat with prepaid billing
        """
        self.assertEqual(
            type(self.client.purchase_reserved_nat(nat_id=NAT_ID,
                                                   billing=pre_paid_billing)),
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
    #2s 2b 3s 3bwait for start
    #suite.addTest(TestNatClient("test_create_nat_without_eips"))
    #suite.addTest(TestNatClient("test_create_nat_with_eip"))
    #suite.addTest(TestNatClient("test_create_nat_with_shared_eip"))
    #suite.addTest(TestNatClient("test_create_nat_with_eip_postpaid"))
    #suite.addTest(TestNatClient("test_delete_nat"))
    #suite.addTest(TestNatClient("test_bind_eip_eip"))
    #suite.addTest(TestNatClient("test_unbond_eip"))
    #suite.addTest(TestNatClient("test_bind_eip_shared_eip"))
    #suite.addTest(TestNatClient("test_unbond_shared_eip"))
    #suite.addTest(TestNatClient("test_update_nat"))
    #suite.addTest(TestNatClient("test_list_nats"))
    #suite.addTest(TestNatClient("test_list_nats_with_detailed_options"))
    #suite.addTest(TestNatClient("test_get_nat"))
    #suite.addTest(TestNatClient("test_purchase_reserved_nat"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
