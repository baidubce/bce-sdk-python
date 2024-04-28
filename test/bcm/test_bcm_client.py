#-*- coding: UTF-8 -*-
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
from baidubce.services.bcm.bcm_model import SiteOnceConfig

PY2 = sys.version_info[0] == 2
if PY2:
    reload(sys)
    sys.setdefaultencoding('utf8')

HOST = b'bcm.bj.baidubce.com'
AK = b'ak'
SK = b'sk'

user_id = '11111'
app_name = "app_name"
scope = 'BCE_BCC'
metric_name = 'CpuIdlePercent'
metric_name_batch = 'CPUUsagePercent,MemUsagePercent'
statistics = 'average,maximum,minimum'
dimensions = 'InstanceId:i-ysNRS8Vs'
dimensions_batch = 'InstanceId:i-JJlYmXGi,InstanceId:i-OyWnVQc9'
start_time = '2023-09-10T06:11:48Z'
end_time = '2023-09-10T07:11:48Z'
period_in_second = 60
custom_namespace = "test_qsh"
custom_metric_name = "taasd"

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

    def test_list_notify_group(self):
        """
        test list notify group
        """
        response = self.client.list_notify_group(page_no=1, page_size=10)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_list_notify_party(self):
        """
        test list notify party
        """
        response = self.client.list_notify_party(name="test", page_no=1, page_size=5)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_action(self):
        """
        test create action
        """
        notification = bcm_model.Notification("EMAIL")
        member = bcm_model.Member("notifyParty", "56c9e0e2138c4f", "lzs")
        response = self.client.create_action(user_id, [notification], [member], "test_wjr_py")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_delete_action(self):
        """
        test delete action
        """
        response = self.client.delete_action(user_id=user_id, name="bb832cf9-ce5e-4c59-85a0-4ddf30******")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_list_action(self):
        """
        test list action
        """
        response = self.client.list_action(user_id=user_id, page_no=1, page_size=5, name="test")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_action(self):
        """
        test update action
        """
        notification = bcm_model.Notification("EMAIL")
        member = bcm_model.Member("notifyParty", "56c9e0e2138c4f", "lzs")
        response = self.client.update_action(user_id=user_id, notifications=[notification], members=[member],
                                             alias="test_wjr_py",
                                             disable_times=[], action_callbacks=[],
                                             name="2185c71a-9132-4b4e-92d2-35eebd******")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_log_extract(self):
        """
        test log extract
        """
        extract_rule = ("800] \"(?<method>(GET|POST|PUT|DELETE)) .*/v1/dashboard/metric/(?<widget>("
                        "cycle|trend|report|billboard|gaugechart)) HTTP/1.1\".* (?<resTime>[0-9]+)ms")
        log_example = ("10.157.16.207 - - [09/Apr/2020:20:45:33 +0800] \"POST /v1/dashboard/metric/gaugechart "
                       "HTTP/1.1\" 200 117 109ms")
        response = self.client.log_extract(user_id=user_id, extract_rule=extract_rule, log_example=log_example)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_query_metric_meta_for_application(self):
        """
        test query metric meta for_application
        """
        response = self.client.query_metric_meta_for_application(user_id=user_id, app_name="test14",
                                                                 task_name="79c35af26c4346ab844bcbcdde******",
                                                                 metric_name="log.responseTime",
                                                                 dimension_keys=["method"])
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_query_metric_data_for_application(self):
        """
        test query metric data for_application
        """
        response = self.client.query_metric_data_for_application(user_id=user_id, app_name="zmq-log-1115",
                                                                 task_name="6d3f07e6684d47b69ca9600f7f******",
                                                                 metric_name="exec.6d3f07e6684d47b69ca9600f7f******.me",
                                                                 start_time="2023-12-05T09:54:15Z",
                                                                 end_time="2023-12-05T10:04:15Z",
                                                                 instances=["0.zmq-log-1115"],
                                                                 statistics=["average", "maximum"])
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_list_alarm_metrics_for_application(self):
        """
        test list alarm metrics for application
        """
        response = self.client.list_alarm_metrics_for_application(user_id=user_id, app_name="test_ymd_app_0918",
                                                                  task_name="46e78b2831394f738429f88265******",
                                                                  search_name="test_name")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_alarm_policy_for_application(self):
        """
        test get alarm policy for application
        """
        response = self.client.get_alarm_policy_for_application(user_id=user_id, app_name="test_ymd_app_0918",
                                                                alarm_name="inst-test")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_delete_alarm_policy_for_application(self):
        """
        test delete alarm policy for application
        """
        response = self.client.delete_alarm_policy_for_application(user_id=user_id, app_name="uuu", alarm_name="dasd")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_list_alarm_policy_for_application(self):
        """
        test list alarm policy for application
        """
        response = self.client.list_alarm_policy_for_application(user_id=user_id, page_no=1, src_type="PORT")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_alarm_policy_for_application(self):
        """
        test create alarm policy for application
        """
        monito_object_view = bcm_model.ApplicationObjectView("zmq-log-1115.453bf9588c9e488f9ba2c98412******")
        monitor_object = bcm_model.ApplicationMonitorObject("APP", [monito_object_view])
        rule = bcm_model.ApplicationAlarmRule("log.ab3b543f41974e26ab984d94fc******.log_metric", "log_metric",
                                              60, "average", 10, ">", 1,
                                              0, [])
        response = self.client.create_alarm_policy_for_application(user_id, "", "test_wjr_py",
                                                                   "zmq-log-1115", "APP",
                                                                   monitor_object, "ab3b543f41974e26ab984d94fc******",
                                                                   "LOG", "INSTANCE", "MAJOR",
                                                                   [[rule]], incident_actions=["624c99b5-5436-478c"
                                                                                               "-8326-0efc81******"])
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_alarm_policy_for_application(self):
        """
        test update alarm policy for application
        """
        monito_object_view = bcm_model.ApplicationObjectView("zmq-log-1115.453bf9588c9e488f9ba2c98412******")
        monitor_object = bcm_model.ApplicationMonitorObject("APP", [monito_object_view])
        rule = bcm_model.ApplicationAlarmRule("log.ab3b543f41974e26ab984d94fc******.log_metric2", "log_metric2",
                                              60, "average", 10, ">", 1,
                                              0, [])
        response = self.client.update_alarm_policy_for_application(user_id, "", "test_wjr_py",
                                                                   "zmq-log-1115", "APP",
                                                                   monitor_object, "ab3b543f41974e26ab984d94fc******",
                                                                   "LOG", "INSTANCE", "MAJOR",
                                                                   [[rule]], incident_actions=[
                "624c99b5-5436-478c-8326-0efc81******"])
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_application_data(self):
        response = self.client.create_application_data(app_name, "BCC", user_id, "testAlias-1213", "description-1213")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_application_data_list(self):
        response = self.client.get_application_data_list(user_id, 1, 10)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_application_data(self):
        response = self.client.update_application_data(user_id, "5401", app_name, "BCC", "test", "t1")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_delete_application_data(self):
        response = self.client.delete_application_data(user_id, "test_1213")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_application_instance_list(self):
        response = self.client.get_application_instance_list(user_id, "bj", "test_1213", "name",
                                                             1, 10, "bsm")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_application_instance(self):
        host_list = [{
            "instanceId": "7d4e09af-d01b-4492-88e9-c27d90967f0b",
            "region": "bj"
        }, {
            "instanceId": "d8293318-7d34-433e-928a-b0e72cb3f3ba",
            "region": "bj"
        }]
        response = self.client.create_application_instance(user_id, app_name, host_list)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_application_instance_created_list(self):
        response = self.client.get_application_instance_created_list(user_id, app_name, "bj")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_delete_application_instance(self):
        response = self.client.delete_application_instance(user_id, app_name, "7099")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_application_instance_task(self):
        response = self.client.create_application_instance_task(user_id, app_name, "task_proc_test",
                                                                0, "/proc/exe", 300)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_application_instance_log_task(self):
        log_example = "namespace:04b91096-a294-477d-bd11-1a7bcfb5a921\n"
        match_rule = "namespace:(?P<namespace>[0-9a-fA-F-]+)"
        rate = 5
        extract_result = [{
            "extractFieldName": "namespace",
            "extractFieldValue": "04b91096-a294-477d-bd11-1a7bcfb5a921",
            "dimensionMapTable": "namespaceTable"
        }]
        metrics = [
            {
                "metricName": "space",
                "saveInstanceData": 1,
                "valueFieldType": 0,
                "aggrTags": [
                    {
                        "range": "App",
                        "tags": ""
                    },
                    {
                        "range": "App",
                        "tags": "namespace"
                    }
                ],
                "metricAlias": "",
                "metricUnit": "",
                "valueFieldName": ""
            }
        ]
        response = self.client.create_application_instance_task(user_id, app_name, "task_log_test", 2, "/bin/log/info",
                                                                60, "test_description", log_example, match_rule, rate,
                                                                extract_result, metrics)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_application_monitor_task_detail(self):
        task_name = "9b67163479fe4ffcb31a8a79aaf14cf9"
        response = self.client.get_application_monitor_task_detail(user_id, app_name, task_name)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_application_monitor_task_list(self):
        response = self.client.get_application_monitor_task_list(user_id, app_name)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_application_monitor_task(self):
        response = self.client.update_application_monitor_task(user_id, app_name, "task_proc_test",
                                                                "9b67163479fe4ffcb31a8a79aaf14cf9",
                                                               0, "/proc/bin", 300, "test_description")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_application_monitor_log_task(self):
        log_example = "namespace:04b91096-a294-477d-bd11-1a7bcfb5a921\n"
        match_rule = "namespace:(?P<namespace>[0-9a-fA-F-]+)"
        rate = 5
        extract_result = [{
            "extractFieldName": "namespace",
            "extractFieldValue": "04b91096-a294-477d-bd11-1a7bcfb5a921",
            "dimensionMapTable": "namespaceTable"
        }]
        metrics = [
            {
                "metricName": "space",
                "saveInstanceData": 1,
                "valueFieldType": 0,
                "aggrTags": [
                    {
                        "range": "App",
                        "tags": ""
                    },
                    {
                        "range": "App",
                        "tags": "namespace"
                    }
                ],
                "metricAlias": "",
                "metricUnit": "",
                "valueFieldName": ""
            }
        ]
        response = self.client.update_application_monitor_task(user_id, app_name, "task_log_test01", "424c68d575d24ef7bcd0b3f5e72643a2",
                                                               2, "/bin/log/info",60, "test_description01", log_example, match_rule, rate,
                                                                extract_result, metrics)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_delete_application_monitor_task(self):
        response = self.client.delete_application_monitor_task(user_id, "424c68d575d24ef7bcd0b3f5e72643a2", app_name)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_application_dimension_table(self):
        response = self.client.create_application_dimension_table(user_id, app_name, "test_table",
                                                                  "a=>1\nb=>2")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_application_dimension_table_list(self):
        response = self.client.get_application_dimension_table_list(user_id, app_name, "test")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_application_dimension_table(self):
        response = self.client.update_application_dimension_table(user_id, app_name, "test_table",
                                                                  "a=>1")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_delete_application_dimension_table(self):
        response = self.client.delete_application_dimension_table(user_id, app_name, "test_table")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)


    def test_get_dashboard(self):
        dashboard_name = '_54507'
        response = self.client.get_dashboard(user_id=user_id, dashboard_name=dashboard_name)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_dashboard(self):
        title = 'yyy-python3'
        dashboard_type = 'common'
        configure = "{\"tabs\":[{\"dimensions\":[],\"metric\":[],\"name\":\"\",\"namespace\":[],\"widgets\":[[{\"name\":\"_54382_54383\"},{\"name\":\"_54382_54384\"},{\"name\":\"_54382_54385\"}],[{\"name\":\"_54382_54386\"}]]}]}"
        response = self.client.create_dashboard(user_id=user_id, configure=configure,
                                                title=title, dashboard_type=dashboard_type)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_dashboard(self):
        dashboard_name = '_54550'
        title = 'yyy-python-update2'
        dashboard_type = 'common'
        configure = "{\"tabs\":[{\"dimensions\":[],\"metric\":[],\"name\":\"\",\"namespace\":[],\"widgets\":[[{\"name\":\"_54382_54383\"},{\"name\":\"_54382_54384\"},{\"name\":\"_54382_54385\"}],[{\"name\":\"_54382_54386\"}]]}]}"
        response = self.client.update_dashboard(user_id=user_id, configure=configure,
                                                title=title, dashboard_type=dashboard_type,
                                                dashboard_name=dashboard_name)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_delete_dashboard(self):
        dashboard_name = '_54549'
        response = self.client.delete_dashboard(user_id=user_id, dashboard_name=dashboard_name)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_duplicate_dashboard(self):
        dashboard_name = '_54579'
        response = self.client.duplicate_dashboard(user_id=user_id, dashboard_name=dashboard_name)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_dashboard_widget(self):
        dashboard_name = '_54579'
        widget_name = '_54579_54586'
        response = self.client.get_dashboard_widget(user_id=user_id, dashboard_name=dashboard_name
                                                    , widget_name=widget_name)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_dashboard_widget(self):
        dashboard_name = '_54579'
        response = self.client.create_dashboard_widget(user_id=user_id, dashboard_name=dashboard_name)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_delete_dashboard_widget(self):
        dashboard_name = '_54579'
        widget_name = '_54579_54586'
        response = self.client.delete_dashboard_widget(user_id=user_id, dashboard_name=dashboard_name
                                                       , widget_name=widget_name)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_duplicate_dashboard_widget(self):
        dashboard_name = '_54579'
        widget_name = '_54579_54584'
        response = self.client.duplicate_dashboard_widget(user_id=user_id, dashboard_name=dashboard_name
                                                          , widget_name=widget_name)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_dashboard_widget(self):
        dashboard_name = '_54579'
        widget_name = '_54579_54584'
        widget_type = 'trend'
        title = 'bccNew'
        configure = {
            "data": [
                {
                    "metric": [
                        {
                            "name": "CpuIdlePercent",
                            "unit": "%",
                            "alias": "CPU空闲率",
                            "contrast": [],
                            "timeContrast": [],
                            "statistics": "avg"
                        }
                    ],
                    "monitorObject": [
                        {
                            "instanceName": "zmq-as0001 ",
                            "id": "i-yq8qU5Qf"
                        }
                    ],
                    "scope": "BCE_BCC",
                    "subService": "linux",
                    "region": "bj",
                    "scopeValue": {
                        "name": "BCC",
                        "value": "BCE_BCC",
                    },
                    "resourceType": "Instance",
                    "monitorType": "scope",
                    "namespace": [
                        {
                            "namespaceType": "instance",
                            "transfer": "",
                            "filter": "",
                            "name": "i-yq8qU5Qf___bj.BCE_BCC.453bf9588c9e488f9ba2c984129090dc",
                            "instanceName": "zmq-as0001 ",
                            "region": "bj",
                            "bcmService": "BCE_BCC",
                            "subService": [
                                {
                                    "name": "serviceType",
                                    "value": "linux"
                                }
                            ]
                        }
                    ],
                    "product": "453bf9588c9e488f9ba2c984129090dc"
                }
            ],
            "style": {
                "displayType": "line",
                "nullPointMode": "zero",
                "threshold": 0,
                "decimals": 2,
                "isEdit": "true",
                "unit": "%"
            },
            "title": "bccNew",
            "timeRange": {
                "timeType": "dashboard",
                "unit": "minutes",
                "number": 1,
                "relative": "today()"
            },
            "time": "",
            "monitorType": "scope"
        }
        response = self.client.update_dashboard_widget(user_id=user_id, dashboard_name=dashboard_name,
                                                       widget_name=widget_name, widget_type=widget_type,
                                                       title=title, configure=configure, )
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_dashboard_report_data(self):
        data = [
            {
                "metric": [
                    {
                        "alias": "CPU空闲率",
                        "cycle": 30,
                        "displayName": "cpu",
                        "name": "CpuIdlePercent",
                        "statistics": "avg",
                        "unit": "%"
                    }
                ],
                "monitorObject": [
                    {
                        "id": "i-isvkUW76",
                        "instanceName": "instance-xcy9049y "
                    }
                ],
                "monitorType": "scope",
                "namespace": [
                    {
                        "bcmService": "BCE_BCC",
                        "instanceName": "instance-xcy9049y ",
                        "name": "i-isvkUW76___bj.BCE_BCC.a0d04d7c202140cb80155ff7b6752ce4",
                        "namespaceType": "app",
                        "region": "bj",
                        "subService": [
                            {
                                "name": "serviceType",
                                "value": "linux"
                            }
                        ],
                        "transfer": ""
                    }
                ],
                "product": "a0d04d7c202140cb80155ff7b6752ce4",
                "region": "bj",
                "scope": "BCE_BCC",
                "scopeValue": {
                    "name": "BCC",
                    "value": "BCE_BCC"
                },
                "subService": "linux"
            }
        ]

        time = "2023-12-08 09:10:59|2023-12-08 10:10:59"
        response = self.client.get_dashboard_report_data(data=data, time=time, config=None)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_dashboard_trend_data(self):
        data = [
            {
                "metric": [
                    {
                        "alias": "CPU空闲率",
                        "cycle": 30,
                        "displayName": "cpu",
                        "name": "CpuIdlePercent",
                        "statistics": "avg",
                        "unit": "%"
                    }
                ],
                "monitorObject": [
                    {
                        "id": "i-isvkUW76",
                        "instanceName": "instance-xcy9049y "
                    }
                ],
                "monitorType": "scope",
                "namespace": [
                    {
                        "bcmService": "BCE_BCC",
                        "instanceName": "instance-xcy9049y ",
                        "name": "i-isvkUW76___bj.BCE_BCC.a0d04d7c202140cb80155ff7b6752ce4",
                        "namespaceType": "app",
                        "region": "bj",
                        "subService": [
                            {
                                "name": "serviceType",
                                "value": "linux"
                            }
                        ],
                        "transfer": ""
                    }
                ],
                "product": "a0d04d7c202140cb80155ff7b6752ce4",
                "region": "bj",
                "scope": "BCE_BCC",
                "scopeValue": {
                    "name": "BCC",
                    "value": "BCE_BCC"
                },
                "subService": "linux"
            }
        ]
        time = "2023-12-08 09:10:59|2023-12-08 09:11:59"
        response = self.client.get_dashboard_trend_data(data=data, time=time, config=None)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_dashboard_gauge_chart_data(self):
        data = [
            {
                "metric": [
                    {
                        "alias": "CPU空闲率",
                        "cycle": 30,
                        "displayName": "cpu",
                        "name": "CpuIdlePercent",
                        "statistics": "avg",
                        "unit": "%"
                    }
                ],
                "monitorObject": [
                    {
                        "id": "i-isvkUW76",
                        "instanceName": "instance-xcy9049y "
                    }
                ],
                "monitorType": "scope",
                "namespace": [
                    {
                        "bcmService": "BCE_BCC",
                        "instanceName": "instance-xcy9049y ",
                        "name": "i-isvkUW76___bj.BCE_BCC.a0d04d7c202140cb80155ff7b6752ce4",
                        "namespaceType": "app",
                        "region": "bj",
                        "subService": [
                            {
                                "name": "serviceType",
                                "value": "linux"
                            }
                        ],
                        "transfer": ""
                    }
                ],
                "product": "a0d04d7c202140cb80155ff7b6752ce4",
                "region": "bj",
                "scope": "BCE_BCC",
                "scopeValue": {
                    "name": "BCC",
                    "value": "BCE_BCC"
                },
                "subService": "linux"
            }
        ]
        time = "2023-12-08 09:10:59|2023-12-08 09:11:59"
        response = self.client.get_dashboard_gauge_chart_data(data=data, time=time, config=None)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_dashboard_billboard_data(self):
        data = [
            {
                "metric": [
                    {
                        "alias": "CPU空闲率",
                        "cycle": 30,
                        "displayName": "cpu",
                        "name": "CpuIdlePercent",
                        "statistics": "avg",
                        "unit": "%"
                    }
                ],
                "monitorObject": [
                    {
                        "id": "i-isvkUW76",
                        "instanceName": "instance-xcy9049y "
                    }
                ],
                "monitorType": "scope",
                "namespace": [
                    {
                        "bcmService": "BCE_BCC",
                        "instanceName": "instance-xcy9049y ",
                        "name": "i-isvkUW76___bj.BCE_BCC.a0d04d7c202140cb80155ff7b6752ce4",
                        "namespaceType": "app",
                        "region": "bj",
                        "subService": [
                            {
                                "name": "serviceType",
                                "value": "linux"
                            }
                        ],
                        "transfer": ""
                    }
                ],
                "product": "a0d04d7c202140cb80155ff7b6752ce4",
                "region": "bj",
                "scope": "BCE_BCC",
                "scopeValue": {
                    "name": "BCC",
                    "value": "BCE_BCC"
                },
                "subService": "linux"
            }
        ]
        time = "2023-12-08 09:10:59|2023-12-08 09:11:59"
        response = self.client.get_dashboard_billboard_data(data=data, time=time, config=None)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_dashboard_trend_senior_data(self):
        data = [
            {
                "metric": [
                    {
                        "alias": "CPU空闲率",
                        "cycle": 30,
                        "displayName": "cpu",
                        "name": "CpuIdlePercent",
                        "statistics": "avg",
                        "unit": "%"
                    }
                ],
                "monitorObject": [
                    {
                        "id": "i-isvkUW76",
                        "instanceName": "instance-xcy9049y "
                    }
                ],
                "monitorType": "scope",
                "namespace": [
                    {
                        "bcmService": "BCE_BCC",
                        "instanceName": "instance-xcy9049y ",
                        "name": "i-isvkUW76___bj.BCE_BCC.a0d04d7c202140cb80155ff7b6752ce4",
                        "namespaceType": "app",
                        "region": "bj",
                        "subService": [
                            {
                                "name": "serviceType",
                                "value": "linux"
                            }
                        ],
                        "transfer": ""
                    }
                ],
                "product": "a0d04d7c202140cb80155ff7b6752ce4",
                "region": "bj",
                "scope": "BCE_BCC",
                "scopeValue": {
                    "name": "BCC",
                    "value": "BCE_BCC"
                },
                "subService": "linux"
            }
        ]
        time = "2023-12-08 09:10:59|2023-12-08 09:11:59"
        response = self.client.get_dashboard_trend_senior_data(data=data, time=time, config=None)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_dashboard_report_muti_data(self):
        data = [
            {
                "region": "bj",
                "subService": "linux",
                "namespace": [
                    {
                        "namespaceType": "app",
                        "transfer": "",
                        "filter": "",
                        "name": "41b372b8-3acc-423c-a6b0-af5c69fd1c41___bj.BCE_BEC.a0d04d7c202140cb80155ff7b6752ce4",
                        "instanceName": "prod.nmp.nn.yd1 ",
                        "region": "bj",
                        "bcmService": "BCE_BEC",
                        "subService": [
                            {
                                "name": "serviceType",
                                "value": "linux"
                            }
                        ]
                    }
                ],
                "product": "a0d04d7c202140cb80155ff7b6752ce4",
                "monitorObject": [
                    {
                        "instanceName": "prod.nmp.nn.yd1",
                        "id": "41b372b8-3acc-423c-a6b0-af5c69fd1c41"
                    }
                ],
                "scope": "BCE_BEC",
                "scopeValue": {
                    "name": "BEC",
                    "value": "BCE_BEC",
                },
                "metric": [
                    {
                        "displayName": "",
                        "name": "vNicInBytes",
                        "alias": "网卡输入流量",
                        "unit": "Bytes",
                        "contrast": [],
                        "timeContrast": [],
                        "statistics": "avg",
                        "cycle": 60,
                        "dimensions": [
                            "eth1",
                            "eth0"
                        ],
                        "metricDimensions": [
                            {
                                "name": "nicName",
                                "values": [
                                    "eth1",
                                    "eth0"
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
        time = "2023-12-08 09:10:59|2023-12-08 10:10:59"
        response = self.client.get_dashboard_report_data(data=data, time=time, config=None)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_dashboard_trend_muti_data(self):
        data = [
            {
                "region": "bj",
                "subService": "linux",
                "namespace": [
                    {
                        "namespaceType": "app",
                        "transfer": "",
                        "filter": "",
                        "name": "41b372b8-3acc-423c-a6b0-af5c69fd1c41___bj.BCE_BEC.a0d04d7c202140cb80155ff7b6752ce4",
                        "instanceName": "prod.nmp.nn.yd1 ",
                        "region": "bj",
                        "bcmService": "BCE_BEC",
                        "subService": [
                            {
                                "name": "serviceType",
                                "value": "linux"
                            }
                        ]
                    }
                ],
                "product": "a0d04d7c202140cb80155ff7b6752ce4",
                "monitorObject": [
                    {
                        "instanceName": "prod.nmp.nn.yd1",
                        "id": "41b372b8-3acc-423c-a6b0-af5c69fd1c41"
                    }
                ],
                "scope": "BCE_BEC",
                "scopeValue": {
                    "name": "BEC",
                    "value": "BCE_BEC",
                },
                "metric": [
                    {
                        "displayName": "",
                        "name": "vNicInBytes",
                        "alias": "网卡输入流量",
                        "unit": "Bytes",
                        "contrast": [],
                        "timeContrast": [],
                        "statistics": "avg",
                        "cycle": 60,
                        "dimensions": [
                            "eth1",
                            "eth0"
                        ],
                        "metricDimensions": [
                            {
                                "name": "nicName",
                                "values": [
                                    "eth1",
                                    "eth0"
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
        time = "2023-12-08 09:10:59|2023-12-08 10:10:59"
        response = self.client.get_dashboard_trend_data(data=data, time=time, config=None)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_dashboard_gauge_chart_muti_data(self):
        data = [
            {
                "region": "bj",
                "subService": "linux",
                "namespace": [
                    {
                        "namespaceType": "app",
                        "transfer": "",
                        "filter": "",
                        "name": "41b372b8-3acc-423c-a6b0-af5c69fd1c41___bj.BCE_BEC.a0d04d7c202140cb80155ff7b6752ce4",
                        "instanceName": "prod.nmp.nn.yd1 ",
                        "region": "bj",
                        "bcmService": "BCE_BEC",
                        "subService": [
                            {
                                "name": "serviceType",
                                "value": "linux"
                            }
                        ]
                    }
                ],
                "product": "a0d04d7c202140cb80155ff7b6752ce4",
                "monitorObject": [
                    {
                        "instanceName": "prod.nmp.nn.yd1",
                        "id": "41b372b8-3acc-423c-a6b0-af5c69fd1c41"
                    }
                ],
                "scope": "BCE_BEC",
                "scopeValue": {
                    "name": "BEC",
                    "value": "BCE_BEC",
                },
                "metric": [
                    {
                        "displayName": "",
                        "name": "vNicInBytes",
                        "alias": "网卡输入流量",
                        "unit": "Bytes",
                        "contrast": [],
                        "timeContrast": [],
                        "statistics": "avg",
                        "cycle": 60,
                        "dimensions": [
                            "eth1",
                            "eth0"
                        ],
                        "metricDimensions": [
                            {
                                "name": "nicName",
                                "values": [
                                    "eth1",
                                    "eth0"
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
        time = "2023-12-08 09:10:59|2023-12-08 10:10:59"
        response = self.client.get_dashboard_gauge_chart_data(data=data, time=time, config=None)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_dashboard_billboard_muti_data(self):
        data = [
            {
                "region": "bj",
                "subService": "linux",
                "namespace": [
                    {
                        "namespaceType": "app",
                        "transfer": "",
                        "filter": "",
                        "name": "41b372b8-3acc-423c-a6b0-af5c69fd1c41___bj.BCE_BEC.a0d04d7c202140cb80155ff7b6752ce4",
                        "instanceName": "prod.nmp.nn.yd1 ",
                        "region": "bj",
                        "bcmService": "BCE_BEC",
                        "subService": [
                            {
                                "name": "serviceType",
                                "value": "linux"
                            }
                        ]
                    }
                ],
                "product": "a0d04d7c202140cb80155ff7b6752ce4",
                "monitorObject": [
                    {
                        "instanceName": "prod.nmp.nn.yd1",
                        "id": "41b372b8-3acc-423c-a6b0-af5c69fd1c41"
                    }
                ],
                "scope": "BCE_BEC",
                "scopeValue": {
                    "name": "BEC",
                    "value": "BCE_BEC",
                },
                "metric": [
                    {
                        "displayName": "",
                        "name": "vNicInBytes",
                        "alias": "网卡输入流量",
                        "unit": "Bytes",
                        "contrast": [],
                        "timeContrast": [],
                        "statistics": "avg",
                        "cycle": 60,
                        "dimensions": [
                            "eth1",
                            "eth0"
                        ],
                        "metricDimensions": [
                            {
                                "name": "nicName",
                                "values": [
                                    "eth1",
                                    "eth0"
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
        time = "2023-12-08 09:10:59|2023-12-08 10:10:59"
        response = self.client.get_dashboard_billboard_data(data=data, time=time, config=None)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_dashboard_dimensions(self):
        dimensions = "nicName"
        metric_name = "vNicInBytes"
        region = "bj"
        service = "BCE_BEC"
        show_id = "7744b3f3-ec04-459a-b3ae-4379111534ff"
        response = self.client.get_dashboard_dimensions(user_id=user_id, metric_name=metric_name, region=region,
                                                        service=service, show_id=show_id, dimensions=dimensions,
                                                        config=None)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_cloud_event_data(self):
        """
        test get cloud event data
        """
        response = self.client.get_cloud_event_data(account_id="a0d04d7c202140cb80155ff7b6752ce4",
                                                    start_time="2023-10-01T00:00:00Z", end_time="2023-11-01T01:00:00Z",
                                                    page_no=1, page_size=10)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_platform_event_data(self):
        """
        test get platform event data
        """
        response = self.client.get_platform_event_data(account_id="a0d04d7c202140cb80155ff7b6752ce4",
                                                       start_time="2023-10-01T00:00:00Z",
                                                       end_time="2023-11-01T01:00:00Z",
                                                       page_no=1, page_size=10)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_event_policy(self):
        """
        test create event policy
        """
        account_id = user_id
        service_name = "BCE_BCC"
        name = "py_sdk_test"
        block_status = "NORMAL"
        event_filter = bcm_model.EventFilter(event_level="*", event_type_list=["*"], eventAliasNames=[])
        resource = bcm_model.EventResourceFilter(region="bj", type="Instance", monitor_object_type="ALL", resources=[])
        incident_actions = ["2fc6e953-331a-4404-8ce7-1c05975dbd9c"]
        response = self.client.create_event_policy(account_id=account_id, service_name=service_name, name=name,
                                                   block_status=block_status, event_filter=event_filter,
                                                   resource=resource, incident_actions=incident_actions)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_instance_group(self):
        """
        test create instance group
        """
        response = self.client.create_instance_group(user_id=user_id, region="bj", service_name="BCE_BCC",
                                                     type_name="Instance", name="py-sdk-test",
                                                     resource_id_list=[])
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_instance_group(self):
        """
        test update instance group
        """
        response = self.client.update_instance_group(user_id=user_id, ig_id="7923", region="bj", service_name="BCE_BCC",
                                                     type_name="Instance", name="py-sdk-test-update")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_delete_instance_group(self):
        """
        test delete instance group
        """
        response = self.client.delete_instance_group(user_id=user_id, ig_id="7923")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_instance_group(self):
        """
        test get instance group
        """
        response = self.client.get_instance_group(user_id=user_id, ig_id="7923")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_list_instance_group(self):
        """
        test list instance group
        """
        response = self.client.list_instance_group(user_id=user_id, name="", region="bj", service_name="BCE_BCC",
                                                   type_name="Instance", page_no=1, page_size=10)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_add_ig_instance(self):
        """
        test add instance to instance group
        """
        resource_id_list = bcm_model.MonitorResource(user_id=user_id, region="bj", service_name="BCE_BCC",
                                                     type_name="Instance", identifiers=[],
                                                     resource_id="InstanceId:dd0109a3-a7fe-4ffb-b2ae-3c6aa0b63705")
        response = self.client.add_ig_instance(ig_id="7923", user_id=user_id, resource_id_list=[resource_id_list])
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_remove_ig_instance(self):
        """
        test remove instance from instance group
        """
        resource_id_list = bcm_model.MonitorResource(user_id=user_id, region="bj", service_name="BCE_BCC",
                                                     type_name="Instance", identifiers=[],
                                                     resource_id="InstanceId:dd0109a3-a7fe-4ffb-b2ae-3c6aa0b63705")
        response = self.client.remove_ig_instance(ig_id="7923", user_id=user_id, resource_id_list=[resource_id_list])
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_list_ig_instance(self):
        """
        test list instance from instance group
        """
        response = self.client.list_ig_instance(ig_id="7923", user_id=user_id, service_name="BCE_BCC",
                                                type_name="Instance", region="bj", view_type="DETAIL_VIEW",
                                                page_no=1, page_size=10)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_list_all_instance(self):
        """
        test list all instance
        """
        response = self.client.list_all_instance(user_id=user_id, service_name="BCE_BCC",
                                                 type_name="Instance", region="bj", view_type="LIST_VIEW",
                                                 keyword_type="name", keyword="", page_no=1, page_size=10)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_list_filter_instance(self):
        """
        test list filter instance
        """
        response = self.client.list_filter_instance(user_id=user_id, service_name="BCE_BCC",
                                                    type_name="Instance", region="bj", view_type="LIST_VIEW",
                                                    keyword_type="name", keyword="", page_no=1, page_size=10,
                                                    ig_id="7923", ig_uuid="bc59b391-2973-41f5-b13f-596c0b268682")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_push_metric_data(self):
        """
        test push metric data
        """

        metric_data = [bcm_model.MetricDatum("cpu_test", [], 1.2, "1702555303")]
        response = self.client.push_metric_data(user_id=user_id,
                                                scope="scope_test",
                                                metric_data = metric_data)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_custom_metric_data(self):
        """
        test get custom metric data
        """
        namespaces = "scope_test"
        metric_name = "cpu_test"
        dimensions = []
        statistics = "average"
        cycle = 60

        response = self.client.get_custom_metric_data(user_id=user_id, namespaces=namespaces, metric_name=metric_name,
                                                      dimensions=dimensions, statistics=statistics, start_time="2023-12-05T09:54:15Z",
                                                      end_time="2023-12-05T10:04:15Z", cycle=cycle)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_push_cusomt_metric_data(self):
        """
        test push custom metric data
        """
        response = self.client.push_custom_metric_data(user_id=user_id,
                                                       namespace="test_pyy", metric_name="pv",
                                                       dimensions=[], value=123, timestamp="2023-12-17T08:00:00Z")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_site_http_task_config(self):
        """
        test create site http task config
        """
        response = self.client.create_site_http_task_config(user_id=user_id,
                                                            task_name="task_name", address="www.baidu.com",
                                                            method="get", post_content="", advance_config=False,
                                                            cycle=60, idc="beijing-CMNET", timeout = 20)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_site_http_task_config(self):
        """
        test update site http task config
        """
        response = self.client.update_site_http_task_config(user_id=user_id,
                                                            task_id="rriHgFGaIaVIqYanAveRMervXWWfQufq",
                                                            task_name="task_name", address="www.baidu.com",
                                                            method="get", post_content="", advance_config=False,
                                                            cycle=60, idc="henan-CMNET", timeout = 20)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_site_http_task_config(self):
        """
        test get site http task config
        """
        response = self.client.get_site_http_task_config(user_id=user_id,
                                                         task_id="rriHgFGaIaVIqYanAveRMervXWWfQufq")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_site_https_task_config(self):
        """
        test create site https task config
        """
        response = self.client.create_site_https_task_config(user_id=user_id,
                                                             task_name="task_name", address="www.baidu.com",
                                                             method="get", post_content="", advance_config=False,
                                                             cycle=60, idc="beijing-CMNET", timeout = 20)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_site_https_task_config(self):
        """
        test update site https task config
        """
        response = self.client.update_site_https_task_config(user_id=user_id,
                                                             task_id="rriHgFGaIaVIqYanAveRMervXWWfQufq",
                                                             task_name="task_name", address="www.baidu.com",
                                                             method="get", post_content="", advance_config=False,
                                                             cycle=60, idc="henan-CMNET", timeout = 20)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_site_https_task_config(self):
        """
        test get site https task config
        """
        response = self.client.get_site_https_task_config(user_id=user_id,
                                                          task_id="rriHgFGaIaVIqYanAveRMervXWWfQufq")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_site_ping_task_config(self):
        """
        test create site ping task config
        """
        response = self.client.create_site_ping_task_config(user_id=user_id,
                                                            task_name="task_name", address="www.baidu.com",
                                                            packet_count=1, packet_loss_rate=1,
                                                            cycle=60, idc="beijing-CMNET", timeout = 20)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_site_ping_task_config(self):
        """
        test update site ping task config
        """
        response = self.client.update_site_ping_task_config(user_id=user_id,
                                                            task_id="VoFXOMtXwLJSWgxIUjavNPgHcdznwivS",
                                                            task_name="task_name", address="www.baidu.com",
                                                            packet_count=1, packet_loss_rate=1,
                                                            cycle=60, idc="henan-CMNET", timeout = 20)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_site_ping_task_config(self):
        """
        test get site ping task config
        """
        response = self.client.get_site_ping_task_config(user_id=user_id,
                                                         task_id="VoFXOMtXwLJSWgxIUjavNPgHcdznwivS")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_site_tcp_task_config(self):
        """
        test create site tcp task config
        """
        response = self.client.create_site_tcp_task_config(user_id=user_id,
                                                           task_name="task_name", address="www.baidu.com",
                                                           port=80, advance_config=False,
                                                           cycle=60, idc="beijing-CMNET", timeout = 2,
                                                           input_type=0, output_type=0, input="", expected_output="")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_site_tcp_task_config(self):
        """
        test update site tcp task config
        """
        response = self.client.update_site_tcp_task_config(user_id=user_id,
                                                           task_id="JAbvZxtXWxreAkiHgFnPtEQqBWcZzkjU",
                                                           task_name="task_name", address="www.baidu.com",
                                                           port=80, advance_config=False,
                                                           cycle=60, idc="beijing-CMNET", timeout = 3,
                                                           input_type=0, output_type=0, input="", expected_output="")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_site_tcp_task_config(self):
        """
        test get site tcp task config
        """
        response = self.client.get_site_tcp_task_config(user_id=user_id,
                                                        task_id="JAbvZxtXWxreAkiHgFnPtEQqBWcZzkjU")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_site_udp_task_config(self):
        """
        test create site udp task config
        """
        response = self.client.create_site_udp_task_config(user_id=user_id,
                                                           task_name="task_name", address="www.baidu.com",
                                                           port=80, advance_config=False,
                                                           cycle=60, idc="beijing-CMNET", timeout = 2,
                                                           input_type=0, output_type=0, input="", expected_output="")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_site_udp_task_config(self):
        """
        test update site udp task config
        """
        response = self.client.update_site_udp_task_config(user_id=user_id,
                                                           task_id="JAbvZxtXWxreAkiHgFnPtEQqBWcZzkjU",
                                                           task_name="task_name", address="www.baidu.com",
                                                           port=80, advance_config=False,
                                                           cycle=60, idc="beijing-CMNET", timeout = 3,
                                                           input_type=0, output_type=0, input="", expected_output="")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_site_udp_task_config(self):
        """
        test get site udp task config
        """
        response = self.client.get_site_udp_task_config(user_id=user_id,
                                                        task_id="JAbvZxtXWxreAkiHgFnPtEQqBWcZzkjU")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_site_ftp_task_config(self):
        """
        test create site ftp task config
        """
        response = self.client.create_site_ftp_task_config(user_id=user_id,
                                                           task_name="task_name", address="www.baidu.com",
                                                           port=80, anonymous_login=False,
                                                           cycle=60, idc="beijing-CMNET", timeout = 3,
                                                           user_name="", password="")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_site_ftp_task_config(self):
        """
        test update site ftp task config
        """
        response = self.client.update_site_ftp_task_config(user_id=user_id,
                                                           task_id="JAbvZxtXWxreAkiHgFnPtEQqBWcZzkjU",
                                                           task_name="task_name", address="www.baidu.com",
                                                           port=80, anonymous_login=False,
                                                           cycle=60, idc="beijing-CMNET", timeout = 3,
                                                           user_name="", password="")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_site_ftp_task_config(self):
        """
        test get site ftp task config
        """
        response = self.client.get_site_ftp_task_config(user_id=user_id,
                                                        task_id="JAbvZxtXWxreAkiHgFnPtEQqBWcZzkjU")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_site_dns_task_config(self):
        """
        test create site dns task config
        """
        response = self.client.create_site_dns_task_config(user_id=user_id,
                                                           task_name="task_name", address="www.baidu.com",
                                                           cycle=60, idc="beijing-CMNET", timeout = 3,
                                                           resolve_type="RECURSION", kidnap_white="")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_site_dns_task_config(self):
        """
        test update site dns task config
        """
        response = self.client.update_site_dns_task_config(user_id=user_id,
                                                           task_id="SisKPHhkfWQvkRUeUGZYGuLLSDymnTsA",
                                                           task_name="task_name", address="www.baidu.com",
                                                           cycle=60, idc="beijing-CMNET", timeout = 3,
                                                           resolve_type="RECURSION", kidnap_white="")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_site_dns_task_config(self):
        """
        test get site dns task config
        """
        response = self.client.get_site_dns_task_config(user_id=user_id,
                                                        task_id="SisKPHhkfWQvkRUeUGZYGuLLSDymnTsA")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_site_task_config_list(self):
        """
        test get site task config list
        """
        response = self.client.get_site_task_config_list(user_id=user_id,
                                                         query=None, type="http", page_no=1, page_size=10)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_delete_site_task_config(self):
        """
        test delete site task config
        """
        response = self.client.delete_site_task_config(user_id=user_id,
                                                       task_id="rriHgFGaIaVIqYanAveRMervXWWfQufq")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_site_task_config_info(self):
        """
        test get site task config info
        """
        response = self.client.get_site_task_config_info(user_id=user_id,
                                                         task_id="SisKPHhkfWQvkRUeUGZYGuLLSDymnTsA")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_site_alarm_config(self):
        """
        test create site alarm config
        """
        rule = bcm_model.SiteAlarmRule("connectTime",
                                       None,
                                       60, "average", 10, ">", 1,
                                       "THRESHOLD", ["average"], [], None)
        response = self.client.create_site_alarm_config(user_id=user_id,
                                                        task_id="SisKPHhkfWQvkRUeUGZYGuLLSDymnTsA",
                                                        comment="", alias_name="pyy_test",
                                                        level="MAJOR", action_enabled=True,
                                                        resume_actions=["37eddd21-a44c-42c6-b0bb-a3e9d738a091"],
                                                        insufficient_actions=["37eddd21-a44c-42c6-b0bb-a3e9d738a091"],
                                                        incident_action=["37eddd21-a44c-42c6-b0bb-a3e9d738a091"],
                                                        insufficient_cycle=0, rules=[rule], region="bj",
                                                        callback_url="", method=None, site_monitor=None, tag="")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_update_site_alarm_config(self):
        """
        test update site alarm config
        """
        rule = bcm_model.SiteAlarmRule("connectTime",
                                       None,
                                       60, "average", 10, ">", 1,
                                       "THRESHOLD", ["average"], [], None)
        response = self.client.update_site_alarm_config(user_id=user_id,
                                                        task_id="SisKPHhkfWQvkRUeUGZYGuLLSDymnTsA",
                                                        alarm_name="b87ffe8c1c584b09b2baf15e6244d55d",
                                                        comment="", alias_name="pyy_test",
                                                        level="MAJOR", action_enabled=True,
                                                        resume_actions=["37eddd21-a44c-42c6-b0bb-a3e9d738a091"],
                                                        insufficient_actions=["37eddd21-a44c-42c6-b0bb-a3e9d738a091"],
                                                        incident_action=["37eddd21-a44c-42c6-b0bb-a3e9d738a091"],
                                                        insufficient_cycle=60, rules=[rule], region="bj",
                                                        callback_url="", method=None, site_monitor=None, tag="")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_delete_site_alarm_config(self):
        """
        test delete site alarm config
        """
        response = self.client.delete_site_alarm_config(user_id=user_id,
                                                        alarm_names=["b87ffe8c1c584b09b2baf15e6244d55d"])
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_site_alarm_config_detail(self):
        """
        test get site alarm config detail
        """
        response = self.client.get_site_alarm_config_detail(user_id=user_id,
                                                            alarm_name="b87ffe8c1c584b09b2baf15e6244d55d")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_site_alarm_config_list(self):
        """
        test get site alarm config detail
        """
        response = self.client.get_site_alarm_config_list(user_id=user_id,
                                                          alarm_name="b87ffe8c1c584b09b2baf15e6244d55d",
                                                          task_id=None, action_enabled=True,
                                                          page_no=1, page_size=10)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_block_site_alarm_config(self):
        """
        test get site alarm config detail
        """
        response = self.client.block_site_alarm_config(user_id=user_id,
                                                       alarm_name="b87ffe8c1c584b09b2baf15e6244d55d",
                                                       namespace=None)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_unblock_site_alarm_config(self):
        """
        test get site alarm config detail
        """
        response = self.client.unblock_site_alarm_config(user_id=user_id,
                                                         alarm_name="b87ffe8c1c584b09b2baf15e6244d55d",
                                                         namespace=None)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_site_metric_data(self):
        """
        test get site metric data
        """
        response = self.client.get_site_metric_data(user_id=user_id,
                                                    task_id="VoFXOMtXwLJSWgxIUjavNPgHcdznwivS",
                                                    metric_name="success", statistics=["average", "sum"],
                                                    start_time="2023-12-19T06:09:12Z",
                                                    end_time="2023-12-19T06:19:12Z",
                                                    cycle=60, dimensions=None)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_site_overall_view(self):
        """
        test get site overall view
        """
        response = self.client.get_site_overall_view(user_id=user_id,
                                                     task_id="VoFXOMtXwLJSWgxIUjavNPgHcdznwivS")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_site_provincial_view(self):
        """
        test get site provincial view
        """
        response = self.client.get_site_provincial_view(user_id=user_id,
                                                        task_id="VoFXOMtXwLJSWgxIUjavNPgHcdznwivS",
                                                        isp="beijing")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_site_agent(self):
        """
        test get site agent
        """
        response = self.client.get_site_once_agent(user_id=user_id)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_get_site_agent_for_task(self):
        """
        test get site agent for task
        """
        response = self.client.get_site_agent_for_task(user_id=user_id,
                                                       task_id="VoFXOMtXwLJSWgxIUjavNPgHcdznwivS")
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_create_alarm_policy(self):
        """
        test create alarm policy
        """
        monitor_object = bcm_model.MonitorObject("INSTANCE", [dimensions])
        rule = bcm_model.AlarmRule(1, "CPUUsagePercent", 60, "average", "12345", ">", 1)
        self.client.create_alarm_config(user_id, "test_policy_0123", "BCE_BCC", "CRITICAL", "bj",
                                        monitor_object, ["d242711b-****-****-****-b8ac175f8e7d"], [[rule]])

    def test_update_alarm_policy(self):
        """
        test update alarm policy
        """
        monitor_object = bcm_model.MonitorObject("INSTANCE", ["InstanceId:i-WvElewBV"])
        rule = bcm_model.AlarmRule(1, "CPUUsagePercent", 60, "average", "12345", ">", 1)
        self.client.update_alarm_config(user_id, "5c09e9********************d62091",
                                        "test_policy_01234", "BCE_BCC", "CRITICAL", "bj",
                                        monitor_object, ["d242711b-****-****-****-b8ac175f8e7d"], [[rule]])

    def test_delete_alarm_policy(self):
        """
        test delete alarm policy
        """
        self.client.delete_alarm_config(user_id, "5c09e9********************d62091", "BCE_BCC")

    def test_block_alarm_policy(self):
        """
        test block alarm policy
        """
        self.client.block_alarm_config(user_id, "5c09e9********************d62091", "BCE_BCC")

    def test_unblock_alarm_policy(self):
        """
        test unblock alarm policy
        """
        self.client.unblock_alarm_config(user_id, "5c09e9********************d62091", "BCE_BCC")

    def test_get_alarm_policy_detail(self):
        """
        test get alarm policy detail
        """
        resp = self.client.get_alarm_config_detail(user_id, "5c09e9********************d62091", "BCE_BCC")
        print(resp)

    def test_get_single_instance_alarm_configs(self):
        """
        test get single instance alarm configs
        """
        resp = self.client.get_single_instance_alarm_configs(user_id, "BCE_BCC", 1, 10)
        print(resp)

    def test_get_alarm_metrics(self):
        """
        test get alarm metrics
        """
        resp = self.client.get_alarm_metrics(user_id, "BCE_BCC")
        print(resp)

    def test_create_alarm_policy_v2(self):
        """
        test create alarm policy v2
        """
        action = bcm_model.AlarmAction("test_yangmoda")
        rule = bcm_model.AlarmConfigRule("CPUUsagePercent", ">", "average", 12345.0)
        policy = bcm_model.AlarmConfigPolicy([rule], 1)
        identifier = bcm_model.KV("InstanceId", "i-WvElew**")
        instance = bcm_model.TargetInstance("bj", [identifier])
        self.client.create_alarm_config_v2(user_id, "test_policy_01234", "BCE_BCC", "TARGET_TYPE_MULTI_INSTANCES",
                                           "CRITICAL", "bj", [action], [policy], target_instances=[instance])

    def test_update_alarm_policy_v2(self):
        """
        test update alarm policy v2
        """
        action = bcm_model.AlarmAction("test_yangmoda")
        rule = bcm_model.AlarmConfigRule("CPUUsagePercent", ">", "average", 12345.0)
        policy = bcm_model.AlarmConfigPolicy([rule], 1)
        identifier = bcm_model.KV("InstanceId", "i-WvElewBV")
        instance = bcm_model.TargetInstance("bj", [identifier])
        self.client.update_alarm_config_v2(user_id, "5c09e9********************d62091", "test_policy_012345",
                                           "BCE_BCC", "TARGET_TYPE_MULTI_INSTANCES",
                                           "CRITICAL", "bj", [action], [policy], target_instances=[instance])

    def test_block_alarm_policy_v2(self):
        """
        test block alarm policy v2
        """
        self.client.block_alarm_config_v2(user_id, "5c09e9********************d62091", "BCE_BCC")

    def test_unblock_alarm_policy_v2(self):
        """
        test unblock alarm policy v2
        """
        self.client.unblock_alarm_config_v2(user_id, "5c09e9********************d62091", "BCE_BCC")

    def test_get_alarm_policy_detail_v2(self):
        """
        test get alarm policy detail v2
        """
        resp = self.client.get_alarm_config_detail_v2(user_id, "5c09e9********************d62091", "BCE_BCC")
        print(resp)

    def test_create_custom_alarm_policy(self):
        """
        create alarm policy for customNamespace
        """
        rule = bcm_model.CustomAlarmRule(custom_metric_name, 60, "average", 10, ">", 1, 1, [])

        response = self.client.create_custom_alarm_policy(user_id, "test_policy_zz", custom_namespace, "MAJOR",
                                                         rules=[rule])
    def test_delete_custom_alarm_policy(self):
        """
        delete alarm policy for customNamespace
        """
        custom_alarm_list = [
            {
                "scope": "test_qsh",
                "userId": "a0d04d7c202140cb80155ff7********",
                "alarmName": [
                    "test_policy_zz"
                ]
            }
        ]
        response = self.client.delete_custom_alarm_policy(custom_alarm_list)

    def test_update_custom_alarm_policy(self):
        """
         update alarm policy for customNamespace
        """
        rule = bcm_model.CustomAlarmRule(custom_metric_name, 60, "average", 10, ">", 1, 1, [])

        response = self.client.update_custom_alarm_policy(user_id, "test_policy_13", custom_namespace, "MAJOR",
                                                         rules=[rule])
        print(response)
    def test_list_custom_policy(self):
        """
        list alarm policies for customNamespace
        """
        res = self.client.list_custom_policy("a0d04d7c202140cb80155ff7********", 1, 10)
        print(res)

    def test_detail_custom_policy(self):
        """
        detail alarm policy for customNamespace
        """
        res = self.client.detail_custom_policy("a0d04d7c202140cb80155ff7********", "test_qsh", "test_policy_zz")
        print(res)
    def test_block_custom_policy(self):
        """
        block alarm policy for customNamespace
        """
        res = self.client.block_custom_policy("a0d04d7c202140cb80155ff7********", "test_qsh", "test_policy_zz")
        print(res)
    def test_unblock_custom_policy(self):
        """
        unblock alarm policy for customNamespace
        """
        res = self.client.unblock_custom_policy("a0d04d7c202140cb80155ff7********", "test_qsh", "test_policy_zz")
        print(res)

    def test_create_site_once_task(self):
        """
        create site once task
        """
        onceConfig = SiteOnceConfig(method="get")
        res = self.client.create_site_once_task("HTP", "a0d04d7c202140cb80155ff7********", "www.baidu.com",
                                               "beijing-CMNET", 60, "HTTP", once_config=onceConfig)
        print(res)
    def test_list_site_once_records(self):
        """
        list site once records
        """
        res = self.client.list_site_once_records()
        print(res)
    def test_delete_site_once_record(self):
        """
        delete site once record
        """
        res = self.client.delete_site_once_record("a0d04d7c202140cb80155ff7********", "OMVQcQTDPmSeLIXAsJEKAAbZwynfOINu")
        print(res)
    def test_detail_site_once_result(self):
        """
        detail site once result
        """
        res = self.client.detail_site_once_result("a0d04d7c202140cb80155ff7********", "OMVQcQTDPmSeLIXAsJEKAAbZwynfOINu",
                                                 filter_area="beijing")
        print(res)
    def test_detail_site_once(self):
        """
        detail site once
        """
        res = self.client.detail_site_once("a0d04d7c202140cb80155ff7********")
        print(res)
    def test_again_exec_site_once(self):
        """
        again exec site once
        """
        res = self.client.again_exec_site_once("a0d04d7c202140cb80155ff7********", "OMVQcQTDPmSeLIXAsJEKAAbZwynfOINu")
        print(res)

    def test_list_site_once_history(self):
        """
        list site once history
        """
        res = self.client.list_site_once_history(user_id="a0d04d7c202140cb80155ff7********")
        print(res)
    def test_get_site_once_agent(self):
        """
        get site agent
        """
        res = self.client.get_site_once_agent(user_id="a0d04d7c202140cb80155ff7********")
        print(res)

    def test_get_multi_dimension_latest_metrics(self):
        """
        get multi dimension latest metrics
        """
        res = self.client.get_multi_dimension_latest_metrics(user_id="a0d04d7c202140cb80155ff7********",
                                                             scope="BCE_BLB",
                                                             metric_names=["ActiveConnCount", "DropOutBytes"],
                                                             statistics=[
                                                                 "average",
                                                                 "sum",
                                                                 "minimum"
                                                             ],
                                                             dimensions=[{"name": "BlbId", "value": "lb-****ed23"}],
                                                             timestamp="2024-03-18T06:01:00Z")
        print(res)

    def test_get_all_data_metrics_v2(self):
        """
        get all data metrics v2
        """

        res = self.client.get_all_data_metrics_v2(user_id="a0d04d7c202140cb80155ff7********",
                                                  scope="BCE_BCC", region="bj", type=None,
                                                  dimensions=[[{"name": "InstanceId", "value": "i-DMx***xX"}],
                                                              [{"name": "InstanceId", "value": "i-Y8N***md"}]],
                                                  metric_names=["CPUUsagePercent", "MemUsedPercent"],
                                                  statistics=[
                                                      "average",
                                                      "sum"
                                                  ],
                                                  cycle=60,
                                                  start_time="2024-03-20T07:01:00Z",
                                                  end_time="2024-03-20T07:05:00Z")
        print(res)

    def test_batch_get_all_data_metrics_v2(self):
        """
        batch get all data metrics v2
        """
        res = self.client.batch_get_all_data_metrics_v2(user_id="a0d04d7c2021******155ff7b6752ce4",
                                                        scope="BCE_MQ_KAFKA", region="bj", type="Node",
                                                        dimensions=[[
                                                            {"name": "ClusterId", "value": "efe456d667c649******652c93812a79"},
                                                            {"name": "NodeId", "value": "i-Um1V8Haq"}
                                                        ]],
                                                        metric_names=["CpuUsedPercent", "CpuIdlePercent"],
                                                        statistics=[
                                                            "average",
                                                            "sum"
                                                        ],
                                                        cycle=60,
                                                        start_time="2024-03-21T06:33:50Z",
                                                        end_time="2024-03-21T07:33:50Z")
        print(res)

    def test_get_metric_dimension_top(self):
        """
        get metric dimension top
        """
        res = self.client.get_metric_dimension_top(user_id="453bf9********************9090dc",
                                                   scope="BCE_PFS", region="bj",
                                                   dimensions= {"InstanceId": "pfs-1*****7"},
                                                   metric_name="WriteIO",
                                                   statistics="average",
                                                   labels=[
                                                       "FilesetId"
                                                   ],
                                                   start_time="2024-03-21T06:33:50Z",
                                                   end_time="2024-03-21T07:33:50Z")
        print(res)

if __name__ == '__main__':
    suite = unittest.TestSuite()

    # suite.addTest(TestBcmClient("test_get_metric_dimension_top"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
