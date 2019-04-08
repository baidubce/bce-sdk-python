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
from baidubce.services.blb import app_blb_client

"""
# sandbox
vpc_id = b''
subnetId = b''
HOST = b''
AK = b''
SK = b''
blbId = b''
bccId = b''
bccIP = ''
appServerGroupId = ''
policyId = ''
"""

# online
vpc_id = b''
subnetId = b''
HOST = b''
AK = b''
SK = b''
blbId = b''
bccId = ''
appServerGroupId = ''
policyId = ''
portId = ''


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.
    :return:
    :rtype string
    """
    return str(uuid.uuid4())


generate_client_token = generate_client_token_by_uuid


class TestAppBlbClient(unittest.TestCase):
    """
    unit test
    """

    def setUp(self):
        """
        set up
        """
        config = BceClientConfiguration(
            credentials=BceCredentials(AK, SK), endpoint=HOST)
        self.the_client = app_blb_client.AppBlbClient(config)

    def test_create_app_loadbalancer(self):
        """
        test case for create_app_loadbalancer
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.create_app_loadbalancer(
                name='test_blb_hzf111', vpc_id=vpc_id, subnet_id=subnetId,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_update_app_loadbalancer(self):
        """
        test case for update_app_loadbalancer
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.update_app_loadbalancer(
                blbId, name=b'blb_test_hzf_new',
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_describe_app_loadbalancers(self):
        """
        test case for describe_app_loadbalancers
        """
        print(self.the_client.describe_app_loadbalancers())

    def test_describe_app_loadbalancer_detail(self):
        """
        test case for describe_app_loadbalancer_detail
        """
        print(self.the_client.describe_app_loadbalancer_detail(blbId))

    def test_delete_app_loadbalancer(self):
        """
        test case for delete_app_loadbalancer
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.delete_app_loadbalancer(
                blbId, client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_app_tcp_listener(self):
        """
        test case for create_app_tcp_listener
        """
        client_token = generate_client_token()
        #test_token = str.encode(test_token)
        self.assertEqual(
            type(self.the_client.create_app_tcp_listener(
                blbId, 1900, 'Hash', client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_app_udp_listener(self):
        """
        test case for create_app_udp_listener
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.create_app_udp_listener(
                blbId, 30000, 'Hash',
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_app_http_listener(self):
        """
        test case for create_app_http_listener
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.create_app_http_listener(
                blbId, 600, 'LeastConnection',
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_app_https_listener(self):
        """
        test case for create_app_https_listener
        """
        client_token = generate_client_token()
        cert_ids = []
        cert_ids.append('cert-6nszzxe4kj6i')
        self.assertEqual(
            type(self.the_client.create_app_https_listener(
                blbId, 800, 'LeastConnection', cert_ids,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_app_ssl_listener(self):
        """
        test case for create_ssl_listener
        """
        client_token = generate_client_token()
        cert_ids = []
        cert_ids.append('cert-6nszzxe4kj6i')
        self.assertEqual(
            type(self.the_client.create_app_ssl_listener(
                blbId, 1100, 'LeastConnection', cert_ids,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_update_app_tcp_listener(self):
        """
        test case for app tcp listener
        """
        self.assertEqual(
            type(self.the_client.update_app_tcp_listener(
                blbId, 1900, scheduler='RoundRobin')),
            baidubce.bce_response.BceResponse)

    def test_update_app_udp_listener(self):
        """
        test case for app udp listener
        """
        self.assertEqual(
            type(self.the_client.update_app_udp_listener(
                blbId, 30000, 'RoundRobin')),
            baidubce.bce_response.BceResponse)

    def test_update_app_http_listener(self):
        """
        test case for app http listener
        """
        self.assertEqual(
            type(self.the_client.update_app_http_listener(
                blbId, 600, server_timeout=750)),
            baidubce.bce_response.BceResponse)

    def test_update_app_https_listener(self):
        """
        test case for app https listener
        """
        self.assertEqual(
            type(self.the_client.update_app_https_listener(
                blbId, 800, server_timeout=800)),
            baidubce.bce_response.BceResponse)

    def test_update_app_ssl_listener(self):
        """
        test case for app ssl listener
        """
        cert_ids = []
        cert_ids.append('cert-f10dqrtjxyb7')
        self.assertEqual(
            type(self.the_client.update_app_ssl_listener(
                blbId, 1100, scheduler='RoundRobin', dual_auth=False)),
            baidubce.bce_response.BceResponse)

    def test_describe_app_tcp_listener(self):
        """
        test case for describe_app_tcp_listener
        """
        print(self.the_client.describe_app_tcp_listener(blbId))

    def test_describe_app_udp_listener(self):
        """
        test case for describe_app_udp_listener
        """
        print(self.the_client.describe_app_udp_listener(blbId))

    def test_describe_app_http_listener(self):
        """
        test case for describe_app_http_listener
        """
        print(self.the_client.describe_app_http_listener(blbId))

    def test_describe_app_https_listener(self):
        """
        test case for describe_app_https_listener
        """
        print(self.the_client.describe_app_https_listener(blbId))

    def test_describe_app_ssl_listener(self):
        """
        test case for describe_app_ssl_listener
        """
        print(self.the_client.describe_app_ssl_listener(blbId))

    def test_delete_app_listeners(self):
        """
        test case for delete app listener
        """
        client_token = generate_client_token()

        portlist = []
        portlist.append(1900)

        self.assertEqual(
            type(self.the_client.delete_app_listeners(
                blbId, portlist, client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_policys(self):
        """
            test case for create policys
        """
        client_token = generate_client_token()
        app_policy_vos = []
        rule_list = []
        app_rule = {
            'key': '*',
            'value': '*'
        }
        rule_list.append(app_rule)
        app_policy = {
            'desc': 'for test',
            'appServerGroupId': appServerGroupId,
            'backendPort': 666,
            'priority': 2334,
            'ruleList': rule_list
        }
        app_policy_vos.append(app_policy)
        self.assertEqual(
            type(self.the_client.create_policys(
                blbId, 1900, app_policy_vos)),
            baidubce.bce_response.BceResponse)

    def test_describe_policys(self):
        """
        test case for describe policys
        """
        print(self.the_client.describe_policys(blbId, 1900))

    def test_delete_policys(self):
        """
        test case for delete policys
        """
        client_token = generate_client_token()

        policyid_list = []
        policyid_list.append(policyId)

        self.assertEqual(
            type(self.the_client.delete_policys(
                blbId, 1900, policyid_list, client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_app_server_group(self):
        """
        test case for create app server group
        """
        client_token = generate_client_token()

        app_backserver = {
            'instanceId': bccId,
            'weight': 50
            #'privateIp': bccIP,
            #'portList': port_list
        }

        backserver_list = []
        backserver_list.append(app_backserver)
        self.assertEqual(
            type(self.the_client.create_app_server_group(
                blbId,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_update_app_server_group(self):
        """
        test case for update backend servers
        """
        client_token = generate_client_token()
        new_name = 'updated111'

        self.assertEqual(
            type(self.the_client.update_app_server_group(
                blbId, appServerGroupId,
                name=new_name,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_describe_app_server_group(self):
        """
        test case for describe app server group
        """
        print(self.the_client.describe_app_server_group(blbId))

    def test_delete_app_server_group(self):
        """
        test case for delete app server group
        """
        client_token = generate_client_token()

        self.assertEqual(
            type(self.the_client.delete_app_server_group(
                blbId, appServerGroupId,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_app_server_group_port(self):
        """
        test case for create app server group port
        """
        client_token = generate_client_token()

        self.assertEqual(
            type(self.the_client.create_app_server_group_port(
                blbId, appServerGroupId, 6700, 'TCP',
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_update_app_server_group_port(self):
        """
        test case for update backend servers port
        """
        client_token = generate_client_token()

        self.assertEqual(
            type(self.the_client.update_app_server_group_port(
                blbId, appServerGroupId, portId,
                health_check_timeout_insecond=10,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_delete_app_server_group_port(self):
        """
        test case for delete app server group port
        """
        client_token = generate_client_token()
        port_list = [portId]

        self.assertEqual(
            type(self.the_client.delete_app_server_group_port(
                blbId, appServerGroupId, port_list,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_create_app_blb_rs(self):
        """
        test case for create app blb rs
        """
        client_token = generate_client_token()
        backend_server_list = [{
            'instanceId': bccId,
            'weight': 56
        }]

        self.assertEqual(
            type(self.the_client.create_app_blb_rs(
                blbId, appServerGroupId, backend_server_list,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_update_app_blb_rs(self):
        """
        test case for update app blb rs
        """
        client_token = generate_client_token()
        backend_server_list = [{
            'instanceId': bccId,
            'weight': 57
        }]

        self.assertEqual(
            type(self.the_client.update_app_blb_rs(
                blbId, appServerGroupId, backend_server_list,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_describe_app_blb_rs(self):
        """
        test case for app blb rs
        """
        print(self.the_client.describe_app_blb_rs(blbId, appServerGroupId))

    def test_delete_app_blb_rs(self):
        """
        test case for delete app blb rs
        """
        client_token = generate_client_token()
        backend_server_list = []
        backend_server_list.append(bccId)

        self.assertEqual(
            type(self.the_client.delete_app_blb_rs(
                blbId, appServerGroupId, backend_server_list,
                client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_describe_rs_mount(self):
        """
        test case for describe rs mount
        """
        print(self.the_client.describe_rs_mount(blbId, appServerGroupId))

    def test_describe_rs_unmount(self):
        """
        test case for describe rs mount
        """
        print(self.the_client.describe_rs_unmount(blbId, appServerGroupId))


if __name__ == "__main__":
    suite = unittest.TestSuite()
    #suite.addTest(TestAppBlbClient("test_create_app_loadbalancer"))
    #suite.addTest(TestAppBlbClient("test_update_app_loadbalancer"))
    #suite.addTest(TestAppBlbClient("test_describe_app_loadbalancers"))
    #suite.addTest(TestAppBlbClient("test_describe_app_loadbalancer_detail"))
    #suite.addTest(TestAppBlbClient("test_delete_app_loadbalancer"))

    #suite.addTest(TestAppBlbClient("test_create_app_tcp_listener"))
    #suite.addTest(TestAppBlbClient("test_create_app_udp_listener"))
    #suite.addTest(TestAppBlbClient("test_create_app_http_listener"))
    #suite.addTest(TestAppBlbClient("test_create_app_https_listener"))
    #suite.addTest(TestAppBlbClient("test_create_app_ssl_listener"))
    #suite.addTest(TestAppBlbClient("test_update_app_tcp_listener"))
    #suite.addTest(TestAppBlbClient("test_update_app_udp_listener"))
    #suite.addTest(TestAppBlbClient("test_update_app_http_listener"))
    #suite.addTest(TestAppBlbClient("test_update_app_https_listener"))
    #suite.addTest(TestAppBlbClient("test_update_app_ssl_listener"))
    #suite.addTest(TestAppBlbClient("test_describe_app_tcp_listener"))
    #suite.addTest(TestAppBlbClient("test_describe_app_udp_listener"))
    #suite.addTest(TestAppBlbClient("test_describe_app_http_listener"))
    #suite.addTest(TestAppBlbClient("test_describe_app_https_listener"))
    #suite.addTest(TestAppBlbClient("test_describe_app_ssl_listener"))
    #suite.addTest(TestAppBlbClient("test_delete_app_listeners"))
    #suite.addTest(TestAppBlbClient("test_create_policys"))
    #suite.addTest(TestAppBlbClient("test_describe_policys"))
    #suite.addTest(TestAppBlbClient("test_delete_policys"))

    #suite.addTest(TestAppBlbClient("test_create_app_server_group"))
    #suite.addTest(TestAppBlbClient("test_update_app_server_group"))
    #suite.addTest(TestAppBlbClient("test_describe_app_server_group"))
    #suite.addTest(TestAppBlbClient("test_delete_app_server_group"))
    #suite.addTest(TestAppBlbClient("test_create_app_server_group_port"))
    #suite.addTest(TestAppBlbClient("test_update_app_server_group_port"))
    #suite.addTest(TestAppBlbClient("test_delete_app_server_group_port"))
    #suite.addTest(TestAppBlbClient("test_create_app_blb_rs"))
    #suite.addTest(TestAppBlbClient("test_update_app_blb_rs"))
    #suite.addTest(TestAppBlbClient("test_describe_app_blb_rs"))
    #suite.addTest(TestAppBlbClient("test_delete_app_blb_rs"))
    #suite.addTest(TestAppBlbClient("test_describe_rs_mount"))
    #suite.addTest(TestAppBlbClient("test_describe_rs_unmount"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
