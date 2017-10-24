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
reload(sys)
sys.setdefaultencoding('utf-8')

import baidubce
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.route import route_client

vpc_id = 'vpc-8dpfkp4e4f46'
route_table_id = 'rt-j0vaaviaggpt'
route_rule_id = 'rr-2fjn3rx9imj8'




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
        HOST = 'bcc.bce-api.baidu.com'
        AK = '4f4b13eda66e42e29225bb02d9193a48'
        SK = '507b4a729f6a44feab398a6a5984304d'
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
        self.the_client = route_client.RouteClient(config)

    def test_create_route(self):
        """
        test case for create_route
        """
        client_token = generate_client_token()
        self.assertEqual(
            type(self.the_client.create_route(route_table_id,
                                              '192.168.241.0/24',
                                              '3.3.3.3/32',
                                              'custom', 'test', 'i-kcZqtDGO',
                                              client_token=client_token)),
            baidubce.bce_response.BceResponse)

    def test_get_route(self):
        """
        test case for get_route
        """
        print self.the_client.get_route(route_table_id=route_table_id)

        #self.assertEqual(
        #    type(self.the_client.get_route(vpc_id)),
        #    baidubce.bce_response.BceResponse)

    def test_delete_route(self):
        """
        test case for delete_route
        """
        self.assertEqual(
            type(self.the_client.delete_route(route_rule_id)),
            baidubce.bce_response.BceResponse)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    #suite.addTest(TestRouteClient("test_create_route"))
    suite.addTest(TestRouteClient("test_get_route"))
    #suite.addTest(TestRouteClient("test_delete_route"))
    runner = unittest.TextTestRunner()
    runner.run(suite)

