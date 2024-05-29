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
This module for local dns test.
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
from baidubce.services.localdns import ld_client
import collections

collections.Callable = collections.abc.Callable

HOST = b''
AK = b''
SK = b''


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.
    :return:
    :rtype string
    """
    return str(uuid.uuid4())


generate_client_token = generate_client_token_by_uuid


class TestLdClient(unittest.TestCase):
    """
    unit test
    """

    def setUp(self):
        """
        set up
        """
        config = BceClientConfiguration(
            credentials=BceCredentials(AK, SK), endpoint=HOST)
        self.the_client = ld_client.LdClient(config)

    def test_list_zone(self):
        """
        test case for list_zone
        """
        print(self.the_client.list_private_zone())

    def test_create_zone(self):
        """
        test case for create_zone
        """
        client_token = generate_client_token()
        create_private_zone_request = {
            'zoneName': 'ccqTest0711.com'
        }
        self.assertEqual(
            type(self.the_client.create_private_zone(create_private_zone_request=create_private_zone_request, client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_delete_zone(self):
        """
        test case for delete_zone
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.delete_private_zone(zone_id='zone-w4zkd52uqxj1', client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_get_zone(self):
        """
        test case for get_zone
        """
        print(self.the_client.get_private_zone(zone_id='zone-nqa0uqyse51z'))

    def test_bind_vpc(self):
        """
        test case for bind_vpc
        """
        client_token = generate_client_token()
        bind_vpc_request = {
            'region': 'bj',
            'vpcIds': ['vpc-4kzjwxgvx4fi']
        }
        self.assertEqual(
            type(self.the_client.bind_vpc(zone_id='zone-nqa0uqyse51z', bind_vpc_request=bind_vpc_request,
                                          client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_unbind_vpc(self):
        """
        test case for unbind_vpc
        """
        client_token = generate_client_token()
        unbind_vpc_request = {
            'region': 'bj',
            'vpcIds': ['vpc-4kzjwxgvx4fi']
        }
        self.assertEqual(
            type(self.the_client.unbind_vpc(zone_id='zone-nqa0uqyse51z', unbind_vpc_request=unbind_vpc_request,
                                          client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_add_record(self):
        """
        test case for add_record
        """
        client_token = generate_client_token()
        add_record_request = {
            'rr': 'www',
            'type': 'A',
            'value': '2.2.2.2'
        }
        self.assertEqual(
            type(self.the_client.add_record(zone_id='zone-nqa0uqyse51z', add_record_request=add_record_request,
                                          client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_update_record(self):
        """
        test case for update_record
        """
        client_token = generate_client_token()
        update_record_request = {
            'rr': 'www',
            'type': 'A',
            'value': '2.2.2.3'
        }
        self.assertEqual(
            type(self.the_client.update_record(record_id='rc-ix82js8e23ev', update_record_request=update_record_request,
                                          client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_enable_record(self):
        """
        test case for enable_record
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.enable_record(record_id='rc-ix82js8e23ev', client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_disable_record(self):
        """
        test case for disable_record
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.disable_record(record_id='rc-ix82js8e23ev', client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_delete_record(self):
        """
        test case for delete_record
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.delete_record(record_id='rc-ix82js8e23ev', client_token=client_token)),
            baidubce.bce_response.BceResponse)

