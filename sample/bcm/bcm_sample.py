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
