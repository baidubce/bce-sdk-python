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

HOST = b'bcm.bj.baidubce.com'
AK = b'your ak'
SK = b'your sk'

user_id = '11111'
scope = 'BCE_BCC'
metric_name = 'CpuIdlePercent'
metric_name_batch = 'CPUUsagePercent,MemUsagePercent'
statistics = 'average,maximum,minimum'
dimensions = 'InstanceId:i-xhWSkyNb'
dimensions_batch = 'InstanceId:4c3069002046,InstanceId:b9a044ee30f2'
start_time = '2022-05-10T06:11:48Z'
end_time = '2022-05-10T07:11:48Z'
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
        test get metric data
        """
        response = self.client.get_metric_data(user_id=user_id, scope=scope, metric_name=metric_name,
                                               dimensions=dimensions, statistics=statistics, start_time=start_time,
                                               end_time=end_time, period_in_second=period_in_second)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_batch_metric_data(self):
        """
        test get batch metric data
        """
        response = self.client.get_batch_metric_data(user_id=user_id, scope=scope, metric_name=metric_name_batch,
                                                     dimensions=dimensions_batch, statistics=statistics,
                                                     start_time=start_time,
                                                     end_time=end_time, period_in_second=period_in_second)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)


if __name__ == '__main__':
    suite = unittest.TestSuite()

    # suite.addTest(TestBcmClient("test_get_metric_data"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
