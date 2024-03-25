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
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.probe import probe_client

if sys.version < '3':
    reload(sys)
    sys.setdefaultencoding('utf-8')

# config parameters
vpc_id = ''
subnet_id = ''


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.
    :return:
    :rtype string
    """
    return str(uuid.uuid4())


generate_client_token = generate_client_token_by_uuid


class TestProbeClient(unittest.TestCase):
    """
    unit test
    """
    probe_id = ''

    def setUp(self):
        """
        set up
        """
        HOST = b'bcc.bj.baidubce.com'
        AK = b''
        SK = b''
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
        self.the_client = probe_client.ProbeClient(config)


    def test_create_probe(self):
        """
        test case for create_probe
        """
        client_token = generate_client_token()
        src_ip_list = []
        res = self.the_client.create_probe(name='test',
                                           vpc_id=vpc_id,
                                           subnet_id=subnet_id,
                                           protocol='UDP',
                                           frequency=10,
                                           dst_ip='192.168.0.4',
                                           dst_port='80',
                                           source_ips=src_ip_list,
                                           source_ip_num=1,
                                           payload='test_create',
                                           client_token=client_token)
        print(res)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_list_probes(self):
        """
        test case for list_probes
        """
        res = self.the_client.list_probes()
        print(res)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_get_probe(self):
        """
        test case for get_probe
        """
        res = self.the_client.get_probe(self.probe_id)
        print(res)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_update_probe(self):
        """
        test case for update_probe
        """
        client_token = generate_client_token()
        res = self.the_client.update_probe(self.probe_id,
                                           name="test_update",
                                           dst_ip='192.168.0.10',
                                           dst_port='22',
                                           frequency=30,
                                           payload='test_update',
                                           client_token=client_token)
        print(res)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)

    def test_delete_probe(self):
        """
        test case for delete_probe
        """
        client_token = generate_client_token()
        res = self.the_client.delete_probe(self.probe_id,
                                           client_token=client_token)
        print(res)
        self.assertEqual(type(res), baidubce.bce_response.BceResponse)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestProbeClient("test_create_probe"))
    suite.addTest(TestProbeClient("test_list_probes"))
    suite.addTest(TestProbeClient("test_get_probe"))
    suite.addTest(TestProbeClient("test_update_probe"))
    suite.addTest(TestProbeClient("test_get_probe"))
    suite.addTest(TestProbeClient("test_delete_probe"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
