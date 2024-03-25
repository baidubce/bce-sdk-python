# -*- coding: utf-8 -*-
# !/usr/bin/env python

# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import unittest
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.lbdc import lbdc_client
from baidubce.services.lbdc.model import Billing
from unittest.mock import MagicMock


class TestLbdcClient(unittest.TestCase):
    """
    unit test
    """

    def setUp(self):
        """
        set up
        """
        HOST = b''
        AK = b''
        SK = b''
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK), lbdc=HOST)
        self.client = lbdc_client.LbdcClient(config)

    def test_create_lbdc(self):
        # Test case 1: Test with minimum input values
        response = MagicMock()
        response.status_code = 200
        self.client._send_request = MagicMock(return_value=response)
        self.client.create_lbdc(name='test', type='7Layer', ccu_count=1, billing=Billing(reservation_length=1))
        self.client._send_request.assert_called_once_with(
            http_method='POST',
            path='/v1/lbdc',
            body='{"name": "test", "type": "7Layer", "ccuCount": 1,\
                "billing": {"paymentTiming": Postpaid, "reservation_length": 1}}',
            headers={'Accept': '*/*', 'Content-Type': 'application/json;charset=utf-8'},
            params={b'clientToken': self.client._generate_default_client_token()},
            config=None,
            body_parser=unittest.mock.ANY
        )

        # Test case 2: Test with all input values
        response = MagicMock()
        response.status_code = 200
        self.client._send_request = MagicMock(return_value=response)
        self.client.create_lbdc(
            name='test',
            type='4Layer',
            ccu_count=1,
            billing={
                'payment_timing': 'Postpaid',
                'reservation': {
                    'reservation_length': 1
                }
            },
            desc='test',
            renew={
                'reservation_length': 1
            },
            client_token='test',
            config=None
        )
        self.client._send_request.assert_called_once_with(
            http_method='POST',
            path='/v1/lbdc',
            body='{"name": "test", "type": "test", "ccuCount": 1,\
                "billing": {"paymentTiming": "Postpaid", "reservation": {"reservationLength": 1}},\
                "desc": "test", "renewReservation": {"reservationLength": 1}}',
            headers={'Accept': '*/*', 'Content-Type': 'application/json;charset=utf-8'},
            params={b'clientToken': 'test'},
            config=None,
            body_parser=unittest.mock.ANY
        )

        # Test case 3: Test with invalid input values
        with self.assertRaises(TypeError):
            self.client.create_lbdc(name='test', type='test', ccu_count='invalid', billing=None)

    def test_upgrade_lbdc(self):
        # Test case 1: Test with minimum input values
        response = MagicMock()
        response.status_code = 200
        self.client._send_request = MagicMock(return_value=response)
        self.client.upgrade_lbdc(lbdc_id='test', action='resize', ccu_count=1)
        self.client._send_request.assert_called_once_with(
            http_method='PUT',
            path='/v1/lbdc/test',
            body='{"ccuCount": 1}',
            headers={'Accept': '*/*', 'Content-Type': 'application/json;charset=utf-8'},
            params={b'clientToken': self.client._generate_default_client_token(), b'resize': ''},
            config=None,
            body_parser=unittest.mock.ANY
        )

        # Test case 2: Test with all input values
        response = MagicMock()
        response.status_code = 200
        self.client._send_request = MagicMock(return_value=response)
        self.client.upgrade_lbdc(
            lbdc_id='test',
            action='resize',
            ccu_count=1,
            client_token='test',
            config=None
        )
        self.client._send_request.assert_called_once_with(
            http_method='PUT',
            path='/v1/lbdc/test',
            body='{"ccuCount": 1}',
            headers={'Accept': '*/*', 'Content-Type': 'application/json;charset=utf-8'},
            params={b'clientToken': 'test', b'resize': ''},
            config=None,
            body_parser=unittest.mock.ANY
        )

        # Test case 3: Test with invalid input values
        with self.assertRaises(TypeError):
            self.client.upgrade_lbdc(lbdc_id='test', action='test', ccu_count='invalid')

    def test_renew_lbdc(self):
        # Test case 1: Test with minimum input values
        response = MagicMock()
        response.status_code = 200
        self.client._send_request = MagicMock(return_value=response)
        self.client.renew_lbdc(lbdc_id='test', action='purchaseReserved', billing=None)
        self.client._send_request.assert_called_once_with(
            http_method='PUT',
            path='/v1/lbdc/test',
            body='{ "billing": {"reservation": null } }',
            headers={'Accept': '*/*', 'Content-Type': 'application/json;charset=utf-8'},
            params={b'clientToken': self.client._generate_default_client_token(), b'purchaseReserved': ''},
            config=None,
            body_parser=unittest.mock.ANY
        )

        # Test case 2: Test with all input values
        response = MagicMock()
        response.status_code = 200
        self.client._send_request = MagicMock(return_value=response)
        self.client.renew_lbdc(
            lbdc_id='test',
            action='purchaseReserved',
            billing={
                'reservation': {
                    'reservation_length': 1
                }
            },
            client_token='test',
            config=None
        )
        self.client._send_request.assert_called_once_with(
            http_method='PUT',
            path='/v1/lbdc/test',
            body='{"billing": {"reservation": {"reservationLength": 1 }}}',
            headers={'Accept': '*/*', 'Content-Type': 'application/json;charset=utf-8'},
            params={b'clientToken': 'test', b'purchaseReserved': ''},
            config=None,
            body_parser=unittest.mock.ANY
        )

        # Test case 3: Test with invalid input values
        with self.assertRaises(TypeError):
            self.client.renew_lbdc(lbdc_id='test', action='test', billing='invalid')

    def test_list_lbdc(self):
        # Test case 1: Test with minimum input values
        response = MagicMock()
        response.status_code = 200
        self.client._send_request = MagicMock(return_value=response)
        self.client.list_lbdc()
        self.client._send_request.assert_called_once_with(
            http_method='GET',
            path='/v1/lbdc',
            headers={'Accept': '*/*', 'Content-Type': 'application/json;charset=utf-8'},
            params={},
            config=None,
            body_parser=unittest.mock.ANY
        )

        # Test case 2: Test with all input values
        response = MagicMock()
        response.status_code = 200
        self.client._send_request = MagicMock(return_value=response)
        self.client.list_lbdc(lbdc_id='test', name='test', config=None)
        self.client._send_request.assert_called_once_with(
            http_method='GET',
            path='/v1/lbdc',
            headers={'Accept': '*/*', 'Content-Type': 'application/json;charset=utf-8'},
            params={b'id': 'test', b'name': 'test'},
            config=None,
            body_parser=unittest.mock.ANY
        )

    def test_get_lbdc(self):
        expected_response = MagicMock()
        expected_response.status_code = 200

        self.client._send_request = MagicMock(return_value=expected_response)
        self.client.get_lbdc('lbdc-1234')
        self.client._send_request.assert_called_once_with(
            http_method='GET',
            path='/v1/lbdc/lbdc-1234',
            headers={'Accept': '*/*', 'Content-Type': 'application/json;charset=utf-8'},
            params={},
            config=None,
            body_parser=unittest.mock.ANY
        )

    def test_update_lbdc(self):
        expected_response = MagicMock()
        expected_response.status_code = 200

        self.client._send_request = MagicMock(return_value=expected_response)
        self.client.update_lbdc('lbdc-1234', name='updated-lbdc', desc='updated description')
        self.client._send_request.assert_called_once_with(
            http_method='PUT',
            path='/v1/lbdc/lbdc-1234',
            body='{"name": "updated-lbdc", "desc": "updated description"}',
            headers={'Accept': '*/*', 'Content-Type': 'application/json;charset=utf-8'},
            params={},
            config=None,
            body_parser=unittest.mock.ANY
        )

    def test_list_lbdc_blb(self):
        expected_response = MagicMock()
        expected_response.status_code = 200
        expected_response.body = b'[{"id": "lbdc-1234", "name": "test-lbdc"}]'

        self.client._send_request = MagicMock(return_value=expected_response)
        self.client.list_lbdc_blb('lbdc-1234')
        self.client._send_request.assert_called_once_with(
            http_method='GET',
            path='/v1/lbdc/lbdc-1234/blb',
            headers={'Accept': '*/*', 'Content-Type': 'application/json;charset=utf-8'},
            params={},
            config=None,
            body_parser=unittest.mock.ANY
        )
