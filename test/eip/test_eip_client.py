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
from baidubce.services.eip.model import Billing, EipStatus


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
        print((self.the_client.list_eips(status=EipStatus.BINDED)))

    def test_start_auto_renew_eip(self):
        """
        test case for start_auto_renew_eip
        """
        self.the_client.start_auto_renew_eip('x.x.x.x', 'Month', 1)

    def test_stop_auto_renew_eip(self):
        """
        test case for stop_auto_renew_eip
        """
        self.the_client.stop_auto_renew_eip('x.x.x.x')

    def test_direct_eip(self):
        """
        test case for direct_eip
        """
        self.the_client.direct_eip('x.x.x.x')
    
    def test_undirect_eip(self):
        """
        test case for undirect_eip
        """
        self.the_client.undirect_eip('x.x.x.x')
    
    def test_list_eip_recycle(self):
        """
        test case for list_eip_recycle
        """
        print(self.the_client.list_eip_recycle())
        print(self.the_client.list_eip_recycle('x.x.x.x'))

    def test_optional_delete_eip(self):
        """
        test case for optional_delete_eip
        """
        self.the_client.optional_delete_eip('x.x.x.x', False)
    
    def test_restore_recycle_eip(self):
        """
        test case for restore_recycle_eip
        """
        self.the_client.restore_recycle_eip('x.x.x.x')

    def test_delete_recycle_eip(self):
        """
        test case for delete_recycle_eip
        """
        self.the_client.delete_recycle_eip('x.x.x.x')
    


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(TestEipClient("test_list_eips"))
    # suite.addTest(TestEipClient("test_release_eip"))
    # suite.addTest(TestEipClient("test_create_eip"))
    # suite.addTest(TestEipClient("test_resize_eip"))
    # suite.addTest(TestEipClient("test_purchase_reserved_eip"))
    # suite.addTest(TestEipClient("test_bind_eip"))
    # suite.addTest(TestEipClient("test_unbind_eip"))
    # suite.addTest(TestEipClient("test_list_eip_recycle"))
    # suite.addTest(TestEipClient("test_optional_delete_eip"))
    # suite.addTest(TestEipClient("test_restore_recycle_eip"))
    # suite.addTest(TestEipClient("test_delete_recycle_eip"))
    # suite.addTest(TestEipClient("test_start_auto_renew_eip"))
    # suite.addTest(TestEipClient("test_stop_auto_renew_eip"))
    # suite.addTest(TestEipClient("test_direct_eip"))
    # suite.addTest(TestEipClient("test_undirect_eip"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
