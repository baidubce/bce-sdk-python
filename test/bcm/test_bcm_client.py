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
app_name = "app_name"
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

if __name__ == '__main__':
    suite = unittest.TestSuite()

    # suite.addTest(TestBcmClient("test_get_metric_data"))

    runner = unittest.TextTestRunner()
    runner.run(suite)
