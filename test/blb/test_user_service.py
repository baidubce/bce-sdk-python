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
This module for user service test.
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
from baidubce.services.blb import user_service_client

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
        self.the_client = user_service_client.UserServiceClient(config)

    def test_create_user_service(self):
        """
        test case for create user service.
        """
        client_token = generate_client_token()
        name = 'test_api_service_pub_point'
        desc = "test service"
        serviceName = "apitest"
        instanceId = "lb-000000"
        authList = [{"uid": "*", "auth": "allow"}]

        self.assertEqual(
            type(self.the_client.create_user_service(
                name, desc, serviceName, instanceId, client_token, authList)),
            baidubce.bce_response.BceResponse)

    def test_update_user_service(self):
        """
        test case for update user service
        """
        client_token = generate_client_token()
        name = 'test_api_service_pub_point'
        desc = "test service"
        service = "apitest.uservice-230ff547.beijing.baidubce.com"

        self.assertEqual(
            type(self.the_client.update_user_service(
                name, desc, service, client_token)),
            baidubce.bce_response.BceResponse)

    def test_user_service_bind_instance(self):
        """
        test case bind instance to user service
        """
        client_token = generate_client_token()
        service = "apitest.uservice-230ff547.beijing.baidubce.com"

        self.assertEqual(
            type(self.the_client.user_service_bind_instance(
                blbId, service, client_token)),
            baidubce.bce_response.BceResponse)

    def test_user_service_unbind_instance(self):
        """
        test case user service unbind instance
        """
        client_token = generate_client_token()
        service = "apitest.uservice-230ff547.beijing.baidubce.com"

        self.assertEqual(
            type(self.the_client.user_service_unbind_instance(
                service, client_token)),
            baidubce.bce_response.BceResponse)

    def test_user_service_add_auth(self):
        """
        test case add Authentication info to user service
        """
        client_token = generate_client_token()
        service = "apitest.uservice-230ff547.beijing.baidubce.com"
        authList = [{"uid": '92314acbxxxxxxxxxx', "auth": "allow"}]

        self.assertEqual(
            type(self.the_client.user_service_add_auth(
                service, authList, client_token)),
            baidubce.bce_response.BceResponse)

    def test_user_service_edit_auth(self):
        """
        test case edit Authentication info of user service
        """
        client_token = generate_client_token()
        service = "apitest.uservice-230ff547.beijing.baidubce.com"
        authList = [{"uid": '92314xxxxxxxxxxxx', "auth": "allow"}]

        self.assertEqual(
            type(self.the_client.user_service_edit_auth(
                service, authList, client_token)),
            baidubce.bce_response.BceResponse)

    def test_user_service_remove_auth(self):
        """
        test case remove Authentication info of user service
        """
        client_token = generate_client_token()
        service = "apitest.uservice-230ff547.beijing.baidubce.com"
        uidList = ['92314xxxxxxxxxxxxxxxxx']

        self.assertEqual(
            type(self.the_client.user_service_remove_auth(
                service, uidList, client_token)),
            baidubce.bce_response.BceResponse)

    def test_get_user_service_list(self):
        """
        test case get user service list information
        """
        client_token = generate_client_token()

        self.assertEqual(
            type(self.the_client.get_user_service_list(
                None, None, client_token)),
            baidubce.bce_response.BceResponse)

    def test_get_user_service_detail(self):
        """
        test case get user service detail information
        """
        client_token = generate_client_token()
        service = 'snic.uservice-d363dd71.beijing.baidubce.com'

        self.assertEqual(
            type(self.the_client.get_user_service_detail(
                service, client_token)),
            baidubce.bce_response.BceResponse)

    def test_delete_user_service(self):
        """
        test case delete user service
        """
        client_token = generate_client_token()
        service = 'snic.uservice-d363dd71.beijing.baidubce.com'

        self.assertEqual(
            type(self.the_client.delete_user_service(
                service, client_token)),
            baidubce.bce_response.BceResponse)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # 2s 2b 3s 3b~
    # suite.addTest(TestBlbClient("test_create_user_service"))
    # suite.addTest(TestBlbClient("test_update_user_service"))
    # suite.addTest(TestBlbClient("test_user_service_bind_instance"))
    # suite.addTest(TestBlbClient("test_user_service_unbind_instance"))
    # suite.addTest(TestBlbClient("test_user_service_add_auth"))
    # suite.addTest(TestBlbClient("test_user_service_edit_auth"))
    # suite.addTest(TestBlbClient("test_user_service_remove_auth"))
    # suite.addTest(TestBlbClient("test_get_user_service_list"))
    # suite.addTest(TestBlbClient("test_get_user_service_detail"))
    # suite.addTest(TestBlbClient("test_delete_user_service"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
