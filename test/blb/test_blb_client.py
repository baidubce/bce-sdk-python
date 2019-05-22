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
This module for blb test.
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


class TestBlbClient(unittest.TestCase):
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
            type(self.the_client.create_loadbalancer(
                name='test_blb_hzf', vpc_id=vpc_id, subnet_id=subnetId,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_describe_loadbalancers(self):
        """
        test case for describe_loadbalancers
        """
        print(self.the_client.describe_loadbalancers())

    def test_describe_loadbalancer_detail(self):
        """
        test case for describe_loadbalancer_detail
        """
        print(self.the_client.describe_loadbalancer_detail(blbId))

    def test_update_loadbalancer(self):
        """
        test case for update_loadbalancer
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.update_loadbalancer(
                blbId, name='blb_test_hzf_new',
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_delete_loadbalancer(self):
        """
        test case for delete_loadbalancer
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.delete_loadbalancer(
                blbId, client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_tcp_listener(self):
        """
        test case for create_tcp_listener
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.create_tcp_listener(
                blbId, 100, 200, 'Hash', client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_udp_listener(self):
        """
        test case for create_udp_listener
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.create_udp_listener(
                blbId, 30000, 400, 'Hash', 'qqq',
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_http_listener(self):
        """
        test case for create_http_listener
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.create_http_listener(
                blbId, 600, 700, 'LeastConnection',
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_https_listener(self):
        """
        test case for create_https_listener
        """
        client_token = generate_client_token()
        cert_ids = []
        cert_ids.append(certID)
        self.assertEqual(
            type(self.the_client.create_https_listener(
                blbId, 800, 900, 'LeastConnection', cert_ids,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_ssl_listener(self):
        """
        test case for create_ssl_listener
        """
        client_token = generate_client_token()
        cert_ids = []
        cert_ids.append(certID)
        self.assertEqual(
            type(self.the_client.create_ssl_listener(
                blbId, 1200, 133, 'LeastConnection', cert_ids,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_describe_tcp_listener(self):
        """
        test case for describe_tcp_listener
        """
        print(self.the_client.describe_tcp_listener(blbId))

    def test_describe_udp_listener(self):
        """
        test case for describe_udp_listener
        """
        print(self.the_client.describe_udp_listener(blbId))

    def test_describe_http_listener(self):
        """
        test case for describe_http_listener
        """
        print(self.the_client.describe_http_listener(blbId))

    def test_describe_https_listener(self):
        """
        test case for describe_https_listener
        """
        print(self.the_client.describe_https_listener(blbId))

    def test_describe_ssl_listener(self):
        """
        test case for describe_ssl_listener
        """
        print(self.the_client.describe_ssl_listener(blbId))

    def test_update_tcp_listener(self):
        """
        test case for tcp listener
        """
        self.assertEqual(
            type(self.the_client.update_tcp_listener(
                blbId, 100, backend_port=250)),
            baidubce.bce_response.BceResponse)

    def test_update_udp_listener(self):
        """
        test case for udp listener
        """
        self.assertEqual(
            type(self.the_client.update_udp_listener(
                blbId, 30000, backend_port=677)),
            baidubce.bce_response.BceResponse)

    def test_update_http_listener(self):
        """
        test case for http listener
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.update_http_listener(
                blbId, 600, backend_port=755)),
            baidubce.bce_response.BceResponse)

    def test_update_https_listener(self):
        """
        test case for https listener
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.update_https_listener(
                blbId, 800, backend_port=950)),
            baidubce.bce_response.BceResponse)

    def test_update_ssl_listener(self):
        """
        test case for https listener
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.update_ssl_listener(
                blbId, 1200, backend_port=95)),
            baidubce.bce_response.BceResponse)

    def test_delete_listeners(self):
        """
        test case for delete listener
        """
        client_token = generate_client_token()

        portlist = []
        portlist.append(30000)

        self.assertEqual(
            type(self.the_client.delete_listeners(
                blbId, portlist, client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_add_backend_servers(self):
        """
        test case for add backend servers
        """
        client_token = generate_client_token()

        backserver = {
            'instanceId': bccId,
            'weight': 50
        }

        backserver_list = []
        backserver_list.append(backserver)
        self.assertEqual(
            type(self.the_client.add_backend_servers(
                blbId, backserver_list, client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_describe_health_status(self):
        """
        test case for describe health status
        """
        print(self.the_client.describe_health_status(blbId, 600))

    def test_describe_backend_servers(self):
        """
        test case for describe backend servers
        """
        print(self.the_client.describe_backend_servers(blbId))

    def test_update_backend_servers(self):
        """
        test case for update backend servers
        """
        client_token = generate_client_token()
        backserver = {
            'instanceId': bccId,
            'weight': 55
        }

        backserver_list = []
        backserver_list.append(backserver)

        self.assertEqual(
            type(self.the_client.update_backend_servers(
                blbId, backserver_list, client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_remove_backend_servers(self):
        """
        test case for remove backend servers
        """
        client_token = generate_client_token()

        backserver_list = []
        backserver_list.append(bccId)

        self.assertEqual(
            type(self.the_client.remove_backend_servers(
                blbId, backserver_list, client_token=client_token)),
            baidubce.bce_response.BceResponse)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    #2s 2b 3s 3b~
    #suite.addTest(TestBlbClient("test_create_loadbalancer"))
    #suite.addTest(TestBlbClient("test_describe_loadbalancers"))
    #suite.addTest(TestBlbClient("test_describe_loadbalancer_detail"))
    #suite.addTest(TestBlbClient("test_update_loadbalancer"))
    #suite.addTest(TestBlbClient("test_delete_loadbalancer"))
    #suite.addTest(TestBlbClient("test_create_tcp_listener"))
    #suite.addTest(TestBlbClient("test_create_udp_listener"))
    #suite.addTest(TestBlbClient("test_create_http_listener"))
    #suite.addTest(TestBlbClient("test_create_https_listener"))
    #suite.addTest(TestBlbClient("test_create_ssl_listener"))
    #suite.addTest(TestBlbClient("test_describe_tcp_listener"))
    #suite.addTest(TestBlbClient("test_describe_udp_listener"))
    #suite.addTest(TestBlbClient("test_describe_http_listener"))
    #suite.addTest(TestBlbClient("test_describe_https_listener"))
    #suite.addTest(TestBlbClient("test_describe_ssl_listener"))
    #suite.addTest(TestBlbClient("test_update_tcp_listener"))
    #suite.addTest(TestBlbClient("test_update_udp_listener"))
    #suite.addTest(TestBlbClient("test_update_http_listener"))
    #suite.addTest(TestBlbClient("test_update_https_listener"))
    #suite.addTest(TestBlbClient("test_update_ssl_listener"))
    #suite.addTest(TestBlbClient("test_delete_listeners"))
    #suite.addTest(TestBlbClient("test_add_backend_servers"))
    #suite.addTest(TestBlbClient("test_describe_health_status"))
    #suite.addTest(TestBlbClient("test_describe_backend_servers"))
    #suite.addTest(TestBlbClient("test_update_backend_servers"))
    #suite.addTest(TestBlbClient("test_remove_backend_servers"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
