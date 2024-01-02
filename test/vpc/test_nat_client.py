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
SNAT_RULE_ID = b''
DNAT_RULE_ID = b''


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
        bce_response = self.client.create_nat(client_token=client_token, name=name,
                                        vpc_id=VPC_ID, spec=spec,
                                        billing=post_paid_billing)
        print(bce_response)
        self.assertEqual(type(bce_response), baidubce.bce_response.BceResponse)
        print(bce_response.nat_id)

    def test_create_enhance_nat(self):
        """
        test case for creating enhance nat
        """
        client_token = generate_client_token()
        name = 'enhance_nat_' + client_token
        bce_response = self.client.create_nat(client_token=client_token, name=name,
                               vpc_id=VPC_ID,
                               billing=post_paid_billing, cu_num=10)
        print (type(bce_response))
        print(bce_response)
        print(bce_response.nat_id)

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
    
    def test_create_nat_with_dnat_eip(self):
        """
        test case for creating nat with dnat eips binding
        """
        client_token = generate_client_token()
        name = 'with_dnat_eip_binded' + client_token
        self.client.create_nat(client_token=client_token, name=name,
                               vpc_id=VPC_ID, cu_num=10,
                               dnat_eips=EIP)

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
        print(self.client.list_nats())

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
    
    def test_bind_dnat_eip(self):
        """
        test case for binding dnat with EIP
        """
        self.assertEqual(
            type(self.client.bind_dnat_eip(nat_id=NAT_ID, eips=EIP)),
            baidubce.bce_response.BceResponse)

    def test_bind_dnat_shared_eip(self):
        """
        test case for binding dnat with shared EIP
        """
        self.assertEqual(
            type(self.client.bind_dnat_eip(nat_id=NAT_ID, eips=SHARED_EIP)),
            baidubce.bce_response.BceResponse)

    def test_unbond_dnat_eip(self):
        """
        test case for unbinding dnat EIP
        """
        self.assertEqual(
            type(self.client.unbind_dnat_eip(nat_id=NAT_ID, eips=EIP)),
            baidubce.bce_response.BceResponse)

    def test_unbond_shared_dnat_eip(self):
        """
        test case for unbinding dnat shared eips
        """
        self.assertEqual(
            type(self.client.unbind_dnat_eip(nat_id=NAT_ID, eips=SHARED_EIP)),
            baidubce.bce_response.BceResponse)

    def test_create_snat_rule(self):
        """
        test case for creating snat rule
        """
        rule_name = 'test_snat_rule'
        source_cidr = '192.168.1.0/24'
        self.assertEqual(
            type(self.client.create_snat_rule(nat_id=NAT_ID, rule_name=rule_name, source_cidr=source_cidr, public_ip_address=EIP)),
            baidubce.bce_response.BceResponse)
    
    def test_batch_create_snat_rule(self):
        """
        test case for batch creating snat rule
        """
        rules = [
            {
                'ruleName': 'test_snat_rule1',
                'sourceCIDR': '192.168.1.0/24',
                'publicIpsAddress': EIP
            },
            {
                'ruleName': 'test_snat_rule2',
                'sourceCIDR': '192.168.2.0/24',
                'publicIpsAddress': EIP
            }
        ]
        self.assertEqual(
            type(self.client.batch_create_snat_rule(nat_id=NAT_ID, rules=rules)),
            baidubce.bce_response.BceResponse)
        
    def test_delete_snat_rule(self):
        """
        test case for deleting snat rule
        """
        self.assertEqual(
            type(self.client.delete_snat_rule(nat_id=NAT_ID, snat_rule_id=SNAT_RULE_ID)),
            baidubce.bce_response.BceResponse)
        
    def test_update_snat_rule(self):
        """
        test case for updating snat rule
        """
        new_name = b'test_snat_rule_new'
        source_cidr = '192.168.3.0/24'
        self.assertEqual(
            type(self.client.update_snat_rule(nat_id=NAT_ID, snat_rule_id=SNAT_RULE_ID, name=new_name, source_cidr=source_cidr, public_ip_address=EIP)),
            baidubce.bce_response.BceResponse)

    def test_list_snat_rule(self):
        """
        test case for listing snat rule
        """
        self.assertEqual(
            type(self.client.list_snat_rule(nat_id=NAT_ID, maxKeys=2)),
            baidubce.bce_response.BceResponse)
    
    def test_create_dnat_rule(self):
        """
        test case for creating dnat rule
        """
        rule_name = 'test_dnat_rule'
        private_ip_address = '192.168.1.0/24'
        public_ip_address = EIP[0]
        protocol = 'TCP'
        public_port = '1212'
        private_port = '1212'
        self.assertEqual(
            type(self.client.create_dnat_rule(
            nat_id=NAT_ID, public_ip_address=public_ip_address,
            private_ip_address=private_ip_address,rule_name=rule_name,
            protocol=protocol, public_port=public_port, private_port=private_port)),
            baidubce.bce_response.BceResponse)        
    
    def test_batch_create_dnat_rule(self):
        """
        test case for batch creating dnat rule
        """
        rules = [
            {
                'ruleName': 'test_dnat_rule1',
                'publicIpAddress': EIP[0],
                'privateIpAddress': "192.168.1.1",
                'protocol': 'TCP'
                'publicPort' '1212',
                'privatePort': '1212',
            },
            {
                'ruleName': 'test_dnat_rule1',
                'publicIpAddress': EIP[1],
                'privateIpAddress': "192.168.1.2",
                'protocol': 'UDP'
                'publicPort' '65535',
                'privatePort': '65535',
            }
        ]
        self.assertEqual(
            type(self.client.batch_create_dnat_rule(nat_id=NAT_ID, rules=rules)),
            baidubce.bce_response.BceResponse)
        
    def test_delete_dnat_rule(self):
        """
        test case for deleting dnat rule
        """
        self.assertEqual(
            type(self.client.delete_dnat_rule(nat_id=NAT_ID, dnat_rule_id=DNAT_RULE_ID)),
            baidubce.bce_response.BceResponse)
        
    def test_update_dnat_rule(self):
        """
        test case for updating snat rule
        """
        new_name = b'test_dnat_rule_new'
        private_ip_address = '192.168.1.3'
        public_ip_address = EIP[0]
        protocol = 'TCP'
        self.assertEqual(
            type(self.client.update_dnat_rule(
            nat_id=NAT_ID, dnat_rule_id=DNAT_RULE_ID, rule_name=new_name, public_ip_address=public_ip_address, private_ip_address=private_ip_address, protocol=protocol)),
            baidubce.bce_response.BceResponse)

    def test_list_dnat_rule(self):
        """
        test case for listing snat rule
        """
        self.assertEqual(
            type(self.client.list_dnat_rule(nat_id=NAT_ID, maxKeys=2)),
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
    #suite.addTest(TestNatClient("test_bind_dnat_eip"))
    #suite.addTest(TestNatClient("test_bind_dnat_shared_eip"))
    #suite.addTest(TestNatClient("test_unbond_dnat"))
    #suite.addTest(TestNatClient("test_unbond_shared_dnat_eip"))
    #suite.addTest(TestNatClient("test_create_snat_rule"))
    #suite.addTest(TestNatClient("test_batch_create_snat_rule"))
    #suite.addTest(TestNatClient("test_delete_snat_rule"))
    #suite.addTest(TestNatClient("test_update_snat_rule"))
    #suite.addTest(TestNatClient("test_list_snat_rule"))
    #suite.addTest(TestNatClient("test_create_dnat_rule"))
    #suite.addTest(TestNatClient("test_batch_create_dnat_rule"))
    #suite.addTest(TestNatClient("test_delete_dnat_rule"))
    #suite.addTest(TestNatClient("test_update_dnat_rule"))
    #suite.addTest(TestNatClient("test_list_dnat_rule"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
