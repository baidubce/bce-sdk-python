# -*- coding: utf-8 -*-

# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""
This module for test.
"""

import os
import sys
import unittest
import uuid

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

import baidubce
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.services.route import route_model
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.route import route_client

if sys.version < '3':
    reload(sys)
    sys.setdefaultencoding('utf-8')

# config parameters
vpc_id = 'vpc-qnp2czzhjtq3'
route_table_id = 'rt-i461p6vv7wn8'
route_rule_id = 'rr-qky0vq2xhihy'


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.
    :return:
    :rtype string
    """
    return str(uuid.uuid4())


generate_client_token = generate_client_token_by_uuid


class TestRouteClient(unittest.TestCase):
    """
    unit test
    """
    def setUp(self):
        """
        set up
        """
        HOST = b'bcc.bj.baidubce.com'
        AK = b''
        SK = b''
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
        self.the_client = route_client.RouteClient(config)

    def test_create_route(self):
        """
        test case for create_route
        """
        client_token = generate_client_token()
        res = self.the_client.create_route(route_table_id=route_table_id,
                                           source_address='12.0.0.0/25',
                                           destination_address='3.3.3.9/32',
                                           next_hop_id="",
                                           next_hop_type="dcGateway",
                                           description='3 sdk python dcgw single',
                                           client_token=client_token)
        print (res)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_create_et_mul_route(self):
        """
        test case for create_route
        """
        client_token = generate_client_token()
        active_route = route_model.NextHop(next_hop_id="", next_hop_type="dcGateway",
                                           path_type="ha:active");
        standby_route = route_model.NextHop(next_hop_id="", next_hop_type="dcGateway",
                                            path_type="ha:standby")
        next_hops = []
        next_hops.append(active_route)
        next_hops.append(standby_route)
        res = self.the_client.create_route(route_table_id=route_table_id,
                                           source_address='12.0.0.0/25',
                                           destination_address='3.3.3.6/32',
                                           next_hops=next_hops,
                                           description='2 sdk python dcgw mul',
                                           client_token=client_token)
        print (res)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_get_route(self):
        """
        test case for get_route
        """
        print(self.the_client.get_route(vpc_id))
        self.assertEqual(
           type(self.the_client.get_route(vpc_id)),
           baidubce.bce_response.BceResponse)

    def test_delete_route(self):
        """
        test case for delete_route
        """
        self.assertEqual(
            type(self.the_client.delete_route(route_rule_id)),
            baidubce.bce_response.BceResponse)

    def test_update_route(self):
        """
        test case for update_route
        """
        client_token = generate_client_token()
        updated_description = "Updated description"
        res = self.the_client.update_route(route_rule_id, description=updated_description, client_token=client_token)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_get_route_rule(self):
        """
        test case for get_route_rule
        """
        res = self.the_client.get_route_rule(route_rule_id)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_switch_route(self):
        """
        test case for switch_route
        """
        self.assertEqual(type(self.the_client.switch_route(route_rule_id)),
                         baidubce.bce_response.BceResponse)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(TestRouteClient("test_create_route"))
    # suite.addTest(TestRouteClient("test_get_route"))
    # suite.addTest(TestRouteClient("test_delete_route"))
    # suite.addTest(TestRouteClient("test_update_route"))
    # suite.addTest(TestRouteClient("test_get_route_rule"))
    runner = unittest.TextTestRunner()
    runner.run(suite)



