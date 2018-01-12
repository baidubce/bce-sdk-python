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
        HOST = 'eip.api-sandbox.baidu.com'
        AK = '4f4b13eda66e42e29225bb02d9193a48'
        SK = '507b4a729f6a44feab398a6a5984304d'
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
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
        billing = Billing('Postpaid', 'ByBandwidth', None, None)
        self.the_client.create_eip(1, 'cdhTest2')

    def test_resize_eip(self):
        """
        test case for resize_eip
        """
        self.the_client.resize_eip('10.107.246.132', 2)

    def test_purchase_reserved_eip(self):
        """
        test case for purchase_reserved_eip
        """
        billing = Billing(reservation_length=2)
        self.the_client.purchase_reserved_eip('10.107.245.97', billing)

    def test_bind_eip(self):
        """
        test case for bind_eip
        """
        self.the_client.bind_eip('10.107.246.132', 'BCC', 'i-7RuXDenL')

    def test_unbind_eip(self):
        """
        test case for unbind eip
        """
        self.the_client.unbind_eip('10.107.246.132')

    def test_release_eip(self):
        """
        test case for release_eip
        """
        self.the_client.release_eip('10.107.246.183')

    def test_list_eips(self):
        """
        test case for list_eips
        """
        print self.the_client.list_eips()
        # self.the_client.list_eips(eip='10.107.246.132')


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestEipClient("test_list_eips"))
    runner = unittest.TextTestRunner()
    runner.run(suite)

