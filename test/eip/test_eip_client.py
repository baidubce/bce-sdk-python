# -*- coding: utf-8 -*-

# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
#  of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions
# and limitations under the License.

"""
This module for test.
"""

import unittest

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.eip import eip_client
from baidubce.services.eip.model import Billing


class TestEipClient(unittest.TestCase):
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
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK),
                                        endpoint=HOST)
        self.the_client = eip_client.EipClient(config)

    def tearDown(self):
        """
        tear down
        """
        self.the_client = None

    def test_create_eip(self):
        """
        test case for create_eip
        """
        # billing = Billing('Postpaid', 'ByBandwidth', None, None)
        self.the_client.create_eip(1, 'Test')

    def test_resize_eip(self):
        """
        test case for resize_eip
        """
        self.the_client.resize_eip('x.x.x.x', 3)

    def test_purchase_reserved_eip(self):
        """
        test case for purchase_reserved_eip
        """
        billing = Billing(reservation_length=1)
        self.the_client.purchase_reserved_eip('x.x.x.x', billing)

    def test_bind_eip(self):
        """
        test case for bind_eip
        """
        self.the_client.bind_eip('x.x.x.x', 'BCC', 'i-Dl6AvB0X')

    def test_unbind_eip(self):
        """
        test case for unbind eip
        """
        self.the_client.unbind_eip('x.x.x.x')

    def test_release_eip(self):
        """
        test case for release_eip
        """
        self.the_client.release_eip('x.x.x.x')

    def test_list_eips(self):
        """
        test case for list_eips
        """
        print((self.the_client.list_eips()))
        # self.the_client.list_eips(eip='x.x.x.x')


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(TestEipClient("test_list_eips"))
    # suite.addTest(TestEipClient("test_release_eip"))
    # suite.addTest(TestEipClient("test_create_eip"))
    # suite.addTest(TestEipClient("test_resize_eip"))
    # suite.addTest(TestEipClient("test_purchase_reserved_eip"))
    # suite.addTest(TestEipClient("test_bind_eip"))
    # suite.addTest(TestEipClient("test_unbind_eip"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
