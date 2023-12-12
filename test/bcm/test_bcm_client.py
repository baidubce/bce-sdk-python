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
from baidubce.services.bcm import bcm_client, bcm_model

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

    def test_create_namespace(self):
        """
        test create namespace
        """
        name = "Test01"
        namespace_alias = "test"
        comment = "test"
        response = self.client.create_namespace(user_id=user_id, name=name,
                                                namespace_alias=namespace_alias, comment=comment)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_batch_delete_namespace(self):
        """
        test batch delete namespaces
        """
        names = ["Test01"]
        response = self.client.batch_delete_namespaces(user_id=user_id, names=names)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_namespace(self):
        """
        test update namespace
        """
        name = "Test01"
        namespace_alias = "test01"
        comment = "test01"
        response = self.client.update_namespace(user_id=user_id, name=name,
                                                namespace_alias=namespace_alias, comment=comment)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_list_namespaces(self):
        """
        test list namespaces
        """
        response = self.client.list_namespaces(user_id=user_id)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

        name = "test"
        page_no = 1
        page_size = 10
        response = self.client.list_namespaces(user_id=user_id, name=name, page_no=page_no, page_size=page_size)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_namespace_metrics(self):
        """
        test create custom metric in one namespace
        """
        namespace = "Test01"
        metric_name_without_dimension = "TestMetric01"
        metric_alias = "test"
        unit = "sec"
        cycle = 60
        response = self.client.create_namespace_metric(user_id=user_id, namespace=namespace,
                                                       metric_name=metric_name_without_dimension,
                                                       metric_alias=metric_alias, unit=unit, cycle=cycle)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

        metric_name_dimension = "TestMetric02"
        metric_dimensions = [bcm_model.CustomDimensionModel("test", 1, alias="test")]
        response = self.client.create_namespace_metric(user_id=user_id, namespace=namespace,
                                                       metric_name=metric_name_dimension, metric_alias=metric_alias,
                                                       unit=unit, cycle=cycle, dimensions=metric_dimensions)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_batch_delete_namespace_metrics(self):
        """
        test batch delete custom metrics in one namespace
        """
        namespace = "Test01"
        ids = [1725, 1726]
        response = self.client.batch_delete_namespace_metrics(user_id=user_id, namespace=namespace, ids=ids)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_namespace_metric(self):
        """
        test update custom metric in one namespace
        """
        namespace = "Test01"
        metric_name_without_dimension = "TestMetric01"
        metric_alias = "test01"
        unit = "sec"
        cycle = 60
        response = self.client.update_namespace_metric(user_id=user_id, namespace=namespace,
                                                       metric_name=metric_name_without_dimension,
                                                       metric_alias=metric_alias, unit=unit, cycle=cycle)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_list_namespace_metrics(self):
        """
        test list custom metrics in one namespace
        """
        namespace = "Test01"
        response = self.client.list_namespace_metrics(user_id=user_id, namespace=namespace)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

        namespace = "Test01"
        metric_name = "test"
        metric_alias = "test"
        page_no = 1
        page_size = 10
        response = self.client.list_namespace_metrics(user_id=user_id, namespace=namespace, metric_name=metric_name,
                                                      metric_alias=metric_alias, page_no=page_no, page_size=page_size)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_custom_metrics(self):
        """
        test custom metric in one namespace
        """
        namespace = "Test01"
        metric_name = "TestMetric01"
        response = self.client.get_custom_metric(user_id=user_id, namespace=namespace, metric_name=metric_name)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_namespace_events(self):
        """
        test create custom event in one namespace
        """
        namespace = "Test01"
        event_name = "TestEvent01"
        event_name_alias = "test"
        event_level = bcm_model.EventLevel.NOTICE
        comment = "test"
        response = self.client.create_namespace_event(user_id=user_id, namespace=namespace, event_name=event_name,
                                                      event_name_alias=event_name_alias, event_level=event_level,
                                                      comment=comment)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_batch_delete_namespace_events(self):
        """
        test batch delete custom events in one namespace
        """
        namespace = "Test01"
        names = ["TestEvent01"]
        response = self.client.batch_delete_namespace_events(user_id=user_id, namespace=namespace, names=names)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_namespace_event(self):
        """
        test update custom event in one namespace
        """
        namespace = "Test01"
        event_name = "TestEvent01"
        event_name_alias = "test01"
        event_level = bcm_model.EventLevel.NOTICE
        comment = "test01"
        response = self.client.update_namespace_event(user_id=user_id, namespace=namespace, event_name=event_name,
                                                      event_name_alias=event_name_alias, event_level=event_level,
                                                      comment=comment)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_list_namespace_events(self):
        """
        test list custom events in one namespace
        """
        namespace = "Test01"
        response = self.client.list_namespace_events(user_id=user_id, namespace=namespace)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

        namespace = "Test01"
        event_name = "test"
        event_level = bcm_model.EventLevel.NOTICE
        page_no = 1
        page_size = 10
        response = self.client.list_namespace_events(user_id=user_id, namespace=namespace, name=event_name,
                                                     event_level=event_level, page_no=page_no, page_size=page_size)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_custom_event(self):
        """
        test custom event in one namespace
        """
        namespace = "Test01"
        event_name = "TestEvent01"
        response = self.client.get_custom_event(user_id=user_id, namespace=namespace, event_name=event_name)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)


if __name__ == '__main__':
    suite = unittest.TestSuite()

    # suite.addTest(TestBcmClient("test_get_metric_data"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
