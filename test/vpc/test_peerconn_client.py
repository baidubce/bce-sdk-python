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
Unit tests for peer_connection client.
"""

import unittest
import uuid

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.vpc import peerconn_client
from baidubce.services.vpc import peerconn_model

# Sandbox
LOCAL_VPC_ID = ''
PEER_VPC_ID = ''
PEER_VPC_ID_DIFF = ''
PEER_REGION = 'bj'
PC_DESCRIPTION = 'peer_same_account'
PC_DESCRIPTION_DIFF = 'peer_diff_account'
LOCAL_IF_NAME = 'localIfName'
LOCAL_IF_NAME_DIFF = 'localIfNameDiff'
LOCAL_IF_ID = ''
PEER_ACCOUNT_ID = ''
PEER_IF_NAME = 'peerIfName'
PEERCONN_ID = ''
PEERCONN_ID_DIFF = ''

pre_paid_billing = peerconn_model.Billing('Prepaid')
post_paid_billing = peerconn_model.Billing('Postpaid')


class TestPeerConnClient(unittest.TestCase):
    """
    Test class for peer connection sdk client
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
        self.client = peerconn_client.PeerConnClient(config)

    def tearDown(self):
        """
        tear down
        """
        self.client = None

    def test_create_peerconn_same_account(self):
        """
        test case for creating peer connection
        """
        client_token = generate_client_token()
        self.client.create_peerconn(client_token=client_token,
                                    bandwidth_in_mbps=10,
                                    local_vpc_id=LOCAL_VPC_ID,
                                    peer_vpc_id=PEER_VPC_ID,
                                    peer_region=PEER_REGION,
                                    billing=post_paid_billing,
                                    description=PC_DESCRIPTION,
                                    local_if_name=LOCAL_IF_NAME,
                                    peer_if_name=PEER_IF_NAME, config=None)

    def test_create_peerconn_diff_account(self):
        """
        test case for creating peer connection
        """
        client_token = generate_client_token()
        self.client.create_peerconn(client_token=client_token,
                                    bandwidth_in_mbps=10,
                                    local_vpc_id=LOCAL_VPC_ID,
                                    peer_vpc_id=PEER_VPC_ID_DIFF,
                                    peer_region=PEER_REGION,
                                    billing=post_paid_billing,
                                    description=PC_DESCRIPTION_DIFF,
                                    local_if_name=LOCAL_IF_NAME_DIFF,
                                    peer_account_id=PEER_ACCOUNT_ID,
                                    config=None)

    def test_create_peerconn_diff_region(self):
        """
        test case for creating peer connection
        """
        client_token = generate_client_token()
        self.client.create_peerconn(client_token=client_token,
                                    bandwidth_in_mbps=1,
                                    local_vpc_id=LOCAL_VPC_ID,
                                    peer_vpc_id=PEER_VPC_ID,
                                    peer_region=PEER_REGION,
                                    billing=pre_paid_billing,
                                    description=PC_DESCRIPTION,
                                    local_if_name=LOCAL_IF_NAME,
                                    config=None)

    def test_list_peerconns(self):
        """
        test case for listing peer connections
        """
        print((self.client.list_peerconns(LOCAL_VPC_ID, max_keys=500)))

    def test_get_peerconn(self):
        """
        test case for getting peer connection details
        """
        print((self.client.get_peerconn(peer_conn_id=PEERCONN_ID)))

    def test_update_peerconn(self):
        """
        test case for updating peer connection local interface name
        and description
        """
        client_token = None  # generate_client_token()
        local_if_name = 'new_pc_if_name2'
        description = 'new_description2'
        self.client.update_peerconn(peer_conn_id=PEERCONN_ID,
                                    local_if_id=LOCAL_IF_ID,
                                    description=description,
                                    local_if_name=local_if_name,
                                    client_token=client_token)

    def test_accept_peerconn(self):
        """
        test case for accepting peer connection
        """
        self.client.handle_peerconn(PEERCONN_ID_DIFF, 'accept')

    def test_reject_peerconn(self):
        """
        test case for accepting peer connection
        """
        client_token = generate_client_token()
        self.client.handle_peerconn(PEERCONN_ID_DIFF, 'reject', client_token)

    def test_delete_peerconn(self):
        """
        test case for deleting peer connection
        """
        self.client.delete_peerconn(PEERCONN_ID)

    def test_scale_up_peerconn(self):
        """
        test case for resizing peer connection (bandwidth scale up)
        """
        new_bandwidth_in_mbps = 20
        self.client.resize_peerconn(PEERCONN_ID, new_bandwidth_in_mbps)

    def test_scale_down_peerconn(self):
        """
        test case for resizing peer connection (bandwidth scale up)
        """
        client_token = generate_client_token()
        new_bandwidth_in_mbps = 10
        self.client.resize_peerconn(PEERCONN_ID, new_bandwidth_in_mbps,
                                    client_token)

    def test_purchase_reserved_peerconn(self):
        """
        test case for renewing peer connection prepaid billing
        """
        self.client.purchase_reserved_peerconn(peer_conn_id=PEERCONN_ID,
                                               billing=pre_paid_billing)

    def test_open_peerconn_dns_sync(self):
        """
        test case for opening peer connection dns sync
        """
        self.client.open_peerconn_dns_sync(peer_conn_id=PEERCONN_ID,
                                           role='initiator')

    def test_close_peerconn_dns_sync(self):
        """
        test case for closing peer connection dns sync
        """
        self.client.close_peerconn_dns_sync(peer_conn_id=PEERCONN_ID,
                                            role='acceptor')


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

    # suite.addTest(TestPeerConnClient("test_list_peerconns"))
    # suite.addTest(TestPeerConnClient("test_get_peerconn"))
    # suite.addTest(TestPeerConnClient("test_update_peerconn"))
    # suite.addTest(TestPeerConnClient("test_scale_up_peerconn"))
    # suite.addTest(TestPeerConnClient("test_scale_down_peerconn"))
    # suite.addTest(TestPeerConnClient("test_open_peerconn_dns_sync"))
    # suite.addTest(TestPeerConnClient("test_close_peerconn_dns_sync"))
    # suite.addTest(TestPeerConnClient("test_delete_peerconn"))
    # suite.addTest(TestPeerConnClient("test_create_peerconn_diff_account"))
    # suite.addTest(TestPeerConnClient("test_accept_peerconn"))
    # suite.addTest(TestPeerConnClient("test_reject_peerconn"))
    # suite.addTest(TestPeerConnClient("test_create_peerconn_diff_region"))
    # suite.addTest(TestPeerConnClient("test_create_peerconn_same_account"))
    # suite.addTest(TestPeerConnClient("test_purchase_reserved_peerconn"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
