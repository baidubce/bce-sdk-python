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
Unit tests for bcm client.
"""
import sys
import unittest

import baidubce
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.bcm import bcm_client

PY2 = sys.version_info[0] == 2
if PY2:
    reload(sys)
    sys.setdefaultencoding('utf8')

HOST = b'http://bcm.su.baidubce.com'
AK = b'******'
SK = b'******'

user_id = '3ee0963f14df46be830f5a287ce90ab2'
scope = 'BCE_BCC'
metric_name = 'CpuIdlePercent'
statistics = 'average,maximum,minimum'
dimensions = 'InstanceId:i-xhWSkyNb'
start_time = '2020-09-22T10:02:00Z'
end_time = '2020-09-22T11:01:21Z'
period_in_second = 60


class TestBcmClient(unittest.TestCase):
    """
    Test class for bcm sdk client
    """

    def setUp(self):
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK),
                                        endpoint=HOST)
        self.client = bcm_client.BcmClient(config)

    def test_get_metric_data(self):
        """
        test create bbc instance
        """
        response = self.client.get_metric_data(user_id=user_id, scope=scope, metric_name=metric_name,
                                               dimensions=dimensions, statistics=statistics, start_time=start_time,
                                               end_time=end_time, period_in_second=period_in_second)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)


if __name__ == '__main__':
    suite = unittest.TestSuite()

    #suite.addTest(TestBcmClient("test_get_metric_data"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
