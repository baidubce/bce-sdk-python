# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
"""
Samples for bcm client.
"""

# !/usr/bin/env python
# coding=utf-8
from baidubce.exception import BceHttpClientError, BceServerError
from baidubce.services.bcm.bcm_model import SiteOnceConfig
from baidubce.services.bcm.bcm_client import BcmClient, bcm_model
import bcm_sample_conf

if __name__ == '__main__':

    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    user_id = "fakeuser1ba678asdf8as7df6a5sdf67"
    scope = "BCE_BCC"
    metric_name = "vCPUUsagePercent"
    metric_name_batch = "CPUUsagePercent,MemUsagePercent"
    dimensions = "InstanceId:i-xxx"
    dimensions_batch = "InstanceId:i-1xx,InstanceId:i-2xx"
    statistics = "average,maximum,minimum"
    start_time = "2020-01-20T00:00:01Z"
    end_time = "2020-01-20T00:10:01Z"
    period_in_second = 60
    custom_namespace = "test_qsh"
    custom_metric_name = "taasd"


    # create a bcm client
    bcm_client = BcmClient(bcm_sample_conf.config)

    # query metric data from bcm interface
    try:
        response = bcm_client.get_metric_data(user_id=user_id,
                                              scope=scope,
                                              metric_name=metric_name,
                                              dimensions=dimensions,
                                              statistics=statistics,
                                              start_time=start_time,
                                              end_time=end_time,
                                              period_in_second=period_in_second)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # query batch metric data from bcm interface
    try:
        response = bcm_client.get_batch_metric_data(user_id=user_id,
                                                    scope=scope,
                                                    metric_name=metric_name_batch,
                                                    dimensions=dimensions_batch,
                                                    statistics=statistics,
                                                    start_time=start_time,
                                                    end_time=end_time,
                                                    period_in_second=period_in_second)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete a custom namespace from bcm interface
    try:
        names = ["Test01"]
        response = bcm_client.batch_delete_namespaces(user_id=user_id, names=names)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create a custom namespace for custom monitor from bcm interface
    try:
        name = "Test01"
        namespace_alias = "test"
        comment = "test"
        response = bcm_client.create_namespace(user_id=user_id, name=name,
                                               namespace_alias=namespace_alias, comment=comment)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update a custom namespace from bcm interface
    try:
        name = "Test01"
        namespace_alias = "test01"
        comment = "test01"
        response = bcm_client.update_namespace(user_id=user_id, name=name,
                                               namespace_alias=namespace_alias, comment=comment)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list custom namespaces from bcm interface
    try:
        response = bcm_client.list_namespaces(user_id=user_id)
        print(response)

        name = "test"
        page_no = 1
        page_size = 10
        response = bcm_client.list_namespaces(user_id=user_id, name=name, page_no=page_no, page_size=page_size)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create custom metric from bcm interface
    try:
        namespace = "Test01"
        metric_name_without_dimension = "TestMetric01"
        metric_alias = "test"
        unit = "sec"
        cycle = 60
        response = bcm_client.create_namespace_metric(user_id=user_id, namespace=namespace,
                                                      metric_name=metric_name_without_dimension,
                                                      metric_alias=metric_alias, unit=unit, cycle=cycle)
        print(response)

        metric_name_dimension = "TestMetric02"
        metric_dimensions = [bcm_model.CustomDimensionModel("test", 1, alias="test")]
        response = bcm_client.create_namespace_metric(user_id=user_id, namespace=namespace,
                                                      metric_name=metric_name_dimension, metric_alias=metric_alias,
                                                      unit=unit, cycle=cycle, dimensions=metric_dimensions)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update custom metric from bcm interface
    try:
        namespace = "Test01"
        metric_name_without_dimension = "TestMetric01"
        metric_alias = "test01"
        unit = "sec"
        cycle = 60
        response = bcm_client.update_namespace_metric(user_id=user_id, namespace=namespace,
                                                      metric_name=metric_name_without_dimension,
                                                      metric_alias=metric_alias, unit=unit, cycle=cycle)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list custom metrics from bcm interface
    try:
        namespace = "Test01"
        response = bcm_client.list_namespace_metrics(user_id=user_id, namespace=namespace)
        print(response)

        namespace = "Test01"
        metric_name = "test"
        metric_alias = "test"
        page_no = 1
        page_size = 10
        response = bcm_client.list_namespace_metrics(user_id=user_id, namespace=namespace, metric_name=metric_name,
                                                     metric_alias=metric_alias, page_no=page_no, page_size=page_size)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get custom metric from bcm interface
    custom_metric_ids = []
    try:
        namespace = "Test01"
        metric_name = "TestMetric01"
        response = bcm_client.get_custom_metric(user_id=user_id, namespace=namespace, metric_name=metric_name)
        print(response)
        if response.id is not None:
            custom_metric_ids.append(response.id)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # batch delete custom metrics from bcm interface
    try:
        namespace = "Test01"
        ids = custom_metric_ids
        response = bcm_client.batch_delete_namespace_metrics(user_id=user_id, namespace=namespace, ids=ids)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create custom event from bcm interface
    try:
        namespace = "Test01"
        event_name = "TestEvent01"
        event_name_alias = "test"
        event_level = bcm_model.EventLevel.NOTICE
        comment = "test"
        response = bcm_client.create_namespace_event(user_id=user_id, namespace=namespace, event_name=event_name,
                                                     event_name_alias=event_name_alias, event_level=event_level,
                                                     comment=comment)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update custom event from bcm interface
    try:
        namespace = "Test01"
        event_name = "TestEvent01"
        event_name_alias = "test01"
        event_level = bcm_model.EventLevel.NOTICE
        comment = "test01"
        response = bcm_client.update_namespace_event(user_id=user_id, namespace=namespace, event_name=event_name,
                                                     event_name_alias=event_name_alias, event_level=event_level,
                                                     comment=comment)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list custom events from bcm interface
    try:
        namespace = "Test01"
        response = bcm_client.list_namespace_events(user_id=user_id, namespace=namespace)
        print(response)

        namespace = "Test01"
        event_name = "test"
        event_level = bcm_model.EventLevel.NOTICE
        page_no = 1
        page_size = 10
        response = bcm_client.list_namespace_events(user_id=user_id, namespace=namespace, name=event_name,
                                                    event_level=event_level, page_no=page_no, page_size=page_size)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get custom event from bcm interface
    try:
        namespace = "Test01"
        event_name = "TestEvent01"
        response = bcm_client.get_custom_event(user_id=user_id, namespace=namespace, event_name=event_name)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # batch delete custom events from bcm interface
    try:
        namespace = "Test01"
        names = ["TestEvent01"]
        response = bcm_client.batch_delete_namespace_events(user_id=user_id, namespace=namespace, names=names)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list notify group
    try:
        response = bcm_client.list_notify_group(page_no=1, page_size=10)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list notify party
    try:
        response = bcm_client.list_notify_party(name="test", page_no=1, page_size=5)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create action
    try:
        notification = bcm_model.Notification("EMAIL")
        member = bcm_model.Member("notifyParty", "56c9e0e2138c4f", "lzs")
        response = bcm_client.create_action(user_id, [notification], [member], "test_wjr_py")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete action
    try:
        response = bcm_client.delete_action(user_id=user_id, name="bb832cf9-ce5e-4c59-85a0-4ddf30******")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list action
    try:
        response = bcm_client.list_action(user_id=user_id, page_no=1, page_size=5, name="test")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update action
    try:
        notification = bcm_model.Notification("EMAIL")
        member = bcm_model.Member("notifyParty", "56c9e0e2138c4f", "lzs")
        response = bcm_client.update_action(user_id=user_id, notifications=[notification], members=[member],
                                            alias="test_wjr_py", disable_times=[], action_callbacks=[],
                                            name="2185c71a-9132-4b4e-92d2-35eebd******")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # log extract
    try:
        extract_rule = ("800] \"(?<method>(GET|POST|PUT|DELETE)) .*/v1/dashboard/metric/(?<widget>(cycle|trend|report|"
                        "billboard|gaugechart)) HTTP/1.1\".* (?<resTime>[0-9]+)ms")
        log_example = (
            "10.157.16.207 - - [09/Apr/2020:20:45:33 +0800] \"POST /v1/dashboard/metric/gaugechart HTTP/1.1\""
            " 200 117 109ms")
        response = bcm_client.log_extract(user_id=user_id, extract_rule=extract_rule, log_example=log_example)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # query metric meta for_application
    try:
        response = bcm_client.query_metric_meta_for_application(user_id=user_id, app_name="test14",
                                                                task_name="79c35af26c4346ab844bcbcdde******",
                                                                metric_name="log.responseTime",
                                                                dimension_keys=["method"])
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # query metric data for_application
    try:
        response = bcm_client.query_metric_data_for_application(user_id=user_id, app_name="zmq-log-1115",
                                                                task_name="6d3f07e6684d47b69ca9600f7f******",
                                                                metric_name="exec.6d3f07e6684d47b69ca9600f******"
                                                                            ".metric1",
                                                                start_time="2023-12-05T09:54:15Z",
                                                                end_time="2023-12-05T10:04:15Z",
                                                                instances=["0.zmq-log-1115"],
                                                                statistics=["average", "maximum"])
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list alarm metrics for application
    try:
        response = bcm_client.list_alarm_metrics_for_application(user_id=user_id, app_name="test_ymd_app_0918",
                                                                 task_name="46e78b2831394f738429f8826******",
                                                                 search_name="test_name")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # test get alarm policy for application
    try:
        response = bcm_client.get_alarm_policy_for_application(user_id=user_id, app_name="test_ymd_app_0918",
                                                               alarm_name="inst-test")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete alarm policy for application
    try:
        response = bcm_client.delete_alarm_policy_for_application(user_id=user_id, app_name="uuu", alarm_name="dasd")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list alarm policy for application
    try:
        response = bcm_client.list_alarm_policy_for_application(user_id=user_id, page_no=1, src_type="PORT")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create alarm policy for application
    try:
        monito_object_view = bcm_model.ApplicationObjectView("zmq-log-1115.453bf9588c9e488f9ba2c98412******")
        monitor_object = bcm_model.ApplicationMonitorObject("APP", [monito_object_view])
        rule = bcm_model.ApplicationAlarmRule("log.ab3b543f41974e26ab984d94fc******.log_metric2", "log_metric2",
                                              60, "average", 10, ">", 1,
                                              0, [])
        response = bcm_client.create_alarm_policy_for_application(
            user_id, "", "test_wjr_py", "zmq-log-1115", "APP",
            monitor_object, "ab3b543f41974e26ab984d94fc******", "LOG", "INSTANCE",
            "MAJOR", [[rule]], incident_actions=["624c99b5-5436-478c-8326-0efc81******"])
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update alarm policy for application
    try:
        monito_object_view = bcm_model.ApplicationObjectView("zmq-log-1115.453bf9588c9e488f9ba2c98412******")
        monitor_object = bcm_model.ApplicationMonitorObject("APP", [monito_object_view])
        rule = bcm_model.ApplicationAlarmRule("log.ab3b543f41974e26ab984d94fc******.log_metric2", "log_metric2",
                                              60, "average", 10, ">", 1,
                                              0, [])
        response = bcm_client.update_alarm_policy_for_application(user_id, "", "test_wjr_py",
                                                                  "zmq-log-1115", "APP",
                                                                  monitor_object, "ab3b543f41974e26ab984d94fc******",
                                                                  "LOG", "INSTANCE", "MAJOR",
                                                                  [[rule]], incident_actions=[
                "624c99b5-5436-478c-8326-0efc8******"])
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create_dashboard
    try:
        title = 'yyy-python3'
        dashboard_type = 'common'
        configure = ("{\"tabs\":[{\"dimensions\":[],\"metric\":[],\"name\":\"\",\"namespace\":[],"
                     "\"widgets\":[[{\"name\":\"_54382_54383\"},{\"name\":\"_54382_54384\"},"
                     "{\"name\":\"_54382_54385\"}],[{\"name\":\"_54382_54386\"}]]}]}")
        response = bcm_client.create_dashboard(user_id=user_id, configure=configure,
                                               title=title, dashboard_type=dashboard_type)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get_dashboard
    try:
        dashboard_name = '_54507'
        response = bcm_client.client.get_dashboard(user_id=user_id, dashboard_name=dashboard_name)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update_dashboard
    try:
        dashboard_name = '_54550'
        title = 'yyy-python-update2'
        dashboard_type = 'common'
        configure = ("{\"tabs\":[{\"dimensions\":[],\"metric\":[],\"name\":\"\",\"namespace\":[],\"widgets\":[[{"
                     "\"name\":\"_54382_54383\"},{\"name\":\"_54382_54384\"},{\"name\":\"_54382_54385\"}],"
                     "[{\"name\":\"_54382_54386\"}]]}]}")
        response = bcm_client.update_dashboard(user_id=user_id, configure=configure,
                                               title=title, dashboard_type=dashboard_type,
                                               dashboard_name=dashboard_name)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete_dashboard
    try:
        dashboard_name = '_54549'
        response = bcm_client.delete_dashboard(user_id=user_id, dashboard_name=dashboard_name)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # duplicate_dashboard
    try:
        dashboard_name = '_54579'
        response = bcm_client.duplicate_dashboard(user_id=user_id, dashboard_name=dashboard_name)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get_dashboard_widget
    try:
        dashboard_name = '_54579'
        widget_name = '_54579_54586'
        response = bcm_client.get_dashboard_widget(user_id=user_id, dashboard_name=dashboard_name
                                                   , widget_name=widget_name)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create_dashboard_widget
    try:
        dashboard_name = '_54579'
        response = bcm_client.create_dashboard_widget(user_id=user_id, dashboard_name=dashboard_name)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete_dashboard_widget
    try:
        dashboard_name = '_54579'
        widget_name = '_54579_54586'
        response = bcm_client.delete_dashboard_widget(user_id=user_id, dashboard_name=dashboard_name
                                                      , widget_name=widget_name)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # duplicate_dashboard_widget
    try:
        dashboard_name = '_54579'
        widget_name = '_54579_54584'
        response = bcm_client.duplicate_dashboard_widget(user_id=user_id, dashboard_name=dashboard_name
                                                         , widget_name=widget_name)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update_dashboard_widget
    try:
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
        response = bcm_client.update_dashboard_widget(user_id=user_id, dashboard_name=dashboard_name,
                                                      widget_name=widget_name, widget_type=widget_type,
                                                      title=title, configure=configure, )
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get_dashboard_report_data
    try:
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
        response = bcm_client.get_dashboard_report_data(data=data, time=time, config=None)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get_dashboard
    try:
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
        response = bcm_client.get_dashboard_trend_data(data=data, time=time, config=None)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get_dashboard_gauge_chart_data
    try:
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
        response = bcm_client.get_dashboard_gauge_chart_data(data=data, time=time, config=None)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get_dashboard_billboard_data
    try:
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
        response = bcm_client.get_dashboard_billboard_data(data=data, time=time, config=None)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get_dashboard_trend_senior_data
    try:
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
        response = bcm_client.get_dashboard_trend_senior_data(data=data, time=time, config=None)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get_dashboard_dimensions
    try:
        dimensions = "nicName"
        metric_name = "vNicInBytes"
        region = "bj"
        service = "BCE_BEC"
        show_id = "7744b3f3-ec04-459a-b3ae-4379111534ff"
        response = bcm_client.get_dashboard_dimensions(user_id=user_id, metric_name=metric_name, region=region,
                                                       service=service, show_id=show_id, dimensions=dimensions,
                                                       config=None)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create application data
    try:
        response = bcm_client.create_application_data(name="app_name", type="BCC", user_id=user_id,
                                                      alias="testAlias-1213", description="description-1213")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get application data list
    try:
        response = bcm_client.get_application_data_list(user_id=user_id, page_no=1, page_size=10)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update application data
    try:
        response = bcm_client.update_application_data(user_id=user_id, id="1234", name="app_name", type="BCC",
                                                      alias="test", description="description")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete application data
    try:
        response = bcm_client.delete_application_data(user_id=user_id, name="app_name")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get application instance list
    try:
        response = bcm_client.get_application_instance_list(user_id=user_id, region="bj", app_name="test_1213",
                                                            search_name="name", page_no=1, page_size=10,
                                                            search_value="bsm")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create application instance
    try:
        host_list = [{
            "instanceId": "7d4e09af-d01b-4492-88e9-c27d909****",
            "region": "bj"
        }, {
            "instanceId": "d8293318-7d34-433e-928a-b0e72cb3****",
            "region": "bj"
        }]
        response = bcm_client.create_application_instance(user_id=user_id, app_name="app_name", host_list=host_list)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)
    # get application instance created list
    try:
        response = bcm_client.get_application_instance_created_list(user_id=user_id, app_name="app_name", region="bj")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete application instance
    try:
        response = bcm_client.delete_application_instance(user_id=user_id, app_name="app_name", id="7099")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create application instance task
    try:
        response = bcm_client.create_application_instance_task(user_id=user_id, app_name="app_name",
                                                               alias_name="task_proc_test",
                                                               type=0, target="/proc/exe", cycle=300)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create application instance log task
    try:
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
        response = bcm_client.create_application_instance_task(user_id=user_id, app_name="app_name",
                                                               alias_anem="task_log_test", type=2,
                                                               target="/bin/log/info",
                                                               cycle=60, description="test_description",
                                                               log_example=log_example, match_rule=match_rule,
                                                               rate=rate,
                                                               extract_result=extract_result, metrics=metrics)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get application monitor task detail
    try:
        response = bcm_client.get_application_monitor_task_detail(user_id=user_id, app_name="app_name",
                                                                  task_name="9b67163479fe4ffcb31a8a79aaf1****")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    #  get application monitor task list
    try:
        response = bcm_client.get_application_monitor_task_list(user_id=user_id, app_name="app_name")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update application monitor task
    try:
        response = bcm_client.update_application_monitor_task(user_id=user_id, app_anme="app_name",
                                                              alias_name="task_proc_test",
                                                              name="9b67163479fe4ffcb31a8a79aaf1****",
                                                              type=0, target="/proc/bin", cycle=300,
                                                              description="test_description")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)
    #  update application monitor log task
    try:
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
        response = bcm_client.update_application_monitor_task(user_id=user_id, app_anme="app_name",
                                                              alias_name="task_proc_test",
                                                              name="9b67163479fe4ffcb31a8a79aaf1****",
                                                              type=2, target="/proc/bin", cycle=60,
                                                              description="test_description",
                                                              log_example=log_example,
                                                              match_rule=match_rule,
                                                              rate=rate, extract_result=extract_result, metrics=metrics)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete application monitor task
    try:
        response = bcm_client.delete_application_monitor_task(
            user_id=user_id, name="424c68d575d24ef7bcd0b3f5e726****", app_name="app_name")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create application dimension table
    try:
        response = bcm_client.create_application_dimension_table(
            user_id=user_id, app_name="app_name", table_name="test_table", map_content_json="a=>1\nb=>2")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    #    get application dimension table list
    try:
        response = bcm_client.get_application_dimension_table_list(
            user_id=user_id, app_name="app_name", search_name="test")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)
    #  update application dimension table
    try:
        response = bcm_client.update_application_dimension_table(
            user_id=user_id, app_name="app_name", table_name="test_table", map_content_json="a=>1")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    #  delete application dimension table
    try:
        response = bcm_client.delete_application_dimension_table(
            user_id=user_id, app_name="app_name", table_name="test_table")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get cloud event list
    try:
        response = bcm_client.get_cloud_event_data(account_id=user_id,
                                                   start_time="2023-10-01T00:00:00Z", end_time="2023-11-01T01:00:00Z",
                                                   page_no=1, page_size=10)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get platform event list
    try:
        response = bcm_client.get_platform_event_data(account_id=user_id,
                                                      start_time="2023-10-01T00:00:00Z",
                                                      end_time="2023-11-01T01:00:00Z",
                                                      page_no=1, page_size=10)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s' % (
                e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create event policy
    try:
        event_filter = bcm_model.EventFilter(event_level="*", event_type_list=["*"], eventAliasNames=[])
        resource = bcm_model.EventResourceFilter(region="bj", type="Instance", monitor_object_type="ALL", resources=[])
        incident_actions = ["2fc6e953-331a-4404-8ce7-1c0597*****"]
        response = bcm_client.create_event_policy(account_id=user_id, service_name="BCE_BCC", name="event_policy_name",
                                                  block_status="NORMAL", event_filter=event_filter,
                                                  resource=resource, incident_actions=incident_actions)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s' % (
                e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create instance group
    try:
        response = bcm_client.create_instance_group(user_id=user_id, region="bj", service_name="BCE_BCC",
                                                    type_name="Instance", name="py-sdk-test",
                                                    resource_id_list=[])
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s' % (
                e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update instance group
    try:
        response = bcm_client.update_instance_group(user_id=user_id, ig_id="****", region="bj", service_name="BCE_BCC",
                                                    type_name="Instance", name="py-sdk-test-update")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s' % (
                e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete instance group
    try:
        response = bcm_client.delete_instance_group(user_id=user_id, ig_id="****")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s' % (
                e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get instance group detail
    try:
        response = bcm_client.get_instance_group_detail(user_id=user_id, ig_id="****")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s' % (
                e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list instance group
    try:
        response = bcm_client.list_instance_group(user_id=user_id, name="", region="bj", service_name="BCE_BCC",
                                                  type_name="Instance", page_no=1, page_size=10)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s' % (
                e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # add instance to instance group
    try:
        resource_id_list = bcm_model.MonitorResource(user_id=user_id, region="bj", service_name="BCE_BCC",
                                                     type_name="Instance", identifiers=[],
                                                     resource_id="InstanceId:dd0109a3-****-****-b2ae-3c6aa0b63705")
        response = bcm_client.add_ig_instance(ig_id="****", user_id=user_id, resource_id_list=[resource_id_list])
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s' % (
                e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # remove instance from instance group
    try:
        resource_id_list = bcm_model.MonitorResource(user_id=user_id, region="bj", service_name="BCE_BCC",
                                                     type_name="Instance", identifiers=[],
                                                     resource_id="InstanceId:dd0109a3-****-****-b2ae-3c6aa0b63705")
        response = bcm_client.remove_ig_instance(ig_id="****", user_id=user_id, resource_id_list=[resource_id_list])
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s' % (
                e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # query instance in instance group
    try:
        response = bcm_client.list_ig_instance(ig_id="****", user_id=user_id, service_name="BCE_BCC",
                                               type_name="Instance", region="bj", view_type="DETAIL_VIEW",
                                               page_no=1, page_size=10)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s' % (
                e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # query all instances when you create a scaling group
    try:
        response = bcm_client.list_all_instance(user_id=user_id, service_name="BCE_BCC",
                                                type_name="Instance", region="bj", view_type="LIST_VIEW",
                                                keyword_type="name", keyword="", page_no=1, page_size=10)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s' % (
                e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # query filter instances that is not in an instance group
    try:
        response = bcm_client.list_filter_instance(user_id=user_id, service_name="BCE_BCC",
                                                   type_name="Instance", region="bj", view_type="LIST_VIEW",
                                                   keyword_type="name", keyword="", page_no=1, page_size=10,
                                                   ig_id="7923", ig_uuid="bc59b391-2973-****-****-596c0b268682")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error(
                'send request failed. Response %s, code: %s, msg: %s' % (e.last_error.status_code, e.last_error.code,
                                                                         e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)
    # create alarm policy
    try:
        monitor_object = bcm_model.MonitorObject("INSTANCE", ["InstanceId:i-WvElew**"])
        rule = bcm_model.AlarmRule(1, "CPUUsagePercent", 60, "average", "12345", ">", 1)
        bcm_client.create_alarm_config(user_id, "test_policy_0123", "BCE_BCC", "CRITICAL", "bj",
                                       monitor_object, ["d242711b-****-****-****-b8ac175f8e7d"], [[rule]])
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update alarm policy
    try:
        monitor_object = bcm_model.MonitorObject("INSTANCE", ["InstanceId:i-WvElew**"])
        rule = bcm_model.AlarmRule(1, "CPUUsagePercent", 60, "average", "12345", ">", 1)
        bcm_client.update_alarm_config(user_id, "5c09e9********************d62091",
                                       "test_policy_01234", "BCE_BCC", "CRITICAL", "bj",
                                       monitor_object, ["d242711b-****-****-****-b8ac175f8e7d"], [[rule]])
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete alarm policy
    try:
        bcm_client.delete_alarm_config(user_id, "5c09e9********************d62091", "BCE_BCC")
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # block alarm policy
    try:
        bcm_client.block_alarm_config(user_id, "5c09e9********************d62091", "BCE_BCC")
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # unblock alarm policy
    try:
        bcm_client.unblock_alarm_config(user_id, "374e9c8a591847f294a9a695a8a35038", "BCE_BCC")
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get alarm policy detail
    try:
        bcm_client.get_alarm_config_detail(user_id, "5c09e9********************d62091", "BCE_BCC")
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get single instance alarm configs
    try:
        bcm_client.get_single_instance_alarm_configs(user_id, "BCE_BCC", 1, 10)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get alarm metrics
    try:
        bcm_client.get_alarm_metrics(user_id, "BCE_BCC")
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create alarm policy v2
    try:
        action = bcm_model.AlarmAction("test_yangmoda")
        rule = bcm_model.AlarmConfigRule("CPUUsagePercent", ">", "average", 12345.0)
        policy = bcm_model.AlarmConfigPolicy([rule], 1)
        identifier = bcm_model.KV("InstanceId", "i-WvElew**")
        instance = bcm_model.TargetInstance("bj", [identifier])
        bcm_client.create_alarm_config_v2(user_id, "test_policy_01234", "BCE_BCC", "TARGET_TYPE_MULTI_INSTANCES",
                                          "CRITICAL", "bj", [action], [policy], target_instances=[instance])
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update alarm policy v2
    try:
        action = bcm_model.AlarmAction("test_yangmoda")
        rule = bcm_model.AlarmConfigRule("CPUUsagePercent", ">", "average", 12345.0)
        policy = bcm_model.AlarmConfigPolicy([rule], 1)
        identifier = bcm_model.KV("InstanceId", "i-WvElew**")
        instance = bcm_model.TargetInstance("bj", [identifier])
        bcm_client.update_alarm_config_v2(user_id, "5c09e9********************d62091", "test_policy_012345",
                                          "BCE_BCC", "TARGET_TYPE_MULTI_INSTANCES",
                                          "CRITICAL", "bj", [action], [policy], target_instances=[instance])
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # block alarm policy v2
    try:
        bcm_client.block_alarm_config_v2(user_id, "5c09e9********************d62091", "BCE_BCC")
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # unblock alarm policy v2
    try:
        bcm_client.unblock_alarm_config_v2(user_id, "5c09e9********************d62091", "BCE_BCC")
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get alarm policy detail v2
    try:
        bcm_client.get_alarm_config_detail_v2(user_id, "5c09e9********************d62091", "BCE_BCC")
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)


    # query custom metric data from bcm interface
    try:
        response = bcm_client.get_custom_metric_data(user_id=user_id,
                                                     scope="scope_test",
                                                     metric_name="metric_name",
                                                     dimensions=[],
                                                     statistics="average",
                                                     start_time="2023-12-05T09:54:15Z",
                                                     end_time="2023-12-05T10:04:15Z",
                                                     cycle=60)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)


    # push metric data from bcm interface
    try:
        metric_data = [bcm_model.MetricDatum("cpu_test", [], 1.2, "1702555303")]
        response = bcm_client.push_metric_data(user_id=user_id,
                                               scope="scope_test",
                                               metric_data = metric_data)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # push custom metric data from bcm interface
    try:
        response = bcm_client.push_custom_metric_data(user_id=user_id,
                                                      namespace="test_ns", metric_name="pv",
                                                      dimensions=[], value=123, timestamp="2023-12-17T08:00:00Z")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create site http task config
    try:
        response = bcm_client.create_site_http_task_config(user_id=user_id,
                                                           task_name="task_name", address="www.baidu.com",
                                                           method="get", post_content="", advance_config=False,
                                                           cycle=60, idc="beijing-CMNET", timeout = 20)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)


    # update site http task config
    try:
        response = bcm_client.update_site_http_task_config(user_id=user_id,
                                                           task_id="rriHgFGaIaVIqYanAveRMervXWWfQufq",
                                                           task_name="task_name", address="www.baidu.com",
                                                           method="get", post_content="", advance_config=False,
                                                           cycle=60, idc="henan-CMNET", timeout = 20)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get site http task config
    try:
        response = bcm_client.get_site_http_task_config(user_id=user_id,
                                                        task_id="rriHgFGaIaVIqYanAveRMervXWWfQufq")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create site https task config
    try:
        response = bcm_client.create_site_https_task_config(user_id=user_id,
                                                            task_name="task_name", address="www.baidu.com",
                                                            method="get", post_content="", advance_config=False,
                                                            cycle=60, idc="beijing-CMNET", timeout = 20)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)


    # update site https task config
    try:
        response = bcm_client.update_site_https_task_config(user_id=user_id,
                                                            task_id="rriHgFGaIaVIqYanAveRMervXWWfQufq",
                                                            task_name="task_name", address="www.baidu.com",
                                                            method="get", post_content="", advance_config=False,
                                                            cycle=60, idc="henan-CMNET", timeout = 20)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get site https task config
    try:
        response = bcm_client.get_site_https_task_config(user_id=user_id,
                                                         task_id="rriHgFGaIaVIqYanAveRMervXWWfQufq")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create site ping task config
    try:
        response = bcm_client.create_site_ping_task_config(user_id=user_id,
                                                           task_name="task_name", address="www.baidu.com",
                                                           packet_count=1, packet_loss_rate=1,
                                                           cycle=60, idc="beijing-CMNET", timeout = 20)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)


    # update site ping task config
    try:
        response = bcm_client.update_site_ping_task_config(user_id=user_id,
                                                           task_id="VoFXOMtXwLJSWgxIUjavNPgHcdznwivS",
                                                           task_name="task_name", address="www.baidu.com",
                                                           packet_count=1, packet_loss_rate=1,
                                                           cycle=60, idc="henan-CMNET", timeout = 20)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get site ping task config
    try:
        response = bcm_client.get_site_ping_task_config(user_id=user_id,
                                                        task_id="VoFXOMtXwLJSWgxIUjavNPgHcdznwivS")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create site tcp task config
    try:
        response = bcm_client.create_site_tcp_task_config(user_id=user_id,
                                                          task_name="task_name", address="www.baidu.com",
                                                          port=80, advance_config=False,
                                                          cycle=60, idc="beijing-CMNET", timeout = 2,
                                                          input_type=0, output_type=0, input="", expected_output="")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)


    # update site tcp task config
    try:
        response = bcm_client.update_site_tcp_task_config(user_id=user_id,
                                                          task_id="JAbvZxtXWxreAkiHgFnPtEQqBWcZzkjU",
                                                          task_name="task_name", address="www.baidu.com",
                                                          port=80, advance_config=False,
                                                          cycle=60, idc="beijing-CMNET", timeout = 3,
                                                          input_type=0, output_type=0, input="", expected_output="")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get site tcp task config
    try:
        response = bcm_client.get_site_tcp_task_config(user_id=user_id,
                                                       task_id="VoFXOMtXwLJSWgxIUjavNPgHcdznwivS")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create site udp task config
    try:
        response = bcm_client.create_site_udp_task_config(user_id=user_id,
                                                          task_name="task_name", address="www.baidu.com",
                                                          port=80, advance_config=False,
                                                          cycle=60, idc="beijing-CMNET", timeout = 2,
                                                          input_type=0, output_type=0, input="", expected_output="")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)


    # update site udp task config
    try:
        response = bcm_client.update_site_udp_task_config(user_id=user_id,
                                                          task_id="JAbvZxtXWxreAkiHgFnPtEQqBWcZzkjU",
                                                          task_name="task_name", address="www.baidu.com",
                                                          port=80, advance_config=False,
                                                          cycle=60, idc="beijing-CMNET", timeout = 3,
                                                          input_type=0, output_type=0, input="", expected_output="")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get site udp task config
    try:
        response = bcm_client.get_site_udp_task_config(user_id=user_id,
                                                       task_id="JAbvZxtXWxreAkiHgFnPtEQqBWcZzkjU")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create site ftp task config
    try:
        response = bcm_client.create_site_ftp_task_config(user_id=user_id,
                                                          task_name="task_name", address="www.baidu.com",
                                                          port=80, anonymous_login=False,
                                                          cycle=60, idc="beijing-CMNET", timeout = 3,
                                                          user_name="", password="")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)


    # update site ftp task config
    try:
        response = bcm_client.update_site_ftp_task_config(user_id=user_id,
                                                          task_id="JAbvZxtXWxreAkiHgFnPtEQqBWcZzkjU",
                                                          task_name="task_name", address="www.baidu.com",
                                                          port=80, anonymous_login=False,
                                                          cycle=60, idc="beijing-CMNET", timeout = 3,
                                                          user_name="", password="")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get site ftp task config
    try:
        response = bcm_client.get_site_ftp_task_config(user_id=user_id,
                                                       task_id="JAbvZxtXWxreAkiHgFnPtEQqBWcZzkjU")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create site dns task config
    try:
        response = bcm_client.create_site_dns_task_config(user_id=user_id,
                                                          task_name="task_name", address="www.baidu.com",
                                                          cycle=60, idc="beijing-CMNET", timeout = 3,
                                                          resolve_type="RECURSION", kidnap_white="")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)


    # update site dns task config
    try:
        response = bcm_client.update_site_dns_task_config(user_id=user_id,
                                                          task_id="SisKPHhkfWQvkRUeUGZYGuLLSDymnTsA",
                                                          task_name="task_name", address="www.baidu.com",
                                                          cycle=60, idc="beijing-CMNET", timeout = 3,
                                                          resolve_type="RECURSION", kidnap_white="")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get site dns task config
    try:
        response = bcm_client.get_site_dns_task_config(user_id=user_id,
                                                       task_id="SisKPHhkfWQvkRUeUGZYGuLLSDymnTsA")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)


    # get site task config list
    try:
        response = bcm_client.get_site_task_config_list(user_id=user_id,
                                                        query=None, type="http", page_no=1, page_size=10)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete site task config
    try:
        response = bcm_client.delete_site_task_config(user_id=user_id,
                                                      task_id="rriHgFGaIaVIqYanAveRMervXWWfQufq")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get site task config info
    try:
        response = bcm_client.get_site_task_config_info(user_id=user_id,
                                                        task_id="SisKPHhkfWQvkRUeUGZYGuLLSDymnTsA")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create site alarm config
    try:
        rule = bcm_model.SiteAlarmRule("connectTime",
                                       None,
                                       60, "average", 10, ">", 1,
                                       "THRESHOLD", ["average"], [], None)
        response = bcm_client.create_site_alarm_config(user_id=user_id,
                                                       task_id="SisKPHhkfWQvkRUeUGZYGuLLSDymnTsA",
                                                       comment="", alias_name="pyy_test",
                                                       level="MAJOR", action_enabled=True,
                                                       resume_actions=["37eddd21-a44c-42c6-b0bb-a3e9d738a091"],
                                                       insufficient_actions=["37eddd21-a44c-42c6-b0bb-a3e9d738a091"],
                                                       incident_action=["37eddd21-a44c-42c6-b0bb-a3e9d738a091"],
                                                       insufficient_cycle=0, rules=[rule], region="bj",
                                                       callback_url="", method=None, site_monitor=None, tag="")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update site alarm config
    try:
        rule = bcm_model.SiteAlarmRule("connectTime",
                                       None,
                                       60, "average", 10, ">", 1,
                                       "THRESHOLD", ["average"], [], None)
        response = bcm_client.update_site_alarm_config(user_id=user_id,
                                                       task_id="SisKPHhkfWQvkRUeUGZYGuLLSDymnTsA",
                                                       alarm_name="b87ffe8c1c584b09b2baf15e6244d55d",
                                                       comment="", alias_name="pyy_test",
                                                       level="MAJOR", action_enabled=True,
                                                       resume_actions=["37eddd21-a44c-42c6-b0bb-a3e9d738a091"],
                                                       insufficient_actions=["37eddd21-a44c-42c6-b0bb-a3e9d738a091"],
                                                       incident_action=["37eddd21-a44c-42c6-b0bb-a3e9d738a091"],
                                                       insufficient_cycle=60, rules=[rule], region="bj",
                                                       callback_url="", method=None, site_monitor=None, tag="")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete site alarm config
    try:
        response = bcm_client.delete_site_alarm_config(user_id=user_id,
                                                       alarm_names=["b87ffe8c1c584b09b2baf15e6244d55d"])
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get site alarm config detail
    try:
        response = bcm_client.get_site_alarm_config_detail(user_id=user_id,
                                                           alarm_name="b87ffe8c1c584b09b2baf15e6244d55d")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get site alarm config list
    try:
        response = bcm_client.get_site_alarm_config_list(user_id=user_id,
                                                         alarm_name="b87ffe8c1c584b09b2baf15e6244d55d",
                                                         task_id=None, action_enabled=True,
                                                         page_no=1, page_size=10)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # block site alarm config
    try:
        response = bcm_client.block_site_alarm_config(user_id=user_id,
                                                      alarm_name="b87ffe8c1c584b09b2baf15e6244d55d",
                                                      namespace=None)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # unblock site alarm config
    try:
        response = bcm_client.unblock_site_alarm_config(user_id=user_id,
                                                        alarm_name="b87ffe8c1c584b09b2baf15e6244d55d",
                                                        namespace=None)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get site metric data
    try:
        response = bcm_client.get_site_metric_data(user_id=user_id,
                                                   task_id="VoFXOMtXwLJSWgxIUjavNPgHcdznwivS",
                                                   metric_name="success", statistics=["average", "sum"],
                                                   start_time="2023-12-19T06:09:12Z",
                                                   end_time="2023-12-19T06:19:12Z",
                                                   cycle=60, dimensions=None)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get site overall view
    try:
        response = bcm_client.get_site_overall_view(user_id=user_id,
                                                    task_id="VoFXOMtXwLJSWgxIUjavNPgHcdznwivS")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get site provincial view
    try:
        response = bcm_client.get_site_provincial_view(user_id=user_id,
                                                       task_id="VoFXOMtXwLJSWgxIUjavNPgHcdznwivS",
                                                       isp="beijing")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get site agent
    try:
        response = bcm_client.get_site_agent(user_id=user_id)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get site agent for task
    try:
        response = bcm_client.get_site_agent_for_task(user_i=user_id,
                                                      task_id="VoFXOMtXwLJSWgxIUjavNPgHcdznwivS")
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create alarm policy for customNamespace
    try:
        rule = bcm_model.CustomAlarmRule(custom_metric_name, 60, "average", 10, ">", 1, 1, [])

        response = bcm_client.create_custom_alarm_policy(user_id, "test_policy_zz", custom_namespace, "MAJOR",
                                                         rules=[rule])
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete alarm policy for customNamespace
    try:
        custom_alarm_list = [
            {
                "scope": "test_qsh",
                "userId": "a0d04d7c202140cb80155ff7********",
                "alarmName": [
                    "test_policy_zz"
                ]
            }
        ]
        response = bcm_client.delete_custom_alarm_policy(custom_alarm_list)
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # update alarm policy for customNamespace
    try:
        rule = bcm_model.CustomAlarmRule(custom_metric_name, 60, "average", 10, ">", 1, 1, [])

        response = bcm_client.update_custom_alarm_policy(user_id, "test_policy_13", custom_namespace, "MAJOR",
                                                         rules=[rule])
        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list alarm policies for customNamespace
    try:
        res = bcm_client.list_custom_policy("a0d04d7c202140cb80155ff7********", 1, 10)
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # detail alarm policy for customNamespace
    try:
        res = bcm_client.detail_custom_policy("a0d04d7c202140cb80155ff7********", "test_qsh", "test_policy_zz")
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # block alarm policy for customNamespace
    try:
        res = bcm_client.block_custom_policy("a0d04d7c202140cb80155ff7********", "test_qsh", "test_policy_zz")
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # unblock alarm policy for customNamespace
    try:
        res = bcm_client.unblock_custom_policy("a0d04d7c202140cb80155ff7********", "test_qsh", "test_policy_zz")
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # create site once task
    try:
        onceConfig = SiteOnceConfig(method="get")
        res = bcm_client.create_site_once_task("HTP", "a0d04d7c202140cb80155ff7********", "www.baidu.com",
                                               "beijing-CMNET", 60, "HTTP", once_config=onceConfig)
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list site once records
    try:
        res = bcm_client.list_site_once_records()
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # delete site once record
    try:
        res = bcm_client.delete_site_once_record("a0d04d7c202140cb80155ff7********", "OMVQcQTDPmSeLIXAsJEKAAbZwynfOINu")
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # detail site once result
    try:
        res = bcm_client.detail_site_once_result("a0d04d7c202140cb80155ff7********", "OMVQcQTDPmSeLIXAsJEKAAbZwynfOINu",
                                                 filter_area="beijing")
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # detail site once
    try:
        res = bcm_client.detail_site_once("a0d04d7c202140cb80155ff7********")
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # again exec site once
    try:
        res = bcm_client.again_exec_site_once("a0d04d7c202140cb80155ff7********", "OMVQcQTDPmSeLIXAsJEKAAbZwynfOINu")
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # list site once history
    try:
        res = bcm_client.list_site_once_history(user_id="a0d04d7c202140cb80155ff7********")
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get site agent
    try:
        res = bcm_client.get_site_once_agent(user_id="a0d04d7c202140cb80155ff7********")
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get multi dimension latest metrics
    try:
        res = bcm_client.get_multi_dimension_latest_metrics(user_id="a0d04d7c202140cb80155ff7********",
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
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)


    # get metrics by partial dimension at fully param
    try:
        res = bcm_client.get_metrics_by_partial_dimensions(user_id="a0d04d7c202140cb80155ff7********",
                                                           scope="BCE_BLB",
                                                           resource_type="Blb",
                                                           metric_name="ActiveConnCount",
                                                           statistics=[
                                                               "average",
                                                               "sum",
                                                               "minimum"
                                                           ],
                                                           dimensions=[{"name": "BlbPortType", "value": "TCP"}],
                                                           region="bj",
                                                           cycle=60,
                                                           start_time="2024-03-20T02:21:17Z",
                                                           end_time="2024-03-20T03:21:17Z",
                                                           pageNo=2,
                                                           pageSize=5)
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    # get metrics by partial dimension at least params
    try:
        res = bcm_client.get_metrics_by_partial_dimensions(user_id="a0d04d7c202140cb80155ff7********",
                                                           scope="BCE_BCC",
                                                           metric_name="CpuIdlePercent",
                                                           statistics=[
                                                               "average",
                                                               "sum",
                                                               "minimum"
                                                           ],
                                                           start_time="2024-03-20T02:21:17Z",
                                                           end_time="2024-03-20T03:21:17Z")
        print(res)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)