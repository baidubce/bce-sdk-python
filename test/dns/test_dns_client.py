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
This module for dns test.
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
from baidubce.services.dns import dns_client
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


class TestDnsClient(unittest.TestCase):
    """
    unit test
    """

    def setUp(self):
        """
        set up
        """
        config = BceClientConfiguration(
            credentials=BceCredentials(AK, SK), endpoint=HOST)
        self.the_client = dns_client.DnsClient(config)

    def test_list_zone(self):
        """
        test case for list_zone
        """
        print(self.the_client.list_zone(name='javasdk.com'))

    def test_create_zone(self):
        """
        test case for create_zone
        """
        client_token = generate_client_token()
        create_zone_request = {
            'name': 'ccqTest1101.com'
        }
        self.assertEqual(
            type(self.the_client.create_zone(create_zone_request=create_zone_request, client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_delete_zone(self):
        """
        test case for delete_zone
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.delete_zone(zone_name='ccqTest1101.com', client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_paid_zone(self):
        """
        test case for create_zone
        """
        client_token = generate_client_token()
        names = ['ccqTest1101.com']
        create_paid_zone_request = {
            'names': names,
            'productVersion': 'discount',
            'billing': {
                'paymentTiming': 'Prepaid',
                'reservation': {
                    'reservationLength': 1
                }
            }
        }
        self.assertEqual(
            type(self.the_client.create_paid_zone(create_paid_zone_request=create_paid_zone_request,
                                                  client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_upgrade_zone(self):
        """
        test case for upgrade_zone
        """
        client_token = generate_client_token()
        names = ['ccqbcd.com']
        upgrade_zone_request = {
            'names': names,
            'billing': {
                'paymentTiming': 'Prepaid',
                'reservation': {
                    'reservationLength': 1
                }
            }
        }
        self.assertEqual(
            type(self.the_client.upgrade_zone(upgrade_zone_request=upgrade_zone_request, client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_renew_zone(self):
        """
        test case for renew_zone
        """
        client_token = generate_client_token()
        renew_zone_request = {
            'billing': {
                'reservation': {
                    'reservationLength': 1
                }
            }
        }
        self.assertEqual(
            type(self.the_client.renew_zone(name='ccqbcd.com', renew_zone_request=renew_zone_request,
                                            client_token=client_token)), baidubce.bce_response.BceResponse)

    def test_create_record(self):
        """
        test case for create_record
        """
        client_token = generate_client_token()
        create_record_request = {
            'rr': 'ccc',
            'type': 'A',
            'value': '1.1.1.1'
        }
        self.assertEqual(
            type(self.the_client.create_record(zone_name='ccqbcd.com', create_record_request=create_record_request,
                                               client_token=client_token)), baidubce.bce_response.BceResponse)

    def test_list_record(self):
        """
        test case for list_record
        """
        print(self.the_client.list_record(zone_name='ccqbcd.com'))

    def test_update_record(self):
        """
        test case for update_record
        """
        client_token = generate_client_token()
        update_record_request = {
            'rr': 'ccc',
            'type': 'A',
            'value': '1.1.1.2'
        }
        self.assertEqual(
            type(self.the_client.update_record(zone_name='ccqbcd.com', update_record_request=update_record_request,
                                               record_id='52082', client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_update_record_enable(self):
        """
        test case for update_record_enable
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.update_record_enable(zone_name='ccqbcd.com', record_id='52089',
                                                      client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_update_record_disable(self):
        """
        test case for update_record_disable
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.update_record_disable(zone_name='ccqbcd.com', record_id='52089',
                                                       client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_delete_record(self):
        """
        test case for delete_zone
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.delete_record(zone_name='ccqbcd.com', record_id='52089', client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_add_line_group(self):
        """
        test case for add_line_group
        """
        client_token = generate_client_token()
        add_line_group_request = {
            'name': 'ccqLineGroup',
            'lines': ["zhejiang.ct", "shanxi.ct"]
        }
        self.assertEqual(
            type(self.the_client.add_line_group(add_line_group_request=add_line_group_request,
                                                client_token=client_token)), baidubce.bce_response.BceResponse)

    def test_update_line_group(self):
        """
        test case for update_line_group
        """
        client_token = generate_client_token()
        update_line_group_request = {
            'name': 'ccqLineGroup',
            'lines': ["zhejiang.ct"]
        }
        self.assertEqual(
            type(self.the_client.update_line_group(line_id='6174', update_line_group_request=update_line_group_request,
                                                   client_token=client_token)), baidubce.bce_response.BceResponse)

    def test_list_line_group(self):
        """
        test case for list_line_group
        """
        print(self.the_client.list_line_group())

    def test_delete_line_group(self):
        """
        test case for delete_line_group
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.delete_line_group(line_id='6174', client_token=client_token)),
            baidubce.bce_response.BceResponse)



