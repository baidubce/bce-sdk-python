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
Unit tests for dcc client.
"""

import unittest

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.dcc import dcc_client


class TestDccClient(unittest.TestCase):
    """
    unit test
    """
    def setUp(self):
        """
        set up
        """
        HOST = 'dcc.api-sandbox.baidu.com'
        AK = '4f4b13eda66e42e29225bb02d9193a48'
        SK = '507b4a729f6a44feab398a6a5984304d'
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)
        self.the_client = dcc_client.DccClient(config)

    def tearDown(self):
        """
        tear down
        """
        self.the_client = None

    def test_list_dedicated_hosts(self):
        """
        test case for list dedicatedHosts
        """
        print self.the_client.list_dedicated_hosts()

    def test_get_dedicated_host(self):
        """
        test case for get dedicatedHost
        """
        self.the_client.get_dedicated_host('d-MPgs6jPr')

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestDccClient("test_list_dedicated_hosts"))
    # suite.addTest(TestDccClient("test_get_dedicated_host"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
