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
This module for havip test.
"""

import os
import sys
import unittest
import uuid

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

import baidubce
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.havip import havip_client

if sys.version < '3':
    reload(sys)
    sys.setdefaultencoding('utf-8')

# config parameters
vpc_id = 'vpc-r625rqw3wuer'
havip_id = 'havip-w2d4kgc3x0y1'
name = "havip_test"
instance_ids = ["i-syGfPUYO"]
instance_type = "SERVER"
public_ip_address = "180.76.245.166"


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.
    :return:
    :rtype string
    """
    return str(uuid.uuid4())


generate_client_token = generate_client_token_by_uuid


class TestHavipClient(unittest.TestCase):
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
        self.the_client = havip_client.HavipClient(config)

    def test_create_havip(self):
        """
        test case for create_havip
        """
        client_token = generate_client_token()
        res = self.the_client.create_havip(name,
                                           subnet_id='sbn-dk8gl9bc',
                                           private_ip_address='192.168.0.1',
                                           description='desc',
                                           client_token=client_token)
        print(res)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_get_havip_detail_list(self):
        """
        test case for get_havip_detail_list
        """
        client_token = generate_client_token()
        
        res = self.the_client.get_havip_detail_list(vpc_id,
                                                    description='get_havip_detail_list',
                                                    client_token=client_token)
        print(res)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_delete_havip(self):
        """
        test case for delete_havip
        """
        res = self.the_client.delete_havip(havip_id)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_update_havip(self):
        """
        test case for update_havip
        """
        client_token = generate_client_token()
        updated_description = "Updated description"
        res = self.the_client.update_havip(name, havip_id, description=updated_description, client_token=client_token)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_get_havip_detail(self):
        """
        test case for get_havip_detail
        """
        res = self.the_client.get_havip_detail(havip_id)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_havip_attach_instance(self):
        """
        test case for havip_attach_instance
        """
        res = self.the_client.havip_attach_instance(instance_ids, instance_type, havip_id)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_havip_detach_instance(self):
        """
        test case for havip_detach_instance
        """
        client_token = generate_client_token()
        res = self.the_client.havip_detach_instance(instance_ids, instance_type, havip_id, client_token=client_token)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)
    
    def test_havip_bind_public_ip(self):
        """
        test case for havip_bind_public_ip
        """
        client_token = generate_client_token()
        res = self.the_client.havip_bind_public_ip(havip_id, public_ip_address, client_token=client_token)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)
    
    def test_havip_unbind_public_ip(self):
        """
        test case for havip_unbind_public_ip
        """
        client_token = generate_client_token()
        res = self.the_client.havip_unbind_public_ip(havip_id, client_token=client_token)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    #suite.addTest(TestHavipClient("test_create_havip"))
    #suite.addTest(TestHavipClient("test_get_havip_detail_list"))
    #suite.addTest(TestHavipClient("test_delete_havip"))
    #suite.addTest(TestHavipClient("test_update_havip"))
    #suite.addTest(TestHavipClient("test_get_havip_detail"))
    #suite.addTest(TestHavipClient("test_havip_attach_instance"))
    #suite.addTest(TestHavipClient("test_havip_detach_instance"))
    #suite.addTest(TestHavipClient("test_havip_bind_public_ip"))
    #suite.addTest(TestHavipClient("test_havip_unbind_public_ip"))
    runner = unittest.TextTestRunner()
    runner.run(suite)