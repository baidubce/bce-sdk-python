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
This module for et gateway test.
"""

import os
import sys
import unittest
import uuid

from baidubce.services.etGateway import et_gateway_client
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')


NAME = 'dcGateway'
VPC_ID = 'vpc-IyrqYIQ7'
SPEED = 100
ET_ID = 'dcphy-478px3km77dh'
CHANNEL_ID = 'dedicatedconn-i7c1skfd0djs'
LOCAL_CIDRS = ['10.243.87.0/24']
DESCRIPTION = 'test et gateway'
ET_GATEWAY_ID = 'dcgw-4ds9x3kmds88'


class TestETGatewayClient(unittest.TestCase):
    """
    Test class for et gateway sdk client
    """

    def setUp(self):
        """
        set up
        """
        HOST = b'bcc.bj.baidubce.com'
        AK = b''
        SK = b''

        config = BceClientConfiguration(
            credentials=BceCredentials(AK, SK), endpoint=HOST)
        self.client = et_gateway_client.EtGatewayClient(config)

    def tearDown(self):
        """
        tear down
        """
        self.client = None

    def test_create_et_gateway(self):
        """
        test case for creating et gateway
        """
        client_token = generate_client_token()
        self.client.create_et_gateway(client_token=client_token,
                                      name=NAME,
                                      vpc_id=VPC_ID,
                                      speed=SPEED,
                                      description=DESCRIPTION,
                                      local_cidrs=LOCAL_CIDRS,
                                      et_id=ET_ID,
                                      channel_id=CHANNEL_ID,
                                      config=None)

    def test_update_et_gateway(self):
        """
        test case for updating et gateway
        """
        client_token = generate_client_token()
        self.client.update_et_gateway(client_token=client_token,
                                      et_gateway_id=ET_GATEWAY_ID,
                                      name=NAME,
                                      description=DESCRIPTION,
                                      speed=SPEED,
                                      local_cidrs=LOCAL_CIDRS,
                                      config=None)

    def test_delete_et_gateway(self):
        """
        test case for deleting et gateway
        """
        client_token = generate_client_token()
        self.client.delete_et_gateway(client_token=client_token,
                                      et_gateway_id=ET_GATEWAY_ID,
                                      config=None)

    def test_bind_et(self):
        """
        test case for binding et gateway
        """
        client_token = generate_client_token()
        self.client.bind_et(client_token=client_token,
                            et_gateway_id=ET_GATEWAY_ID,
                            et_id=ET_ID,
                            channel_id=CHANNEL_ID,
                            local_cidrs=LOCAL_CIDRS,
                            config=None)

    def test_unbind_et(self):
        """
        test case for unbinding et gateway
        """
        client_token = generate_client_token()
        self.client.unbind_et(client_token=client_token,
                              et_gateway_id=ET_GATEWAY_ID,
                              config=None)

    def test_list_et_gateway(self):
        """
        test case for listing et gateway
        """
        self.client.list_et_gateway(vpc_id=VPC_ID,
                                    et_gateway_id=ET_GATEWAY_ID,
                                    name=NAME,
                                    status=None,
                                    marker=None,
                                    max_keys=None)

    def test_get_et_gateway(self):
        """
        test case for getting et gateway
        """
        self.client.get_et_gateway(et_gateway_id=ET_GATEWAY_ID,
                                   config=None)

    def test_create_health_check(self):
        """
        test case for creating health check
        """
        client_token = generate_client_token()
        self.client.create_health_check(client_token=client_token,
                                        et_gateway_id=ET_GATEWAY_ID,
                                        health_check_source_ip=None,
                                        health_check_type=None,
                                        health_check_port=None,
                                        health_check_interval=3,
                                        health_check_threshold=2,
                                        unhealth_threshold=2,
                                        auto_generate_route_rule=True,
                                        config=None)


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

    # suite.addTest(TestETGatewayClient("test_create_et_gateway"))
    # suite.addTest(TestETGatewayClient("test_update_et_gateway"))
    # suite.addTest(TestETGatewayClient("test_delete_et_gateway"))
    # suite.addTest(TestETGatewayClient("test_bind_et"))
    # suite.addTest(TestETGatewayClient("test_unbind_et"))
    # suite.addTest(TestETGatewayClient("test_list_et_gateway"))
    # suite.addTest(TestETGatewayClient("test_get_et_gateway"))
    # suite.addTest(TestETGatewayClient("test_create_health_check"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
