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
This module provides a client class for BCM.
"""
import copy
import json
import sys
import uuid

from baidubce import bce_base_client, utils, compat
from baidubce.auth import bce_v1_signer
from baidubce.http import handler, bce_http_client, http_methods
from baidubce.services.bcm import bcm_handler, bcm_model
from baidubce.utils import required

if sys.version_info[0] == 2:
    value_type = (str, unicode)
else:
    value_type = (str, bytes)

MAX_INSTANCE_NUMBER = 100


class BcmClient(bce_base_client.BceBaseClient):
    """
    BCM base sdk client
    """

    prefix = b'/json-api'
    csm_prefix = b'/csm/api'
    event_prefix = b'/event-api'
    version = b'/v1'
    version_v2 = b'/v2'

    content_type_header_key = b"content-type"
    content_type_header_value = b"application/json;charset=UTF-8"
    request_id_header_key = b"x-bce-request-id"

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)

    def _merge_config(self, config=None):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, path,
                      body=None, headers=None, params=None,
                      config=None, body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, BcmClient.prefix + BcmClient.version + path, body, headers, params)

    def _send_csm_request(self, http_method, path, version=b'/v1',
                          body=None, headers=None, params=None, config=None, body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json
        if headers is None:
            headers = {}
        if self.content_type_header_key not in headers:
            headers[self.content_type_header_key] = self.content_type_header_value
        if self.request_id_header_key not in headers:
            headers[self.request_id_header_key] = uuid.uuid4()

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [bcm_handler.parse_error, body_parser],
            http_method, BcmClient.csm_prefix + version + path, body, headers, params)

    def _send_event_request(self, http_method, path,
                            body=None, headers=None, params=None, config=None, body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json
        if headers is None:
            headers = {}
        if self.content_type_header_key not in headers:
            headers[self.content_type_header_key] = self.content_type_header_value
        if self.request_id_header_key not in headers:
            headers[self.request_id_header_key] = uuid.uuid4()

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [bcm_handler.parse_error, body_parser],
            http_method, BcmClient.event_prefix + BcmClient.version + path, body, headers, params)

    def get_metric_data(self, user_id=None, scope=None, metric_name=None,
                        dimensions=None, statistics=None, start_time=None,
                        end_time=None, period_in_second=None, config=None):
        """
        Return metric data of product instances owned by the authenticated user.

        This site may help you: https://cloud.baidu.com/doc/BCM/s/9jwvym3kb

        :param user_id:
            Master account ID
        :type user_id: string

        :param scope:
            Cloud product namespace, eg: BCE_BCC.
        :type scope: string

        :param metric_name:
            The metric name of baidu cloud monitor, eg: CpuIdlePercent.
        :type metric_name: string

        :param dimensions:
            Consists of dimensionName: dimensionValue.
            Use semicolons when items have multiple dimensions,
            such as dimensionName: dimensionValue; dimensionName: dimensionValue.
            Only one dimension value can be specified for the same dimension.
            eg: InstanceId:fakeid-2222
        :type dimensions: string

        :param statistics:
            According to the format of statistics1,statistics2,statistics3,
            the optional values are `average`, `maximum`, `minimum`, `sum`, `sampleCount`
        :type statistics: string

        :param start_time:
            Query start time.
            Please refer to the date and time, UTC date indication
        :type start_time: string

        :param end_time:
            Query end time.
            Please refer to the date and time, UTC date indication
        :type end_time: string

        :param period_in_second:
            Statistical period.
            Multiples of 60 in seconds (s).
        :type period_in_second: int

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        user_id = compat.convert_to_bytes(user_id)
        scope = compat.convert_to_bytes(scope)
        metric_name = compat.convert_to_bytes(metric_name)
        path = b'/metricdata/%s/%s/%s' % (user_id, scope, metric_name)
        params = {}

        if dimensions is not None:
            params[b'dimensions'] = dimensions
        if statistics is not None:
            params[b'statistics[]'] = statistics
        if start_time is not None:
            params[b'startTime'] = start_time
        if end_time is not None:
            params[b'endTime'] = end_time
        if period_in_second is not None:
            params[b'periodInSecond'] = period_in_second

        return self._send_request(http_methods.GET, path, params=params, config=config)

    def get_batch_metric_data(self, user_id=None, scope=None, metric_name=None,
                              dimensions=None, statistics=None, start_time=None,
                              end_time=None, period_in_second=None, config=None):
        """
            Return batch metric data of product instances owned by the authenticated user.

            :param user_id:
                Master account ID
            :type user_id: string

            :param scope:
                Cloud product namespace, eg: BCE_BCC.
            :type scope: string

            :param metric_name:
                The metric name of baidu cloud monitor, eg: CpuIdlePercent.
                Use comma when items have multiple metrics,
                such as metric1,metric2,metric3.
            :type metric_name: string

            :param dimensions:
                Consists of dimensionName:dimensionValue.
                Use comma when items have multiple dimensions,
                such as dimensionName:dimensionValue,dimensionName:dimensionValue.
                Only one dimension value can be specified for the same dimension.
                eg: InstanceId:itk-1010,InstanceId:itk-1011
            :type dimensions: string

            :param statistics:
                According to the format of statistics1,statistics2,statistics3,
                the optional values are `average`, `maximum`, `minimum`, `sum`, `sampleCount`
            :type statistics: string

            :param start_time:
                Query start time.
                Please refer to the date and time, UTC date indication
            :type start_time: string

            :param end_time:
                Query end time.
                Please refer to the date and time, UTC date indication
            :type end_time: string

            :param period_in_second:
                Statistical period.
                Multiples of 60 in seconds (s).
            :type period_in_second: int

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        user_id = compat.convert_to_bytes(user_id)
        scope = compat.convert_to_bytes(scope)
        path = b'/metricdata/batch/%s/%s' % (user_id, scope)
        params = {}

        if metric_name is not None:
            params[b'metricName[]'] = metric_name
        if dimensions is not None:
            params[b'dimensions[]'] = dimensions
        if statistics is not None:
            params[b'statistics[]'] = statistics
        if start_time is not None:
            params[b'startTime'] = start_time
        if end_time is not None:
            params[b'endTime'] = end_time
        if period_in_second is not None:
            params[b'periodInSecond'] = period_in_second

        return self._send_request(http_methods.GET, path, params=params, config=config)

    def create_namespace(self, user_id, name, namespace_alias=None, comment=None, config=None):
        """
            create a custom namespace for custom monitor

            This site may help you: https://cloud.baidu.com/doc/BCM/s/cktnhszhv

            :param user_id:
                master account id
            :type user_id: string

            :param name:
                namespace name
            :type name: string

            :param namespace_alias:
                namespace alias name
            :type namespace_alias: string

            :param comment:
                namespace comment
            :type user_id: string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(name) <= 0:
            raise ValueError('name should not be none or empty string')

        path = b'/userId/%s/custom/namespaces/create' % compat.convert_to_bytes(user_id)
        body = {
            "userId": user_id,
            "name": name,
            "namespaceAlias": namespace_alias,
            "comment": comment,
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def batch_delete_namespaces(self, user_id, names, config=None):
        """
            create a custom namespace for custom monitor

            This site may help you: https://cloud.baidu.com/doc/BCM/s/cktnhszhv

            :param user_id:
                master account id
            :type user_id: string

            :param names:
                namespace name collection
            :type names: string array

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(names) <= 0:
            raise ValueError('names should not be empty')

        path = b'/userId/%s/custom/namespaces/delete' % compat.convert_to_bytes(user_id)
        body = {
            "userId": user_id,
            "names": names,
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def update_namespace(self, user_id, name, namespace_alias=None, comment=None, config=None):
        """
            update a custom namespace for custom monitor

            This site may help you: https://cloud.baidu.com/doc/BCM/s/cktnhszhv

            :param user_id:
                master account id
            :type user_id: string

            :param name:
                namespace name
            :type name: string

            :param namespace_alias:
                namespace alias name
            :type namespace_alias: string

            :param comment:
                namespace comment
            :type user_id: string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(name) <= 0:
            raise ValueError('name should not be none or empty string')

        path = b'/userId/%s/custom/namespaces/update' % compat.convert_to_bytes(user_id)
        body = {
            "userId": user_id,
            "name": name,
            "namespaceAlias": namespace_alias,
            "comment": comment,
        }
        return self._send_csm_request(http_methods.PUT, path, body=json.dumps(body), config=config)

    def list_namespaces(self, user_id, name=None, page_no=None, page_size=None, config=None):
        """
            list custom namespaces

            This site may help you: https://cloud.baidu.com/doc/BCM/s/cktnhszhv

            :param user_id:
                master account id
            :type user_id: string

            :param name:
                namespace name prefix for query
            :type name: string

            :param page_no:
                page number
            :type page_no: int

            :param page_size:
                page size
            :type page_size: int

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')

        path = b'/userId/%s/custom/namespaces/list' % compat.convert_to_bytes(user_id)
        params = {
            b'userId': user_id,
        }
        if name is not None:
            params[b'name'] = name
        if page_no is None:
            params[b'pageNo'] = 1
        else:
            params[b'pageNo'] = page_no
        if page_size is None:
            params[b'pageSize'] = 10
        else:
            params[b'pageSize'] = page_size

        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def create_namespace_metric(self, user_id, namespace, metric_name,
                                metric_alias=None, unit=None, cycle=None, dimensions=None, config=None):
        """
            create custom metric in one namespace

            This site may help you: https://cloud.baidu.com/doc/BCM/s/cktnhszhv

            :param user_id:
                master account id
            :type user_id: string

            :param namespace:
                namespace name
            :type namespace: string

            :param metric_name:
                custom metric name
            :type metric_name: string

            :param metric_alias:
                custom metric alias
            :type metric_alias: string

            :param unit:
                custom metric unit
            :type unit: string

            :param unit:
                custom metric unit
            :type unit: string

            :param cycle:
                custom metric cycle
            :type cycle: int

            :param dimensions:
                custom dimension collection
            :type dimensions: CustomDimensionModel array

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(namespace) <= 0:
            raise ValueError('namespace should not be none or empty string')
        if len(metric_name) <= 0:
            raise ValueError('metric_name should not be none or empty string')

        path = (b'/userId/%s/custom/namespaces/%s/metrics/create' %
                (compat.convert_to_bytes(user_id), compat.convert_to_bytes(namespace)))
        body = {
            "userId": user_id,
            "namespace": namespace,
            "metricName": metric_name,
        }
        if metric_alias is not None:
            body["metricAlias"] = metric_alias
        if unit is not None:
            body["unit"] = unit
        if cycle is not None:
            body["cycle"] = cycle
        else:
            body["cycle"] = 60
        if dimensions is not None:
            body["dimensions"] = dimensions
        else:
            body["dimensions"] = []

        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def batch_delete_namespace_metrics(self, user_id, namespace, ids, config=None):
        """
            batch delete custom metric in one namespace

            This site may help you: https://cloud.baidu.com/doc/BCM/s/cktnhszhv

            :param user_id:
                master account id
            :type user_id: string

            :param namespace:
                custom namespace name
            :type namespace: string

            :param ids:
                namespace metric id collection
            :type ids: int array

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(ids) <= 0:
            raise ValueError('ids should not be empty')

        path = (b'/userId/%s/custom/namespaces/%s/metrics/delete' %
                (compat.convert_to_bytes(user_id), compat.convert_to_bytes(namespace)))
        body = {
            "userId": user_id,
            "namespace": namespace,
            "ids": ids,
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def update_namespace_metric(self, user_id, namespace, metric_name,
                                metric_alias=None, unit=None, cycle=None, dimensions=None, config=None):
        """
            update custom metric in one namespace

            This site may help you: https://cloud.baidu.com/doc/BCM/s/cktnhszhv

            :param user_id:
                master account id
            :type user_id: string

            :param namespace:
                namespace name
            :type namespace: string

            :param metric_name:
                custom metric name
            :type metric_name: string

            :param metric_alias:
                custom metric alias
            :type metric_alias: string

            :param unit:
                custom metric unit
            :type unit: string

            :param unit:
                custom metric unit
            :type unit: string

            :param cycle:
                custom metric cycle
            :type cycle: int

            :param dimensions:
                custom dimension collection
            :type dimensions: CustomDimensionModel array

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(namespace) <= 0:
            raise ValueError('namespace should not be none or empty string')
        if len(metric_name) <= 0:
            raise ValueError('metric_name should not be none or empty string')
        if cycle is None:
            raise ValueError('cycle should not be none')

        path = (b'/userId/%s/custom/namespaces/%s/metrics/%s' % (compat.convert_to_bytes(user_id),
                                                                 compat.convert_to_bytes(namespace),
                                                                 compat.convert_to_bytes(metric_name)))
        body = {
            "userId": user_id,
            "namespace": namespace,
            "metricName": metric_name,
            "cycle": cycle,
        }
        if metric_alias is not None:
            body["metricAlias"] = metric_alias
        if unit is not None:
            body["unit"] = unit
        if dimensions is not None:
            body["dimensions"] = dimensions

        return self._send_csm_request(http_methods.PUT, path, body=json.dumps(body), config=config)

    def list_namespace_metrics(self, user_id, namespace,
                               metric_name=None, metric_alias=None, page_no=None, page_size=None, config=None):
        """
            list custom metric in one namespace

            This site may help you: https://cloud.baidu.com/doc/BCM/s/cktnhszhv

            :param user_id:
                master account id
            :type user_id: string

            :param namespace:
                namespace name
            :type namespace: string

            :param metric_name:
                custom metric name prefix for query
            :type metric_name: string

            :param metric_alias:
                custom metric alias prefix for query
            :type metric_alias: string

            :param page_no:
                page number
            :type page_no: int

            :param page_size:
                page size
            :type page_size: int

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(namespace) <= 0:
            raise ValueError('namespace should not be none or empty string')

        path = b'/userId/%s/custom/namespaces/metrics' % compat.convert_to_bytes(user_id)
        params = {
            b'userId': user_id,
            b'namespace': namespace,
        }
        if metric_name is not None:
            params[b'metricName'] = metric_name
        if metric_alias is not None:
            params[b'metricAlias'] = metric_alias
        if page_no is None:
            params[b'pageNo'] = 1
        else:
            params[b'pageNo'] = page_no
        if page_size is None:
            params[b'pageSize'] = 10
        else:
            params[b'pageSize'] = page_size

        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def get_custom_metric(self, user_id, namespace, metric_name, config=None):
        """
            get custom metric detail

            This site may help you: https://cloud.baidu.com/doc/BCM/s/cktnhszhv

            :param user_id:
                master account id
            :type user_id: string

            :param namespace:
                namespace name
            :type namespace: string

            :param metric_name:
                custom metric name
            :type metric_name: string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(namespace) <= 0:
            raise ValueError('namespace should not be none or empty string')
        if len(metric_name) <= 0:
            raise ValueError('metric_name should not be none or empty string')

        path = (b'/userId/%s/custom/namespaces/%s/metrics/%s' % (compat.convert_to_bytes(user_id),
                                                                 compat.convert_to_bytes(namespace),
                                                                 compat.convert_to_bytes(metric_name)))
        params = {}

        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def create_namespace_event(self, user_id, namespace, event_name, event_level,
                               event_name_alias=None, comment=None, config=None):
        """
            create custom event in one namespace

            This site may help you: https://cloud.baidu.com/doc/BCM/s/cktnhszhv

            :param user_id:
                master account id
            :type user_id: string

            :param namespace:
                namespace name
            :type namespace: string

            :param event_level:
                custom event level
            :type event_level: ENUM {'NOTICE', 'WARNING', 'MAJOR', 'CRITICAL'}

            :param event_name:
                custom event name
            :type event_name: string

            :param event_name_alias:
                custom event alias
            :type event_name_alias: string

            :param comment:
                custom event comment
            :type comment: string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(namespace) <= 0:
            raise ValueError('namespace should not be none or empty string')
        if len(event_name) <= 0:
            raise ValueError('event_name should not be none or empty string')
        if not bcm_model.EventLevel.contains(event_level):
            raise ValueError('event_level must be one of %s' % str(bcm_model.EventLevel.all_event_levels()))

        path = b'/custom/event/configs/create'
        body = {
            "userId": user_id,
            "namespace": namespace,
            "eventName": event_name,
            "eventLevel": event_level,
        }
        if event_name_alias is not None:
            body["eventNameAlias"] = event_name_alias
        if comment is not None:
            body["comment"] = comment

        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def batch_delete_namespace_events(self, user_id, namespace, names, config=None):
        """
            batch delete custom metric in one namespace

            This site may help you: https://cloud.baidu.com/doc/BCM/s/cktnhszhv

            :param user_id:
                master account id
            :type user_id: string

            :param namespace:
                custom namespace name
            :type namespace: string

            :param names:
                namespace event name collection
            :type names: string array

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(names) <= 0:
            raise ValueError('names should not be empty')

        path = b'/custom/event/configs/delete'
        body = {
            "userId": user_id,
            "namespace": namespace,
            "names": names,
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def update_namespace_event(self, user_id, namespace, event_name, event_level,
                               event_name_alias=None, comment=None, config=None):
        """
            update custom event in one namespace

            This site may help you: https://cloud.baidu.com/doc/BCM/s/cktnhszhv

            :param user_id:
                master account id
            :type user_id: string

            :param namespace:
                namespace name
            :type namespace: string

            :param event_level:
                custom event level
            :type event_level: ENUM {'NOTICE', 'WARNING', 'MAJOR', 'CRITICAL'}

            :param event_name:
                custom event name
            :type event_name: string

            :param event_name_alias:
                custom event alias
            :type event_name_alias: string

            :param comment:
                custom event comment
            :type comment: string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(namespace) <= 0:
            raise ValueError('namespace should not be none or empty string')
        if len(event_name) <= 0:
            raise ValueError('event_name should not be none or empty string')
        if not bcm_model.EventLevel.contains(event_level):
            raise ValueError('event_level must be one of %s' % str(bcm_model.EventLevel.all_event_levels()))

        path = b'/custom/event/configs/update'
        body = {
            "userId": user_id,
            "namespace": namespace,
            "eventName": event_name,
            "eventLevel": event_level,
        }
        if event_name_alias is not None:
            body["eventNameAlias"] = event_name_alias
        if comment is not None:
            body["comment"] = comment

        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def list_namespace_events(self, user_id, namespace,
                              name=None, event_level=None, page_no=None, page_size=None, config=None):
        """
            list custom event in one namespace

            This site may help you: https://cloud.baidu.com/doc/BCM/s/cktnhszhv

            :param user_id:
                master account id
            :type user_id: string

            :param namespace:
                namespace name
            :type namespace: string

            :param name:
                custom metric name prefix for query
            :type name: string

            :param event_level:
                custom metric level
            :type event_level: None or ENUM {'NOTICE', 'WARNING', 'MAJOR', 'CRITICAL'}

            :param page_no:
                page number
            :type page_no: int

            :param page_size:
                page size
            :type page_size: int

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(namespace) <= 0:
            raise ValueError('namespace should not be none or empty string')
        if event_level is not None and (not bcm_model.EventLevel.contains(event_level)):
            raise ValueError('event_level must be none or one of %s' % str(bcm_model.EventLevel.all_event_levels()))

        path = b'/custom/event/configs/list'
        params = {
            b'userId': user_id,
            b'namespace': namespace,
        }
        if name is not None:
            params[b'name'] = name
        if event_level is not None:
            params[b'event_level'] = event_level
        if page_no is None:
            params[b'pageNo'] = 1
        else:
            params[b'pageNo'] = page_no
        if page_size is None:
            params[b'pageSize'] = 10
        else:
            params[b'pageSize'] = page_size

        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def get_custom_event(self, user_id, namespace, event_name, config=None):
        """
            get custom event detail

            This site may help you: https://cloud.baidu.com/doc/BCM/s/cktnhszhv

            :param user_id:
                master account id
            :type user_id: string

            :param namespace:
                namespace name
            :type namespace: string

            :param event_name:
                custom event name
            :type event_name: string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(namespace) <= 0:
            raise ValueError('namespace should not be none or empty string')
        if len(event_name) <= 0:
            raise ValueError('metric_name should not be none or empty string')

        path = b'/custom/event/configs/detail'
        params = {
            b"userId": user_id,
            b"namespace": namespace,
            b"eventName": event_name,
        }

        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    @required(page_no=int, page_size=int)
    def list_notify_group(self, page_no, page_size, name=None):
        """
            :param name: notify name
            :type name: string
            :param page_no: page number
            :type page_no: int
            :param page_size: page size
            :type page_size: int

            :return
            :rtype baidubce.bce_response.BceResponse
        """
        headers = {self.content_type_header_key: self.content_type_header_value}
        path = b'/alarm/notify/group/list'
        body = {
            "name": name,
            "pageNo": page_no,
            "pageSize": page_size
        }

        return self._send_request(http_methods.POST, path, headers=headers, body=json.dumps(body))

    @required(page_no=int, page_size=int)
    def list_notify_party(self, page_no, page_size, name=None):
        """
            :param name: notify name
            :type name: string
            :param page_no: page number
            :type page_no: int
            :param page_size: page size
            :type page_size: int

            :return
            :rtype baidubce.bce_response.BceResponse
        """
        headers = {self.content_type_header_key: self.content_type_header_value}
        path = b'/alarm/notify/party/list'
        body = {
            "name": name,
            "pageNo": page_no,
            "pageSize": page_size
        }

        return self._send_request(http_methods.POST, path, headers=headers, body=json.dumps(body))

    @required(page_no=int, page_size=int, notifications=list, members=list)
    def create_action(self, user_id, notifications, members, alias, disable_times=None, action_callbacks=None):
        """
        :param user_id:
        :type user_id: string
        :param notifications:
        :type notifications: list of bcm_model.Notification
        :param members:
        :type members: list of bcm_model.Member
        :param alias: action's alias
        :type alias: string
        :param disable_times: disable time
        :type disable_times: list of bcm_model.DisableTime
        :param action_callbacks: list of action callback
        :type action_callbacks: list

        :return
        :rtype baidubce.bce_response.BceResponse
        """
        if disable_times is None:
            disable_times = []
        if action_callbacks is None:
            action_callbacks = []
        path = b'/userId/%s/action/create' % compat.convert_to_bytes(user_id)
        body = {
            "userId": user_id,
            "notifications": notifications,
            "members": members,
            "alias": alias,
            "disableTimes": disable_times,
            "actionCallBacks": action_callbacks
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body))

    def delete_action(self, user_id, name):
        """

        :param user_id:
        :type user_id: string
        :param name: action name
        :type name: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/userId/%s/action/delete' % compat.convert_to_bytes(user_id)
        params = {b'name': name}
        return self._send_csm_request(http_methods.DELETE, path, params=params)

    @required(page_no=int, page_size=int)
    def list_action(self, user_id, page_no, page_size, name=None, order=None):
        """

        :param user_id:
        :type user_id: string
        :param page_no: page number
        :type page_no: int
        :param page_size: page size
        :type page_size: int
        :param name: action name
        :type name: string
        :param order: desc or asc
        :type name: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/userId/%s/action/actionList' % compat.convert_to_bytes(user_id)
        body = {
            "name": name,
            "pageNo": page_no,
            "pageSize": page_size,
            "order": order
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body))

    @required(page_no=int, page_size=int, notifications=list, members=list)
    def update_action(self, user_id, name, notifications, members, alias, disable_times=None,
                      action_callbacks=None):
        """
        :param user_id:
        :type user_id: string
        :param name: action name
        :type name: string
        :param notifications:
        :type notifications: list of bcm_model.Notification
        :param members:
        :type members: list of bcm_model.Member
        :param alias: action's alias
        :type alias: string
        :param disable_times: disable time
        :type disable_times: list of bcm_model.DisableTime
        :param action_callbacks: list of action callback
        :type action_callbacks: list

        :return
        :rtype baidubce.bce_response.BceResponse
        """
        if disable_times is None:
            disable_times = []
        if action_callbacks is None:
            action_callbacks = []
        path = b'/userId/%s/action/update' % compat.convert_to_bytes(user_id)
        body = {
            "productName": user_id,
            "name": name,
            "notifications": notifications,
            "members": members,
            "alias": alias,
            "disableTimes": disable_times,
            "actionCallBacks": action_callbacks,
            "source": "USER"
        }
        return self._send_csm_request(http_methods.PUT, path, body=json.dumps(body))

    def log_extract(self, user_id, extract_rule, log_example):
        """

        :param user_id:
        :type user_id: string
        :param extract_rule: the log extract rule
        :type: string
        :param log_example: log example
        :type: string

        :return
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/userId/%s/application/logextract' % compat.convert_to_bytes(user_id)
        body = {
            "extractRule": extract_rule,
            "logExample": log_example
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body),
                                      body_parser=bcm_handler.parse_json_list)

    def query_metric_meta_for_application(self, user_id, app_name, task_name, metric_name, dimension_keys,
                                          instances=None):
        """

        :param user_id:
        :type user_id string
        :param app_name: application name
        :type app_name: string
        :param task_name: task name
        :type task_name: string
        :param metric_name:
        :type metric_name: string
        :param dimension_keys: multi dimension keys
        :type dimension_keys: list of string
        :param instances: multiple instance names
        :type instances: list of string

        :return
        :rtype baidubce.bce_response.BceResponse
        """

        path = (b'/userId/%s/application/%s/task/%s/metricMeta' % (compat.convert_to_bytes(user_id),
                                                                   compat.convert_to_bytes(app_name),
                                                                   compat.convert_to_bytes(task_name)))
        params = {b'metricName': metric_name, b'dimensionKeys': ",".join(dimension_keys)}
        print(params)
        if instances is not None and len(instances) > 0:
            params[b'instances'] = ",".join(instances)

        return self._send_csm_request(http_methods.GET, path, params=params)

    def query_metric_data_for_application(self, user_id, app_name, task_name, metric_name, start_time, end_time,
                                          instances=None, cycle=None, dimensions=None, statistics=None, aggr_data=None):
        """

        :param user_id:
        :type user_id: string
        :param app_name: application name
        :type app_name: string
        :param task_name: task name
        :type task_name: string
        :param metric_name: metric name
        :type metric_name: string
        :param start_time: start time, such as 2023-12-05T09:54:15Z
        :type start_time: string
        :param end_time: end time, such as 2023-12-05T09:54:15Z
        :type end_time: string
        :param instances: multiple instance names
        :type instances: list of string
        :param cycle: period time
        :type cycle: int
        :param dimensions: dimensions, such as ["httpMethod:POST___GET,path:apipath","httpMethod:POST,path:apipath1]
        :type dimensions: list of string
        :param statistics: statistics, enum: average, maximum, minimum, sum, sampleCount
        :type statistics: list of string
        :param aggr_data: is aggregation data
        :type aggr_data: bool

        :return
        :rtype baidubce.bce_response.BceResponse
        """
        path = (b'/userId/%s/application/%s/task/%s/metricData' % (compat.convert_to_bytes(user_id),
                                                                   compat.convert_to_bytes(app_name),
                                                                   compat.convert_to_bytes(task_name)))
        params = {b'startTime': start_time, b'endTime': end_time, b'metricName': metric_name}
        if statistics is not None and len(statistics) > 0:
            params[b'statistics'] = ",".join(statistics)
        if cycle is not None and cycle > 0:
            params[b'cycle'] = cycle
        if aggr_data is not None:
            params[b'aggrData'] = aggr_data
        if instances is not None and len(instances) > 0:
            params[b'instances'] = ",".join(instances)
        if dimensions is not None and len(dimensions) > 0:
            params[b'dimensions'] = ",".join(dimensions)

        return self._send_csm_request(http_methods.GET, path, params=params, body_parser=bcm_handler.parse_json_list)

    def list_alarm_metrics_for_application(self, user_id, app_name, task_name, search_name=None):
        """

        :param user_id:
        :type user_id: string
        :param app_name: application name
        :type app_name: string
        :param task_name: task name
        :type task_name: string
        :param search_name: metric name
        :type search_name: string

        :return
        :rtype baidubce.bce_response.BceResponse
        """
        path = (b'/userId/%s/application/%s/%s/alarm/metrics' % (compat.convert_to_bytes(user_id),
                                                                 compat.convert_to_bytes(app_name),
                                                                 compat.convert_to_bytes(task_name)))
        params = {}
        if search_name is None:
            params[b'searchName'] = search_name

        return self._send_csm_request(http_methods.GET, path, params=params, body_parser=bcm_handler.parse_json_list)

    def get_alarm_policy_for_application(self, user_id, alarm_name, app_name):
        """

        :param user_id:
        :type user_id: string
        :param app_name: application name
        :type app_name: string
        :param alarm_name: alarm name
        :type alarm_name: string

        :return
        :rtype baidubce.bce_response.BceResponse
        """
        path = (b'/userId/%s/application/alarm/%s/config' % (compat.convert_to_bytes(user_id),
                                                             compat.convert_to_bytes(alarm_name)))
        params = {b'appName': app_name}
        return self._send_csm_request(http_methods.GET, path, params=params)

    def delete_alarm_policy_for_application(self, user_id, alarm_name, app_name):
        """

        :param user_id:
        :type user_id: string
        :param app_name: application name
        :type app_name: string
        :param alarm_name: alarm name
        :type alarm_name: string

        :return
        :rtype baidubce.bce_response.BceResponse
        """
        path = (b'/userId/%s/application/alarm/config' % compat.convert_to_bytes(user_id))
        body = {
            'appName': app_name,
            "alarmName": alarm_name
        }
        return self._send_csm_request(http_methods.DELETE, path, body=json.dumps(body))

    @required(page_no=int, page_size=int)
    def list_alarm_policy_for_application(self, user_id, page_no, page_size=None, app_name=None, alarm_name=None,
                                          action_enabled=None, src_type=None, task_name=None):
        """

        :param user_id:
        :type user_id: string
        :param page_no: page number
        :type page_no: int
        :param app_name: application name
        :type app_name: string
        :param alarm_name: alarm name
        :type alarm_name: string
        :param action_enabled: is action enabled
        :type action_enabled: bool
        :param src_type: task type, enum: PROC,PORT,LOG,SCR
        :type src_type: string
        :param task_name: task name
        :type task_name: string
        :param page_size: page size
        :type page_size: int

        :return
        :rtype baidubce.bce_response.BceResponse
        """
        path = (b'/userId/%s/application/alarm/config/list' % compat.convert_to_bytes(user_id))
        params = {
            b'pageNo': page_no,
            b'pageSize': page_size,
            b'appName': app_name,
            b'alarmName': alarm_name,
            b'actionEnabled': action_enabled,
            b'srcType': src_type,
            b'taskName': task_name,
        }
        return self._send_csm_request(http_methods.GET, path, params=params)

    @required(rules=list)
    def create_alarm_policy_for_application(self, user_id, alarm_description, alarm_name, app_name,
                                            monitor_object_type, monitor_object, src_name, src_type, type, level,
                                            rules, action_enabled=True, incident_actions=None, resume_actions=None,
                                            insufficient_actions=None, insufficient_cycle=None, repeat_alarm_cycle=0,
                                            max_repeat_count=0):
        """
        :param user_id:
        :type user_id: string
        :param alarm_description: alarm policy comment
        :type alarm_description: string
        :param alarm_name: unique alarm name in user_id
        :type alarm_name: string
        :param app_name: application name
        :type app_name: string
        :param monitor_object_type: monitor object type, enum: APP, SERVICE
        :type monitor_object_type: string
        :param monitor_object: application monitor object
        :type monitor_object: bcm_model.ApplicationMonitorObject
        :param src_name: task name
        :type src_name: string
        :param src_type: task type, enum: PROC,PORT,LOG,SCR
        :type src_type: string
        :param type: alarm type
        :type type: string
        :param level: alarm level
        :type level: string
        :param rules: list of application alarm rules
        :type rules: list of ApplicationAlarmRule
        :param action_enabled: is alarm action enabled
        :type action_enabled: bool
        :param incident_actions: The action to be taken in the alarm state
        :type incident_actions: list of string
        :param resume_actions: The action to be taken in the alarm resume
        :type resume_actions: list of string
        :param insufficient_actions:
        :type insufficient_actions: list of string
        :param insufficient_cycle: insufficient cycle
        :type insufficient_cycle: int
        :param repeat_alarm_cycle: repeat alarm_cycle
        :type repeat_alarm_cycle: int
        :param max_repeat_count: max repeat count
        :type max_repeat_count: int

        :return
        :rtype baidubce.bce_response.BceResponse
        """
        path = (b'/userId/%s/application/alarm/config/create' % compat.convert_to_bytes(user_id))
        body = {
            "userId": user_id,
            "alarmDescription": alarm_description,
            "appName": app_name,
            "alarmName": alarm_name,
            "monitorObjectType": monitor_object_type,
            "monitorObject": monitor_object,
            "srcName": src_name,
            "srcType": src_type,
            "type": type,
            "level": level,
            "actionEnabled": action_enabled,
            "incidentActions": incident_actions,
            "resumeActions": resume_actions,
            "insufficientActions": insufficient_actions,
            "insufficientCycle": insufficient_cycle,
            "repeatAlarmCycle": repeat_alarm_cycle,
            "maxRepeatCount": max_repeat_count,
            "rules": rules
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body))

    @required(rules=list)
    def update_alarm_policy_for_application(self, user_id, alarm_description, alarm_name, app_name,
                                            monitor_object_type, monitor_object, src_name, src_type, type, level,
                                            rules, action_enabled=True, incident_actions=None, resume_actions=None,
                                            insufficient_actions=None, insufficient_cycle=None, repeat_alarm_cycle=0,
                                            max_repeat_count=0):
        """
        :param user_id:
        :type user_id: string
        :param alarm_description: alarm policy comment
        :type alarm_description: string
        :param alarm_name: unique alarm name in user_id
        :type alarm_name: string
        :param app_name: application name
        :type app_name: string
        :param monitor_object_type: monitor object type, enum: APP, SERVICE
        :type monitor_object_type: string
        :param monitor_object: application monitor object
        :type monitor_object: bcm_model.ApplicationMonitorObject
        :param src_name: task name
        :type src_name: string
        :param src_type: task type, enum: PROC,PORT,LOG,SCR
        :type src_type: string
        :param type: alarm type
        :type type: string
        :param level: alarm level
        :type level: string
        :param rules: list of application alarm rules
        :type rules: list of ApplicationAlarmRule
        :param action_enabled: is alarm action enabled
        :type action_enabled: bool
        :param incident_actions: The action to be taken in the alarm state
        :type incident_actions: list of string
        :param resume_actions: The action to be taken in the alarm resume
        :type resume_actions: list of string
        :param insufficient_actions:
        :type insufficient_actions: list of string
        :param insufficient_cycle: insufficient cycle
        :type insufficient_cycle: int
        :param repeat_alarm_cycle: repeat alarm_cycle
        :type repeat_alarm_cycle: int
        :param max_repeat_count: max repeat count
        :type max_repeat_count: int

        :return
        :rtype baidubce.bce_response.BceResponse
        """
        path = (b'/userId/%s/application/alarm/config/update' % compat.convert_to_bytes(user_id))
        body = {
            "userId": user_id,
            "alarmDescription": alarm_description,
            "appName": app_name,
            "alarmName": alarm_name,
            "monitorObjectType": monitor_object_type,
            "monitorObject": monitor_object,
            "srcName": src_name,
            "srcType": src_type,
            "type": type,
            "level": level,
            "actionEnabled": action_enabled,
            "incidentActions": incident_actions,
            "resumeActions": resume_actions,
            "insufficientActions": insufficient_actions,
            "insufficientCycle": insufficient_cycle,
            "repeatAlarmCycle": repeat_alarm_cycle,
            "maxRepeatCount": max_repeat_count,
            "rules": rules
        }
        return self._send_csm_request(http_methods.PUT, path, body=json.dumps(body))

    def create_dashboard(self, user_id=None, title=None, configure=None, dashboard_type=None, config=None):
        """
            Create a dashboard
            :param user_id:
                 Master account ID
            :type user_id: string

            :param title:
                Title of the dashboard
            :type title: string

            :param configure:
                Configure the dashboard
            :type configure:string

            :param dashboard_type:
                Dashboard type
            :type dashboard_type:string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        body = {
            "userId": user_id,
            "title": title,
            "configure": configure,
            "type": dashboard_type
        }
        user_id = compat.convert_to_bytes(user_id)
        path = b'/dashboard/products/%s/dashboards' % user_id
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def get_dashboard(self, user_id=None, dashboard_name=None, config=None):
        """
            Create a dashboard
            :param user_id:
                 Master account ID
            :type user_id: string

            :param dashboard_name:
                Dashboard name
            :type dashboard_name:string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(dashboard_name) <= 0:
            raise ValueError('dashboard_name should not be none or empty string')
        user_id = compat.convert_to_bytes(user_id)
        dashboard_name = compat.convert_to_bytes(dashboard_name)
        path = b'/dashboard/products/%s/dashboards/%s' % (user_id, dashboard_name)
        return self._send_csm_request(http_methods.GET, path, config=config)

    def update_dashboard(self, user_id=None, title=None, configure=None,
                         dashboard_type=None, dashboard_name=None, config=None):
        """
            Create a dashboard
            :param user_id:
                 Master account ID
            :type user_id: string

            :param title:
                Title of the dashboard
            :type title: string

            :param configure:
                Configure the dashboard
            :type configure:string

            :param dashboard_type:
                Dashboard type
            :type dashboard_type:string

            :param dashboard_name:
                Dashboard name
            :type dashboard_name:string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(dashboard_name) <= 0:
            raise ValueError('dashboard_name should not be none or empty string')
        body = {
            "userId": user_id,
            "title": title,
            "configure": configure,
            "type": dashboard_type
        }
        user_id = compat.convert_to_bytes(user_id)
        dashboard_name = compat.convert_to_bytes(dashboard_name)
        path = b'/dashboard/products/%s/dashboards/%s' % (user_id, dashboard_name)
        return self._send_csm_request(http_methods.PUT, path, body=json.dumps(body), config=config)

    def delete_dashboard(self, user_id=None, dashboard_name=None, config=None):
        """
            Create a dashboard
            :param user_id:
                 Master account ID
            :type user_id: string

            :param dashboard_name:
                Dashboard name
            :type dashboard_name:string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(dashboard_name) <= 0:
            raise ValueError('dashboard_name should not be none or empty string')
        user_id = compat.convert_to_bytes(user_id)
        dashboard_name = compat.convert_to_bytes(dashboard_name)
        path = b'/dashboard/products/%s/dashboards/%s' % (user_id, dashboard_name)
        return self._send_csm_request(http_methods.DELETE, path, config=config)

    def duplicate_dashboard(self, user_id=None, dashboard_name=None, config=None):
        """
            Create a dashboard
            :param user_id:
                 Master account ID
            :type user_id: string

            :param dashboard_name:
                Dashboard name
            :type dashboard_name:string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(dashboard_name) <= 0:
            raise ValueError('dashboard_name should not be none or empty string')
        body = {
        }
        user_id = compat.convert_to_bytes(user_id)
        dashboard_name = compat.convert_to_bytes(dashboard_name)
        path = b'/dashboard/products/%s/dashboards/%s/duplicate' % (user_id, dashboard_name)
        return self._send_csm_request(http_methods.POST, path, json.dumps(body), config=config)

    def create_dashboard_widget(self, user_id=None, dashboard_name=None, config=None):
        """
            Create a dashboard
            :param user_id:
                 Master account ID
            :type user_id: string

            :param dashboard_name:
                Dashboard name
            :type dashboard_name:string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(dashboard_name) <= 0:
            raise ValueError('dashboard_name should not be none or empty string')
        body = {
        }
        user_id = compat.convert_to_bytes(user_id)
        dashboard_name = compat.convert_to_bytes(dashboard_name)
        path = b'/dashboard/products/%s/dashboards/%s/widgets' % (user_id, dashboard_name)
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def get_dashboard_widget(self, user_id=None, dashboard_name=None, widget_name=None, config=None):
        """
            Create a dashboard
            :param user_id:
                 Master account ID
            :type user_id: string

            :param dashboard_name:
                Dashboard name
            :type dashboard_name:string

            :param widget_name:
                Widget name
            :type widget_name:string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(dashboard_name) <= 0:
            raise ValueError('dashboard_name should not be none or empty string')
        if len(widget_name) <= 0:
            raise ValueError('widget_name should be none or empty string')
        user_id = compat.convert_to_bytes(user_id)
        dashboard_name = compat.convert_to_bytes(dashboard_name)
        widget_name = compat.convert_to_bytes(widget_name)
        path = b'/dashboard/products/%s/dashboards/%s/widgets/%s' % (user_id, dashboard_name, widget_name)
        return self._send_csm_request(http_methods.GET, path, config=config)

    def delete_dashboard_widget(self, user_id=None, dashboard_name=None, widget_name=None, config=None):
        """
            Create a dashboard
            :param user_id:
                 Master account ID
            :type user_id: string

            :param dashboard_name:
                Dashboard name
            :type dashboard_name:string

            :param widget_name:
                Widget name
            :type widget_name:string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(dashboard_name) <= 0:
            raise ValueError('dashboard_name should not be none or empty string')
        if len(widget_name) <= 0:
            raise ValueError('widget_name should be none or empty string')
        user_id = compat.convert_to_bytes(user_id)
        dashboard_name = compat.convert_to_bytes(dashboard_name)
        widget_name = compat.convert_to_bytes(widget_name)
        path = b'/dashboard/products/%s/dashboards/%s/widgets/%s' % (user_id, dashboard_name, widget_name)
        return self._send_csm_request(http_methods.DELETE, path, config=config)

    def duplicate_dashboard_widget(self, user_id=None, dashboard_name=None, widget_name=None, config=None):
        """
            Create a dashboard
            :param user_id:
                 Master account ID
            :type user_id: string

            :param dashboard_name:
                Dashboard name
            :type dashboard_name:string

            :param widget_name:
                Widget name
            :type widget_name:string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(dashboard_name) <= 0:
            raise ValueError('dashboard_name should not be none or empty string')
        if len(widget_name) <= 0:
            raise ValueError('widget_name should be none or empty string')
        body = {
        }
        user_id = compat.convert_to_bytes(user_id)
        dashboard_name = compat.convert_to_bytes(dashboard_name)
        widget_name = compat.convert_to_bytes(widget_name)
        path = (b'/dashboard/products/%s/dashboards/%s/widgets/%s/duplicate' %
                (user_id, dashboard_name, widget_name))
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def update_dashboard_widget(self, user_id=None, dashboard_name=None, widget_name=None,
                                widget_type=None, title=None, configure=None, config=None):
        """
            Create a dashboard
            :param user_id:
                 Master account ID
            :type user_id: string

            :param dashboard_name:
                Dashboard name
            :type dashboard_name:string

            :param widget_name:
                Widget name
            :type widget_name:string

            :param widget_type:
                Widget type
            :type widget_type:string

            :param configure:
                Widget configure
            :type configure:object

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(dashboard_name) <= 0:
            raise ValueError('dashboard_name should not be none or empty string')
        if len(widget_name) <= 0:
            raise ValueError('widget_name should be none or empty string')
        body = {
            "title": title,
            "type": widget_type,
            "configure": configure
        }
        user_id = compat.convert_to_bytes(user_id)
        dashboard_name = compat.convert_to_bytes(dashboard_name)
        widget_name = compat.convert_to_bytes(widget_name)
        path = b'/dashboard/products/%s/dashboards/%s/widgets/%s' % (user_id, dashboard_name, widget_name)
        return self._send_csm_request(http_methods.PUT, path, body=json.dumps(body), config=config)

    def get_dashboard_report_data(self, data=None, time=None, config=None):
        """
            Get dashboard report data
            :param data:
                Query data
            :type data: object

            :param time:
                Query data time
            :type time: string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        body = {
            "data": data,
            "time": time
        }
        path = b'/dashboard/metric/report'
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def get_dashboard_trend_data(self, data=None, time=None, config=None):
        """
            Get dashboard report data
            :param data:
                Query data
            :type data: object

            :param time:
                Query data time
            :type time: string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        body = {
            "data": data,
            "time": time
        }
        path = b'/dashboard/metric/trend'
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def get_dashboard_gauge_chart_data(self, data=None, time=None, config=None):
        """
            Get dashboard report data
            :param data:
                Query data
            :type data: object

            :param time:
                Query data time
            :type time: string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        body = {
            "data": data,
            "time": time
        }
        path = b'/dashboard/metric/gaugechart'
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def get_dashboard_billboard_data(self, data=None, time=None, config=None):
        """
            Get dashboard report data
            :param data:
                Query data
            :type data: object

            :param time:
                Query data time
            :type time: string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        body = {
            "data": data,
            "time": time
        }
        path = b'/dashboard/metric/billboard'
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def get_dashboard_trend_senior_data(self, data=None, time=None, config=None):
        """
            Get dashboard report data
            :param data:
                Query data
            :type data: object

            :param time:
                Query data time
            :type time: string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        body = {
            "data": data,
            "time": time
        }
        path = b'/dashboard/metric/trend/senior'
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def get_dashboard_dimensions(self, user_id, metric_name, region, service, show_id,
                                 dimensions=None, config=None):
        """
            Get dashboard dimensions
            :param user_id:
                 Master account ID
            :type user_id: string

            :param dimensions:
                dashboard dimensions
            :type dimensions: string

            :param metric_name:
                dashboard metric_name
            :type metric_name: string

            :param region:
                dashboard dimensions region
            :type region: string

            :param service:
                cloud service
            :type service:

            :param show_id:
                cloud resourceId
            :type show_id:

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(metric_name) <= 0:
            raise ValueError('metric_name should not be none or empty string')
        if len(region) <= 0:
            raise ValueError('region should not be none or empty string')
        if len(service) <= 0:
            raise ValueError('service should not be none or empty string')
        if len(show_id) <= 0:
            raise ValueError('show_id should not be none or empty string')
        params = {
            b'dimensions': dimensions,
            b'userId': user_id,
            b'metricName': metric_name,
            b'region': region,
            b'service': service,
            b'showId': show_id,
        }
        user_id = compat.convert_to_bytes(user_id)
        service = compat.convert_to_bytes(service)
        region = compat.convert_to_bytes(region)
        path = b'/userId/%s/services/%s/region/%s/metric/dimensions' % (user_id, service, region)
        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def create_application_data(self, name, type, user_id, alias=None, description=None, config=None):
        """
        create application data
        :param name:
        :param type:
        :param user_id:
        :param alias:
        :param description:
        :param config:
        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(type) <= 0:
            raise ValueError("type should not be null")
        if len(name) <= 0:
            raise ValueError("name should not be null")
        req = {
            "name": name,
            "type": type,
            "userId": user_id,
        }
        if alias is not None:
            req["alias"] = alias
        if description is not None:
            req["description"] = description
        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/application' % user_id
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(req), config=config)

    def get_application_data_list(self, user_id, page_no=None, page_size=None, search_name=None, config=None):
        """
        get_application_data_list
        :param user_id:
        :param page_no:
        :param page_size:
        :param search_name:
        :param config:
        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if page_no is None:
            page_no = 1
        if page_size is None:
            page_size = 10
        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/application' % user_id
        params = {
            b'pageSize': page_size,
            b'pageNo': page_no,
        }
        if search_name is not None:
            params[b'searchName'] = search_name
        return self._send_request(http_methods.GET, path, params=params, config=config)

    def update_application_data(self, user_id, id, name, type, alias=None, description=None, config=None):
        """
        update_application_data
        :param user_id:
        :param id:
        :param name:
        :param type:
        :param alias:
        :param description:
        :param config:
        :return:
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(type) <= 0:
            raise ValueError("type should not be null")
        if len(name) <= 0:
            raise ValueError("name should not be null")
        if len(id) <= 0:
            raise ValueError("id should not be null")
        req = {
            "userId": user_id,
            "id": id,
            "name": name,
            "type": type
        }
        if alias is not None:
            req["alias"] = alias
        if description is not None:
            req["description"] = description
        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/application' % user_id
        return self._send_csm_request(http_methods.PUT, path, body=json.dumps(req), config=config)

    def delete_application_data(self, user_id, name, config=None):
        """
        delete_application_data
        :param user_id:
        :param name:
        :param config:
        :return:
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(name) <= 0:
            raise ValueError("name should null be null")
        req = {
            "name": name
        }
        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/application' % user_id
        return self._send_csm_request(http_methods.DELETE, path, body=json.dumps(req), config=config)

    def get_application_instance_list(self, user_id, region, app_name, search_name, page_no=None, page_size=None,
                                      search_value=None, config=None):
        """
        get_application_instance_list
        :param user_id:
        :param region:
        :param app_name:
        :param search_name:
        :param page_no:
        :param page_size:
        :param search_value:
        :param config:
        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(region) <= 0:
            raise ValueError("region should not be null")
        if len(app_name) <= 0:
            raise ValueError("app_name should not be null")
        if page_no is None:
            page_no = 1
        if page_size is None:
            page_size = 10
        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/instances/all' % user_id
        req = {
            "appName": app_name,
            "region": region,
            "pageNo": page_no,
            "pageSize": page_size,
            "searchName": search_name
        }
        if search_value is not None:
            req["searchValue"] = search_value
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(req), config=config)

    @required(user_id=value_type,
              app_name=value_type,
              host_list=list)
    def create_application_instance(self, user_id, app_name, host_list, config=None):
        """
        create_application_instance
        :param user_id:
        :param app_name:
        :param host_list:
        :param config:
        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(app_name) <= 0:
            raise ValueError("app_name should not be null")
        if len(host_list) <= 0:
            raise ValueError("host_list should not be null")
        host_list_json = []
        for host in host_list:
            host_list_json.append(host)
        req = {
            "appName": app_name,
            "userId": user_id,
            "hostList": host_list_json
        }
        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/application/instance/bind' % user_id
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(req), config=config)

    def get_application_instance_created_list(self, user_id, app_name, region=None, config=None):
        """
        get_application_instance_created_list
        :param user_id:
        :param app_name:
        :param region:
        :param config:
        :return:
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(app_name) <= 0:
            raise ValueError("app_name should not be null")
        user_id = compat.convert_to_bytes(user_id)
        app_name = compat.convert_to_bytes(app_name)
        path = b'/userId/%s/application/%s/instance/list' % (user_id, app_name)
        params = None
        if region is not None:
            params = {
                'region': region
            }
        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def delete_application_instance(self, user_id, app_name, id, config=None):
        """
        delete_application_instance
        :param user_id:
        :param app_name:
        :param id:
        :param config:
        :return:
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(app_name) <= 0:
            raise ValueError("app_name should not be null")
        if len(id) <= 0:
            raise ValueError("id should not be null")
        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/application/instance' % user_id
        req = {
            "id": id,
            "appName": app_name
        }
        return self._send_csm_request(http_methods.DELETE, path, body=json.dumps(req), config=config)

    @required(user_id=value_type, app_name=value_type, alias_name=value_type, type=int,
              target=value_type, cycle=int, description=value_type, log_example=value_type,
              match_rule=value_type, rate=int, extract_result=list, metrics=list)
    def create_application_instance_task(self, user_id, app_name, alias_name, type, target,
                                         cycle=None, description=None, log_example=None, match_rule=None, rate=None,
                                         extract_result=None, metrics=None, config=None):
        """
        create_application_instance_task
        :param user_id:
        :param app_name:
        :param alias_name:
        :param type:
        :param target:
        :param cycle:
        :param description:
        :param log_example:
        :param match_rule:
        :param rate:
        :param extract_result:
        :param metrics:
        :param config:
        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(app_name) <= 0:
            raise ValueError("app_name should not be null")
        if type is None:
            raise ValueError("type should not be null")
        if len(alias_name) <= 0:
            raise ValueError("alias_name should not be null")
        if len(target) <= 0:
            raise ValueError("target should not be null")
        if cycle is None:
            cycle = 60
        req = {
            "appName": app_name,
            "type": str(type),
            "aliasName": alias_name,
            "target": target,
            "cycle": str(cycle)
        }
        if description is not None:
            req["description"] = description
        if str(type) == "2":
            if log_example is None:
                raise ValueError("log_example should not be null")
            if match_rule is None:
                raise ValueError("match_rule should not be null")
            if rate is None:
                raise ValueError("rate should not be null")
            if extract_result is None:
                raise ValueError("extract_result should not be null")
            if metrics is None:
                raise ValueError("metrics should not be null")
            req["logExample"] = log_example
            req["matchRule"] = match_rule
            req["rate"] = rate

            extract_result_json = []
            for result in extract_result:
                extract_result_json.append(result)
            req["extractResult"] = extract_result_json

            metrics_json = []
            for metric in metrics:
                metrics_json.append(metric)
            req["metrics"] = metrics_json
        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/application/task/create' % user_id
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(req), config=config)

    def get_application_monitor_task_detail(self, user_id, app_name, task_name, config=None):
        """
        get_application_monitor_task_detail
        :param user_id:
        :param app_name:
        :param task_name:
        :param config:
        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(app_name) <= 0:
            raise ValueError("app_name should not be null")
        if len(task_name) <= 0:
            raise ValueError("task_name should not be null")
        user_id = compat.convert_to_bytes(user_id)
        app_name = compat.convert_to_bytes(app_name)
        task_name = compat.convert_to_bytes(task_name)
        path = b'/userId/%s/application/%s/task/%s' % (user_id, app_name, task_name)
        return self._send_csm_request(http_methods.GET, path, config=config)

    def get_application_monitor_task_list(self, user_id, app_name, type=None, config=None):
        """
        get_application_monitor_task_list
        :param user_id:
        :param app_name:
        :param type:
        :param config:
        :return:
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(app_name) <= 0:
            raise ValueError("app_name should not be null")
        user_id = compat.convert_to_bytes(user_id)
        app_name = compat.convert_to_bytes(app_name)
        path = b'/userId/%s/application/%s/task/list' % (user_id, app_name)
        params = None
        if type is not None:
            params = {
                'type': type
            }
        return self._send_csm_request(http_methods.GET, path, params=params, config=config,
                                      body_parser=bcm_handler.parse_json_list)

    @required(user_id=value_type, app_name=value_type, name=value_type, alias_name=value_type, type=int,
              target=value_type, cycle=int, description=value_type, log_example=value_type,
              match_rule=value_type, rate=int, extract_result=list, metrics=list)
    def update_application_monitor_task(self, user_id, app_name, alias_name, name, type, target,
                                        cycle=None, description=None, log_example=None, match_rule=None, rate=None,
                                        extract_result=None, metrics=None, config=None):
        """
        update application monitor task
        :param user_id:
        :param app_name:
        :param alias_name:
        :param name:
        :param type:
        :param target:
        :param cycle:
        :param description:
        :param log_example:
        :param match_rule:
        :param rate:
        :param extract_result:
        :param metrics:
        :param config:
        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(app_name) <= 0:
            raise ValueError("app_name should not be null")
        if len(name) <= 0:
            raise ValueError("name should not be null")
        if type is None:
            raise ValueError("type should not be null")
        if len(alias_name) <= 0:
            raise ValueError("alias_name should not be null")
        if len(target) <= 0:
            raise ValueError("target should not be null")
        req = {
            "appName": app_name,
            "name": name,
            "type": str(type),
            "aliasName": alias_name,
            "target": target,
        }
        if cycle is not None:
            req["cycle"] = cycle
        if description is not None:
            req["description"] = description
        if str(type) == "2":
            if log_example is None:
                raise ValueError("log_example should not be null")
            if match_rule is None:
                raise ValueError("match_rule should not be null")
            if rate is None:
                raise ValueError("rate should not be null")
            if extract_result is None:
                raise ValueError("extract_result should not be null")
            if metrics is None:
                raise ValueError("metrics should not be null")
            req["logExample"] = log_example
            req["matchRule"] = match_rule
            req["rate"] = rate

            extract_result_json = []
            for result in extract_result:
                extract_result_json.append(result)
            req["extractResult"] = extract_result_json

            metrics_json = []
            for metric in metrics:
                metrics_json.append(metric)
            req["metrics"] = metrics_json
        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/application/task/update' % user_id
        return self._send_csm_request(http_methods.PUT, path, body=json.dumps(req), config=config)

    def delete_application_monitor_task(self, user_id, name, app_name, config=None):
        """
        delete_application_monitor_task
        :param user_id:
        :param name:
        :param app_name:
        :param config:
        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(app_name) <= 0:
            raise ValueError("app_name should not be null")
        if len(name) <= 0:
            raise ValueError("name should not be null")
        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/application/task/delete' % user_id
        req = {
            "name": name,
            "appName": app_name
        }
        return self._send_csm_request(http_methods.DELETE, path, body=json.dumps(req), config=config)

    def create_application_dimension_table(self, user_id, app_name, table_name, map_content_json, config=None):
        """
        create_application_dimension_table
        :param user_id:
        :param app_name:
        :param table_name:
        :param map_content_json:
        :param config:
        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(app_name) <= 0:
            raise ValueError("app_name should not be null")
        if len(table_name) <= 0:
            raise ValueError("table_name should not be null")
        if len(map_content_json) <= 0:
            raise ValueError("map_content_json should not be null")
        req = {
            "userId": user_id,
            "appName": app_name,
            "tableName": table_name,
            "mapContentJson": map_content_json
        }
        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/application/dimensionMap/create' % user_id
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(req), config=config)

    def get_application_dimension_table_list(self, user_id, app_name, search_name=None, config=None):
        """
        get_application_dimension_table_list
        :param user_id:
        :param app_name:
        :param search_name:
        :param config:
        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(app_name) <= 0:
            raise ValueError("app_name should not be null")
        user_id = compat.convert_to_bytes(user_id)
        app_name = compat.convert_to_bytes(app_name)
        path = b'/userId/%s/application/%s/dimensionMap/list' % (user_id, app_name)
        params = None
        if search_name is not None:
            params = {
                'searchName': search_name
            }
        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def update_application_dimension_table(self, user_id, app_name, table_name, map_content_json, config=None):
        """
        update_application_dimension_table
        :param user_id:
        :param app_name:
        :param table_name:
        :param map_content_json:
        :param config:
        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(app_name) <= 0:
            raise ValueError("app_name should not be null")
        if len(table_name) <= 0:
            raise ValueError("table_name should not be null")
        if len(map_content_json) <= 0:
            raise ValueError("map_content_json should not be null")
        req = {
            "userId": user_id,
            "appName": app_name,
            "tableName": table_name,
            "mapContentJson": map_content_json
        }
        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/application/dimensionMap/update' % user_id
        return self._send_csm_request(http_methods.PUT, path, body=json.dumps(req), config=config)

    def delete_application_dimension_table(self, user_id, app_name, table_name, config=None):
        """
        delete_application_dimension_table
        :param user_id:
        :param app_name:
        :param table_name:
        :param config:
        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(app_name) <= 0:
            raise ValueError("app_name should not be null")
        if len(table_name) <= 0:
            raise ValueError("table_name should not be null")
        req = {
            "userId": user_id,
            "appName": app_name,
            "tableName": table_name
        }
        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/application/dimensionMap/delete' % user_id
        return self._send_csm_request(http_methods.DELETE, path, body=json.dumps(req), config=config)

    @required(page_no=int, page_size=int, account_id=str, start_time=str, end_time=str)
    def get_cloud_event_data(self, page_no=1, page_size=10, start_time=None, end_time=None, account_id=None,
                             ascending=None, scope=None, region=None, event_level=None, event_name=None,
                             event_alias=None, resource_type=None, resource_id=None, event_id=None):
        """
        :param page_no: page number
        :type page_no: int
        :param page_size: page size
        :type page_size: int
        :param start_time: start time, such as 2023-12-05T09:54:15Z
        :type start_time: string
        :param end_time: end time, such as 2023-12-05T09:54:15Z
        :type end_time: string
        :param account_id: account id
        :type account_id: string
        :param ascending: ascending
        :type ascending: bool
        :param scope: scope
        :type scope: string
        :param region: region
        :type region: string
        :param event_level: event level
        :type event_level: None or ENUM {'NOTICE', 'WARNING', 'MAJOR', 'CRITICAL'}
        :param event_name: event name
        :type event_name: string
        :param event_alias: event alias
        :type event_alias: string
        :param resource_type: resource type
        :type resource_type: string
        :param resource_id: resource id
        :type resource_id: string
        :param event_id: event id
        :type event_id: string

        :return
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/bce-event/list'
        params = {
            b'pageNo': page_no,
            b'pageSize': page_size,
            b'startTime': start_time,
            b'endTime': end_time,
            b'accountId': account_id,
            b'ascending': ascending,
            b'scope': scope,
            b'region': region,
            b'eventLevel': event_level,
            b'eventName': event_name,
            b'eventAlias': event_alias,
            b'resourceType': resource_type,
            b'resourceId': resource_id,
            b'eventId': event_id,
        }
        return self._send_event_request(http_methods.GET, path, params=params)

    @required(page_no=int, page_size=int, account_id=str, start_time=str, end_time=str)
    def get_platform_event_data(self, page_no=1, page_size=10, start_time=None, end_time=None, account_id=None,
                                ascending=None, scope=None, region=None, event_level=None, event_name=None,
                                event_alias=None, event_id=None):
        """
        :param page_no: page number
        :type page_no: int
        :param page_size: page size
        :type page_size: int
        :param start_time: start time, such as 2023-12-05T09:54:15Z
        :type start_time: string
        :param end_time: end time, such as 2023-12-05T09:54:15Z
        :type end_time: string
        :param account_id: account id
        :type account_id: string
        :param ascending: ascending
        :type ascending: bool
        :param scope: scope
        :type scope: string
        :param region: region
        :type region: string
        :param event_level: event level
        :type event_level: None or ENUM {'NOTICE', 'WARNING', 'MAJOR', 'CRITICAL'}
        :param event_name: event name
        :type event_name: string
        :param event_alias: event alias
        :type event_alias: string
        :param event_id: event id
        :type event_id: string

        :return
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/platform-event/list'
        params = {
            b'pageNo': page_no,
            b'pageSize': page_size,
            b'startTime': start_time,
            b'endTime': end_time,
            b'accountId': account_id,
            b'ascending': ascending,
            b'scope': scope,
            b'region': region,
            b'eventLevel': event_level,
            b'eventName': event_name,
            b'eventAlias': event_alias,
            b'eventId': event_id,
        }
        return self._send_event_request(http_methods.GET, path, params=params)

    @required(account_id=str, service_name=str, name=str, block_status=str, incident_actions=list)
    def create_event_policy(self, account_id, service_name, name, block_status, event_filter,
                            resource, incident_actions):
        """
        :param account_id: account id
        :type account_id: string
        :param service_name: service name
        :type service_name: string
        :param name: event policy name
        :type name: string
        :param block_status: block status, enum: NORMAL, BLOCKED
        :type block_status: string
        :param event_filter: event filter
        :type event_filter: EventFilter
        :param resource: resource filter
        :type resource: EventResourceFilter
        :param incident_actions: incident actions
        :type incident_actions: list of string
        """
        if event_filter is None:
            raise ValueError('event_filter should not be none')
        if resource is None:
            raise ValueError('resource should not be none')

        path = b'/accounts/%s/services/%s/alarm-policies' % (compat.convert_to_bytes(account_id),
                                                             compat.convert_to_bytes(service_name))
        body = {
            "account_id": account_id,
            "service_name": service_name,
            "name": name,
            "blockStatus": block_status,
            "eventFilter": event_filter,
            "resource": resource,
            "incidentActions": incident_actions
        }
        return self._send_event_request(http_methods.POST, path, body=json.dumps(body))

    @required(user_id=str, region=str, service_name=str, type_name=str, name=str)
    def create_instance_group(self, user_id, region, service_name, type_name, name, resource_id_list):
        """
        :param user_id: user id
        :type user_id: string
        :param region: region
        :type region: string
        :param service_name: service name
        :type service_name: string
        :param type_name: type name
        :type type_name: string
        :param name: instance group name
        :type name: string
        :param resource_id_list: resource id list
        :type resource_id_list: list of MonitorResource
        """
        path = b'/userId/%s/instance-group' % compat.convert_to_bytes(user_id)
        body = {
            "userId": user_id,
            "region": region,
            "serviceName": service_name,
            "typeName": type_name,
            "name": name,
            "resourceIdList": resource_id_list
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body))

    @required(user_id=str, ig_id=str, region=str, service_name=str, type_name=str, name=str)
    def update_instance_group(self, ig_id, user_id, region, service_name, type_name, name):
        """
        :param ig_id: instance group id
        :type ig_id: string
        :param user_id: user id
        :type user_id: string
        :param region: region
        :type region: string
        :param service_name: service name
        :type service_name: string
        :param type_name: type name
        :type type_name: string
        :param name: instance group name
        :type name: string
        """
        path = b'/userId/%s/instance-group' % compat.convert_to_bytes(user_id)
        body = {
            "id": ig_id,
            "userId": user_id,
            "region": region,
            "serviceName": service_name,
            "typeName": type_name,
            "name": name,
        }
        return self._send_csm_request(http_methods.PATCH, path, body=json.dumps(body))

    @required(user_id=str, ig_id=str)
    def delete_instance_group(self, user_id, ig_id):
        """
        :param user_id: user id
        :type user_id: string
        :param ig_id: instance group id
        :type ig_id: string
        """
        path = b'/userId/%s/instance-group/%s' % (compat.convert_to_bytes(user_id), compat.convert_to_bytes(ig_id))
        return self._send_csm_request(http_methods.DELETE, path)

    @required(user_id=str, ig_id=str)
    def get_instance_group(self, user_id, ig_id):
        """
        :param user_id: user id
        :type user_id: string
        :param ig_id: instance group id
        :type ig_id: string
        """
        path = b'/userId/%s/instance-group/%s' % (compat.convert_to_bytes(user_id), compat.convert_to_bytes(ig_id))
        return self._send_csm_request(http_methods.GET, path)

    @required(user_id=str, page_no=int, page_size=int)
    def list_instance_group(self, user_id, name, service_name, region, type_name, page_no, page_size):
        """
        :param user_id: user id
        :type user_id: string
        :param name: instance group name
        :type name: string
        :param service_name: service name
        :type service_name: string
        :param region: region
        :type region: string
        :param type_name: type name
        :type type_name: string
        :param page_no: page number
        :type page_no: int
        :param page_size: page size
        :type page_size: int
        """
        path = b'/userId/%s/instance-group/list' % compat.convert_to_bytes(user_id)
        params = {
            b"userId": user_id,
            b"name": name,
            b"serviceName": service_name,
            b"region": region,
            b"typeName": type_name,
            b"pageNo": page_no,
            b"pageSize": page_size
        }
        return self._send_csm_request(http_methods.GET, path, params=params)

    @required(user_id=str, ig_id=str, resource_id_list=list)
    def add_ig_instance(self, ig_id, user_id, resource_id_list):
        """
        :param ig_id: instance group id
        :type ig_id: string
        :param user_id: user id
        :type user_id: string
        :param resource_id_list: resource id list
        :type resource_id_list: list of MonitorResource
        """
        path = b'/userId/%s/instance-group/%s/instance/add' % (compat.convert_to_bytes(user_id),
                                                               compat.convert_to_bytes(ig_id))
        body = {
            "id": ig_id,
            "userId": user_id,
            "resourceIdList": resource_id_list
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body))

    @required(user_id=str, ig_id=str, resource_id_list=list)
    def remove_ig_instance(self, ig_id, user_id, resource_id_list):
        """
        :param ig_id: instance group id
        :type ig_id: string
        :param user_id: user id
        :type user_id: string
        :param resource_id_list: resource id list
        :type resource_id_list: list of MonitorResource
        """
        path = b'/userId/%s/instance-group/%s/instance/remove' % (compat.convert_to_bytes(user_id),
                                                                  compat.convert_to_bytes(ig_id))
        body = {
            "id": ig_id,
            "userId": user_id,
            "resourceIdList": resource_id_list
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body))

    @required(user_id=str, ig_id=str, service_name=str, type_name=str, region=str, view_type=str,
              page_no=int, page_size=int)
    def list_ig_instance(self, user_id, ig_id, service_name, type_name, region, view_type, page_no, page_size):
        """
        :param user_id: user id
        :type user_id: string
        :param ig_id: instance group id
        :type ig_id: string
        :param service_name: service name
        :type service_name: string
        :param type_name: type name
        :type type_name: string
        :param region: region
        :type region: string
        :param view_type: view type, enum: LIST_VIEW, DETAIL_VIEW
        :type view_type: string
        :param page_no: page number
        :type page_no: int
        :param page_size: page size
        :type page_size: int
        """
        path = b'/userId/%s/instance-group/instance/list' % compat.convert_to_bytes(user_id)
        params = {
            b"id": ig_id,
            b"userId": user_id,
            b"serviceName": service_name,
            b"typeName": type_name,
            b"region": region,
            b"viewType": view_type,
            b"pageNo": page_no,
            b"pageSize": page_size
        }
        return self._send_csm_request(http_methods.GET, path, params=params)

    @required(user_id=str, service_name=str, type_name=str, region=str, view_type=str, keyword_type=str, keyword=str,
              page_no=int, page_size=int)
    def list_all_instance(self, user_id, service_name, type_name, region, view_type, keyword_type, keyword,
                          page_no, page_size):
        """
        :param user_id: user id
        :type user_id: string
        :param service_name: service name
        :type service_name: string
        :param type_name: type name
        :type type_name: string
        :param region: region
        :type region: string
        :param view_type: view type, enum: LIST_VIEW, DETAIL_VIEW
        :type view_type: string
        :param keyword_type: keyword type, enum: name, id
        :type keyword_type: string
        :param keyword: keyword
        :type keyword: string
        :param page_no: page number
        :type page_no: int
        :param page_size: page size
        :type page_size: int
        """
        path = b'/userId/%s/instance/list' % compat.convert_to_bytes(user_id)
        params = {
            b"userId": user_id,
            b"serviceName": service_name,
            b"typeName": type_name,
            b"region": region,
            b"viewType": view_type,
            b"keywordType": keyword_type,
            b"keyword": keyword,
            b"pageNo": page_no,
            b"pageSize": page_size
        }
        return self._send_csm_request(http_methods.GET, path, params=params)

    @required(user_id=str, ig_id=str, ig_uuid=str, service_name=str, type_name=str, region=str, view_type=str,
              keyword_type=str, keyword=str, page_no=int, page_size=int)
    def list_filter_instance(self, user_id, ig_id, ig_uuid, service_name, type_name, region, view_type,
                             keyword_type, keyword, page_no, page_size):
        """
        :param user_id: user id
        :type user_id: string
        :param ig_id: instance group id
        :type ig_id: string
        :param ig_uuid: instance group uuid
        :type ig_uuid: string
        :param service_name: service name
        :type service_name: string
        :param type_name: type name
        :type type_name: string
        :param region: region
        :type region: string
        :param view_type: view type, enum: LIST_VIEW, DETAIL_VIEW
        :type view_type: string
        :param keyword_type: keyword type, enum: name, id
        :type keyword_type: string
        :param keyword: keyword
        :type keyword: string
        :param page_no: page number
        :type page_no: int
        :param page_size: page size
        :type page_size: int
        """
        path = b'/userId/%s/instance/filteredList' % compat.convert_to_bytes(user_id)
        params = {
            b"userId": user_id,
            b"id": ig_id,
            b"uuid": ig_uuid,
            b"serviceName": service_name,
            b"typeName": type_name,
            b"region": region,
            b"viewType": view_type,
            b"keywordType": keyword_type,
            b"keyword": keyword,
            b"pageNo": page_no,
            b"pageSize": page_size
        }
        return self._send_csm_request(http_methods.GET, path, params=params)

    def push_metric_data(self, user_id=None, scope=None, metric_data=None, config=None):

        """
        :param user_id: user_id
        :type user_id: string
        :param scope: scope
        :type scope: string
        :param metric_data: metric_data
        :type bcm_model.MetricDatum array
        :return:
        """
        user_id = compat.convert_to_bytes(user_id)
        scope = compat.convert_to_bytes(scope)
        path = b'/metricdata/%s/%s' % (user_id, scope)
        body = {
            "metricData": metric_data
        }

        return self._send_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def get_custom_metric_data(self, user_id=None, namespaces=None, metric_name=None,
                               dimensions=None, statistics=None, start_time=None,
                               end_time=None, cycle=None, config=None):
        """
        Return metric data of product instances owned by the authenticated user.

        This site may help you: https://cloud.baidu.com/doc/BCM/s/9jwvym3kb

        :param user_id:
            Master account ID
        :type user_id: string

        :param namespaces:
            Cloud product namespace, eg: BCE_BCC.
        :type namespaces: string

        :param metric_name:
            The metric name of baidu cloud monitor, eg: CpuIdlePercent.
        :type metric_name: string

        :param dimensions:
            Consists of dimensionName: dimensionValue.
            Use semicolons when items have multiple dimensions,
            such as dimensionName: dimensionValue; dimensionName: dimensionValue.
            Only one dimension value can be specified for the same dimension.
            eg: InstanceId:fakeid-2222
        :type dimensions: string

        :param statistics:
            According to the format of statistics1,statistics2,statistics3,
            the optional values are `average`, `maximum`, `minimum`, `sum`, `sampleCount`
        :type statistics: string

        :param start_time:
            Query start time.
            Please refer to the date and time, UTC date indication
        :type start_time: string

        :param end_time:
            Query end time.
            Please refer to the date and time, UTC date indication
        :type end_time: string

        :param cycle:
            Statistical period.
            Multiples of 60 in seconds (s).
        :type cycle: int

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        user_id = compat.convert_to_bytes(user_id)
        namespaces = compat.convert_to_bytes(namespaces)
        metric_name = compat.convert_to_bytes(metric_name)
        path = b'/userId/%s/custom/namespaces/%s/metrics/%s/data' % (user_id, namespaces, metric_name)

        body = {
            "statistics": statistics,
            "dimensions": dimensions,
            "startTime": start_time,
            "endTime": end_time,
            "cycle": cycle
        }

        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body),
                                      body_parser=bcm_handler.parse_json_list, config=config)

    def push_custom_metric_data(self, user_id=None, namespace=None, metric_name=None,
                                dimensions=None, value=None,
                                timestamp=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param namespace:
        :type namespace: string
        :param metric_name:
        :type metric_name: string
        :param dimensions:
        :type dimensions: bcm_model.Dimension array
        :param value:
        :type value: double
        :param timestamp:
        :type timestamp: string
        :param config:
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        namespace = compat.convert_to_bytes(namespace)
        path = b'/userId/%s/custom/data' % (user_id)
        body = {
            "namespace": namespace,
            "metricName": metric_name,
            "dimensions": dimensions,
            "value": value,
            "timestamp": timestamp
        }

        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def create_site_http_task_config(self, user_id=None, task_name=None, address=None,
                                     method=None, post_content=None,
                                     advance_config=None, cycle=None, idc=None, timeout=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_name:
        :type task_name: string
        :param address:
        :type address: string
        :param method:
        :type method: string
        :param post_content:
        :type post_content: string
        :param advance_config:
        :type advance_config: bool
        :param cycle:
        :type cycle: int
        :param idc:
        :type idc: string
        :param timeout:
        :type timeout: int
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/http/create' % (user_id)
        body = {
            "userId": user_id,
            "taskName": task_name,
            "address": address,
            "method": method,
            "postContent": post_content,
            "advanceConfig": advance_config,
            "cycle": cycle,
            "idc": idc,
            "timeout": timeout,
        }

        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def update_site_http_task_config(self, user_id=None, task_id=None, task_name=None, address=None,
                                     method=None, post_content=None,
                                     advance_config=None, cycle=None, idc=None, timeout=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param task_name:
        :type task_name: string
        :param address:
        :type address: string
        :param method:
        :type method: string
        :param post_content:
        :type post_content: string
        :param advance_config:
        :type advance_config: bool
        :param cycle:
        :type cycle: int
        :param idc:
        :type idc: string
        :param timeout:
        :type timeout: int
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/http/update' % (user_id)
        body = {
            "userId": user_id,
            "taskId": task_id,
            "taskName": task_name,
            "address": address,
            "method": method,
            "postContent": post_content,
            "advanceConfig": advance_config,
            "cycle": cycle,
            "idc": idc,
            "timeout": timeout,
        }

        return self._send_csm_request(http_methods.PUT, path, body=json.dumps(body), config=config)

    def get_site_http_task_config(self, user_id=None, task_id=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/http/detail' % (user_id)
        params = {}

        if task_id is not None:
            params["taskId"] = task_id

        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def create_site_https_task_config(self, user_id=None, task_name=None, address=None,
                                      method=None, post_content=None,
                                      advance_config=None, cycle=None, idc=None, timeout=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_name:
        :type task_name: string
        :param address:
        :type address: string
        :param method:
        :type method: string
        :param post_content:
        :type post_content: string
        :param advance_config:
        :type advance_config: bool
        :param cycle:
        :type cycle: int
        :param idc:
        :type idc: string
        :param timeout:
        :type timeout: int
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/https/create' % (user_id)
        body = {
            "userId": user_id,
            "taskName": task_name,
            "address": address,
            "method": method,
            "postContent": post_content,
            "advanceConfig": advance_config,
            "cycle": cycle,
            "idc": idc,
            "timeout": timeout,
        }

        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def update_site_https_task_config(self, user_id=None, task_id=None, task_name=None, address=None,
                                      method=None, post_content=None,
                                      advance_config=None, cycle=None, idc=None, timeout=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param task_name:
        :type task_name: string
        :param address:
        :type address: string
        :param method:
        :type method: string
        :param post_content:
        :type post_content: string
        :param advance_config:
        :type advance_config: bool
        :param cycle:
        :type cycle: int
        :param idc:
        :type idc: string
        :param timeout:
        :type timeout: int
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/https/update' % (user_id)
        body = {
            "userId": user_id,
            "taskId": task_id,
            "taskName": task_name,
            "address": address,
            "method": method,
            "postContent": post_content,
            "advanceConfig": advance_config,
            "cycle": cycle,
            "idc": idc,
            "timeout": timeout,
        }

        return self._send_csm_request(http_methods.PUT, path, body=json.dumps(body), config=config)

    def get_site_https_task_config(self, user_id=None, task_id=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/https/detail' % (user_id)
        params = {}

        if task_id is not None:
            params["taskId"] = task_id

        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def create_site_ping_task_config(self, user_id=None, task_name=None, address=None,
                                     packet_count=None, packet_loss_rate=None, cycle=None, idc=None,
                                     timeout=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_name:
        :type task_name: string
        :param address:
        :type address: string
        :param packet_count:
        :type packet_count: int
        :param packet_loss_rate:
        :type packet_loss_rate: int
        :param cycle:
        :type cycle: int
        :param idc:
        :type idc: string
        :param timeout:
        :type timeout: int
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/ping/create' % (user_id)
        body = {
            "userId": user_id,
            "taskName": task_name,
            "address": address,
            "packetCount": packet_count,
            "packetLossRate": packet_loss_rate,
            "cycle": cycle,
            "idc": idc,
            "timeout": timeout,
        }

        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def update_site_ping_task_config(self, user_id=None, task_id=None, task_name=None, address=None,
                                     packet_count=None, packet_loss_rate=None, cycle=None, idc=None,
                                     timeout=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param task_name:
        :type task_name: string
        :param address:
        :type address: string
        :param packet_count:
        :type packet_count: int
        :param packet_loss_rate:
        :type packet_loss_rate: int
        :param cycle:
        :type cycle: int
        :param idc:
        :type idc: string
        :param timeout:
        :type timeout: int
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/ping/update' % (user_id)
        body = {
            "userId": user_id,
            "taskId": task_id,
            "taskName": task_name,
            "address": address,
            "packetCount": packet_count,
            "packetLossRate": packet_loss_rate,
            "cycle": cycle,
            "idc": idc,
            "timeout": timeout,
        }

        return self._send_csm_request(http_methods.PUT, path, body=json.dumps(body), config=config)

    def get_site_ping_task_config(self, user_id=None, task_id=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/ping/detail' % (user_id)
        params = {}

        if task_id is not None:
            params["taskId"] = task_id

        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def create_site_tcp_task_config(self, user_id=None, task_name=None, address=None,
                                    port=None, advance_config=None, cycle=None, idc=None, timeout=None,
                                    input_type=None, output_type=None, input=None, expected_output=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_name:
        :type task_name: string
        :param address:
        :type address: string
        :param method:
        :type method: string
        :param post_content:
        :type post_content: string
        :param advance_config:
        :type advance_config: bool
        :param cycle:
        :type cycle: int
        :param idc:
        :type idc: string
        :param timeout:
        :type timeout: int
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/tcp/create' % (user_id)
        body = {
            "userId": user_id,
            "taskName": task_name,
            "address": address,
            "port": port,
            "advanceConfig": advance_config,
            "inputType": input_type,
            "outputType": output_type,
            "input": input,
            "expectedOutput": expected_output,
            "cycle": cycle,
            "idc": idc,
            "timeout": timeout,
        }

        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def update_site_tcp_task_config(self, user_id=None, task_id=None, task_name=None, address=None,
                                    port=None, advance_config=None, cycle=None, idc=None, timeout=None,
                                    input_type=None, output_type=None, input=None, expected_output=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param task_name:
        :type task_name: string
        :param address:
        :type address: string
        :param port:
        :type port: int
        :param post_content:
        :type post_content: string
        :param advance_config:
        :type advance_config: bool
        :param cycle:
        :type cycle: int
        :param idc:
        :type idc: string
        :param timeout:
        :type timeout: int
        :param input_type:
        :type input_type: int
        :param output_type:
        :type output_type: int
        :param input:
        :type input: string
        :param expected_output:
        :type expected_output: string
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/tcp/update' % (user_id)
        body = {
            "userId": user_id,
            "taskId": task_id,
            "taskName": task_name,
            "address": address,
            "port": port,
            "advanceConfig": advance_config,
            "inputType": input_type,
            "outputType": output_type,
            "input": input,
            "expectedOutput": expected_output,
            "cycle": cycle,
            "idc": idc,
            "timeout": timeout,
        }

        return self._send_csm_request(http_methods.PUT, path, body=json.dumps(body), config=config)

    def get_site_tcp_task_config(self, user_id=None, task_id=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/tcp/detail' % (user_id)
        params = {}

        if task_id is not None:
            params["taskId"] = task_id

        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def create_site_udp_task_config(self, user_id=None, task_name=None, address=None,
                                    port=None, advance_config=None, cycle=None, idc=None, timeout=None,
                                    input_type=None, output_type=None, input=None, expected_output=None, config=None):
        """
            :param user_id:
            :type user_id: string
            :param task_name:
            :type task_name: string
            :param address:
            :type address: string
            :param method:
            :type method: string
            :param post_content:
            :type post_content: string
            :param advance_config:
            :type advance_config: bool
            :param cycle:
            :type cycle: int
            :param idc:
            :type idc: string
            :param timeout:
            :type timeout: int
            :param config:
            :type config
            :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/udp/create' % (user_id)
        body = {
            "userId": user_id,
            "taskName": task_name,
            "address": address,
            "port": port,
            "advanceConfig": advance_config,
            "inputType": input_type,
            "outputType": output_type,
            "input": input,
            "expectedOutput": expected_output,
            "cycle": cycle,
            "idc": idc,
            "timeout": timeout,
        }

        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def update_site_udp_task_config(self, user_id=None, task_id=None, task_name=None, address=None,
                                    port=None, advance_config=None, cycle=None, idc=None, timeout=None,
                                    input_type=None, output_type=None, input=None, expected_output=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param task_name:
        :type task_name: string
        :param address:
        :type address: string
        :param port:
        :type port: int
        :param post_content:
        :type post_content: string
        :param advance_config:
        :type advance_config: bool
        :param cycle:
        :type cycle: int
        :param idc:
        :type idc: string
        :param timeout:
        :type timeout: int
        :param input_type:
        :type input_type: int
        :param output_type:
        :type output_type: int
        :param input:
        :type input: string
        :param expected_output:
        :type expected_output: string
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/udp/update' % (user_id)
        body = {
            "userId": user_id,
            "taskId": task_id,
            "taskName": task_name,
            "address": address,
            "port": port,
            "advanceConfig": advance_config,
            "inputType": input_type,
            "outputType": output_type,
            "input": input,
            "expectedOutput": expected_output,
            "cycle": cycle,
            "idc": idc,
            "timeout": timeout,
        }

        return self._send_csm_request(http_methods.PUT, path, body=json.dumps(body), config=config)

    def get_site_udp_task_config(self, user_id=None, task_id=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/udp/detail' % (user_id)
        params = {}

        if task_id is not None:
            params["taskId"] = task_id

        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def create_site_ftp_task_config(self, user_id=None, task_name=None, address=None,
                                    port=None, anonymous_login=None, cycle=None, idc=None, timeout=None,
                                    user_name=None, password=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_name:
        :type task_name: string
        :param address:
        :type address: string
        :param port:
        :type port: int
        :param post_content:
        :type post_content: string
        :param anonymous_login:
        :type anonymous_login: bool
        :param cycle:
        :type cycle: int
        :param idc:
        :type idc: string
        :param timeout:
        :type timeout: int
        :param user_name:
        :type user_name: string
        :param password:
        :type password: string
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/ftp/create' % (user_id)
        body = {
            "userId": user_id,
            "taskName": task_name,
            "address": address,
            "port": port,
            "anonymousLogin": anonymous_login,
            "userName": user_name,
            "password": password,
            "cycle": cycle,
            "idc": idc,
            "timeout": timeout,
        }

        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def update_site_ftp_task_config(self, user_id=None, task_id=None, task_name=None, address=None,
                                    port=None, anonymous_login=None, cycle=None, idc=None, timeout=None,
                                    user_name=None, password=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param task_name:
        :type task_name: string
        :param address:
        :type address: string
        :param port:
        :type port: int
        :param post_content:
        :type post_content: string
        :param anonymous_login:
        :type anonymous_login: bool
        :param cycle:
        :type cycle: int
        :param idc:
        :type idc: string
        :param timeout:
        :type timeout: int
        :param user_name:
        :type user_name: string
        :param password:
        :type password: string
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/ftp/update' % (user_id)
        body = {
            "userId": user_id,
            "taskId": task_id,
            "taskName": task_name,
            "address": address,
            "port": port,
            "anonymousLogin": anonymous_login,
            "userName": user_name,
            "password": password,
            "cycle": cycle,
            "idc": idc,
            "timeout": timeout,
        }

        return self._send_csm_request(http_methods.PUT, path, body=json.dumps(body), config=config)

    def get_site_ftp_task_config(self, user_id=None, task_id=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/ftp/detail' % (user_id)
        params = {}

        if task_id is not None:
            params["taskId"] = task_id

        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def create_site_dns_task_config(self, user_id=None, task_name=None, address=None,
                                    cycle=None, idc=None, timeout=None,
                                    server=None, resolve_type=None, kidnap_white=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_name:
        :type task_name: string
        :param address:
        :type address: string
        :param post_content:
        :type post_content: string
        :param cycle:
        :type cycle: int
        :param idc:
        :type idc: string
        :param timeout:
        :type timeout: int
        :param server:
        :type server: string
        :param resolve_type:
        :type resolve_type: ENUM {'RECURSION', 'ITERATION'}
        :param kidnap_white:
        :type kidnap_white: string
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/dns/create' % (user_id)
        body = {
            "userId": user_id,
            "taskName": task_name,
            "address": address,
            "server": server,
            "resolveType": resolve_type,
            "kidnapWhite": kidnap_white,
            "cycle": cycle,
            "idc": idc,
            "timeout": timeout,
        }

        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def update_site_dns_task_config(self, user_id=None, task_id=None, task_name=None, address=None,
                                    cycle=None, idc=None, timeout=None,
                                    server=None, resolve_type=None, kidnap_white=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param task_name:
        :type task_name: string
        :param address:
        :type address: string
        :param post_content:
        :type post_content: string
        :param cycle:
        :type cycle: int
        :param idc:
        :type idc: string
        :param timeout:
        :type timeout: int
        :param server:
        :type server: string
        :param resolve_type:
        :type resolve_type: ENUM {'RECURSION', 'ITERATION'}
        :param kidnap_white:
        :type kidnap_white: string
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/dns/update' % (user_id)
        body = {
            "userId": user_id,
            "taskId": task_id,
            "taskName": task_name,
            "address": address,
            "server": server,
            "resolveType": resolve_type,
            "kidnapWhite": kidnap_white,
            "cycle": cycle,
            "idc": idc,
            "timeout": timeout,
        }

        return self._send_csm_request(http_methods.PUT, path, body=json.dumps(body), config=config)

    def get_site_dns_task_config(self, user_id=None, task_id=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param config:
        :type config
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/dns/detail' % (user_id)
        params = {}

        if task_id is not None:
            params["taskId"] = task_id

        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def get_site_task_config_list(self, user_id=None, query=None, type=None, page_no=None, page_size=None, config=None):

        """
        :param user_id:
        :type user_id: string
        :param query:
        :type query: string
        :param type:
        :type type: string
        :param page_no:
        :type page_no: int
        :param page_size:
        :type page_size: int
        :param config:
        :type config:
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/list' % (user_id)
        if query is None:
            query = "NAME:"
        params = {
            b'query': query,
            b'type': type,
        }

        if page_no is None:
            params[b'pageNo'] = 1
        else:
            params[b'pageNo'] = page_no
        if page_size is None:
            params[b'pageSize'] = 10
        else:
            params[b'pageSize'] = page_size

        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def delete_site_task_config(self, user_id=None, task_id=None, config=None):

        """
        :param user_id:
        :type user_id: string
        :param task_Id:
        :type task_Id: string
        :param config:
        :type config:
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/delete' % (user_id)
        params = {
            b'taskId': task_id,
        }

        return self._send_csm_request(http_methods.DELETE, path, params=params, config=config)

    def get_site_task_config_info(self, user_id=None, task_id=None, config=None):

        """
        :param user_id:
        :type user_id: string
        :param task_Id:
        :type task_Id: string
        :param config:
        :type config:
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        task_id = compat.convert_to_bytes(task_id)
        path = b'/userId/%s/site/%s' % (user_id, task_id)

        return self._send_csm_request(http_methods.GET, path, config=config)

    def create_site_alarm_config(self, user_id=None, task_id=None, comment=None, alias_name=None,
                                 level=None, action_enabled=None, resume_actions=None, insufficient_actions=None,
                                 incident_action=None, insufficient_cycle=None, rules=None, region=None,
                                 callback_url=None, method=None, site_monitor=None, tag=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param comment:
        :type comment: string
        :param alias_name:
        :type alias_name: string
        :param level:
        :type level: ENUM {'NOTICE', 'WARNING', 'CRITICAL', 'MAJOR', 'CUSTOM'}
        :param action_enabled:
        :type action_enabled: bool
        :param resume_actions:
        :type :type user_id: string: string
        :param insufficient_actions:
        :type insufficient_actions: string
        :param incident_action:
        :type incident_action: string
        :param insufficient_cycle:
        :type insufficient_cycle: int
        :param rules:
        :type rules: list of SiteAlarmRule
        :param region:
        :type region: string
        :param callback_url:
        :type callback_url: string
        :param method:
        :type method: string
        :param site_monitor:
        :type site_monitor: string
        :param tag:
        :type tag: string
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/alarm/config/create' % (user_id)
        body = {
            "userId": user_id,
            "taskId": task_id,
            "comment": comment,
            "aliasName": alias_name,
            "level": level,
            "actionEnabled": action_enabled,
            "resumeActions": resume_actions,
            "insufficientActions": insufficient_actions,
            "incidentAction": incident_action,
            "insufficientCycle": insufficient_cycle,
            "rules": rules,
            "region": region,
            "callbackUrl": callback_url,
            "method": method,
            "siteMonitor": site_monitor,
            "tag": tag
        }

        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config)

    def delete_site_alarm_config(self, user_id=None, alarm_names=None, config=None):

        """
        :param user_id:
        :type user_id: string
        :param alarm_names:
        :type alarm_names: list
        :param config:
        :type config:
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/alarm/config/delete' % (user_id)
        body = {
            "alarmNames": alarm_names
        }

        return self._send_csm_request(http_methods.DELETE, path, body=json.dumps(body), config=config)

    def update_site_alarm_config(self, user_id=None, task_id=None, alarm_name=None, comment=None, alias_name=None,
                                 level=None, action_enabled=None, resume_actions=None, insufficient_actions=None,
                                 incident_action=None, insufficient_cycle=None, rules=None, region=None,
                                 callback_url=None, method=None, site_monitor=None, tag=None, config=None):
        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param alarm_name:
        :type alarm_name: string
        :param comment:
        :type comment: string
        :param alias_name:
        :type alias_name: string
        :param level:
        :type level: ENUM {'NOTICE', 'WARNING', 'CRITICAL', 'MAJOR', 'CUSTOM'}
        :param action_enabled:
        :type action_enabled: bool
        :param resume_actions:
        :type :type user_id: string: string
        :param insufficient_actions:
        :type insufficient_actions: string
        :param incident_action:
        :type incident_action: string
        :param insufficient_cycle:
        :type insufficient_cycle: int
        :param rules:
        :type rules: list of SiteAlarmRule
        :param region:
        :type region: string
        :param callback_url:
        :type callback_url: string
        :param method:
        :type method: string
        :param site_monitor:
        :type site_monitor: string
        :param tag:
        :type tag: string
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/alarm/config/update' % (user_id)
        body = {
            "userId": user_id,
            "taskId": task_id,
            "alarmName": alarm_name,
            "comment": comment,
            "aliasName": alias_name,
            "level": level,
            "actionEnabled": action_enabled,
            "resumeActions": resume_actions,
            "insufficientActions": insufficient_actions,
            "incidentAction": incident_action,
            "insufficientCycle": insufficient_cycle,
            "rules": rules,
            "region": region,
            "callbackUrl": callback_url,
            "method": method,
            "siteMonitor": site_monitor,
            "tag": tag
        }

        return self._send_csm_request(http_methods.PUT, path, body=json.dumps(body), config=config)

    def get_site_alarm_config_detail(self, user_id=None, alarm_name=None, config=None):

        """
        :param user_id:
        :type user_id: string
        :param alarm_name:
        :type alarm_name: string
        :param config:
        :type config:
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/alarm/config/detail' % (user_id)
        params = {
            b'alarmName': alarm_name,
        }

        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def get_site_alarm_config_list(self, user_id=None, task_id=None, alarm_name=None,
                                   action_enabled=None, page_no=None, page_size=None, config=None):

        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param alarm_name:
        :type alarm_name: string
        :param action_enabled:
        :type action_enabled: bool
        :param page_no:
        :type page_no: int
        :param page_size:
        :type page_size: int
        :param config:
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/alarm/config/list' % (user_id)
        params = {}

        if task_id is not None:
            params[b'taskId'] = task_id
        if alarm_name is not None:
            params[b'alarmName'] = alarm_name
        if action_enabled is not None:
            params[b'actionEnabled'] = action_enabled

        if page_no is None:
            params[b'pageNo'] = 1
        else:
            params[b'pageNo'] = page_no
        if page_size is None:
            params[b'pageSize'] = 10
        else:
            params[b'pageSize'] = page_size

        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def block_site_alarm_config(self, user_id=None, alarm_name=None, namespace=None, config=None):

        """
        :param user_id:
        :type user_id: string
        :param alarm_name:
        :type alarm_name: string
        :param config:
        :type config:
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/alarm/config/block' % (user_id)
        params = {
            "alarmName": alarm_name,
            "namespace": namespace
        }

        return self._send_csm_request(http_methods.POST, path, params=params, config=config)

    def unblock_site_alarm_config(self, user_id=None, alarm_name=None, namespace=None, config=None):

        """
        :param user_id:
        :type user_id: string
        :param alarm_name:
        :type alarm_name: string
        :param config:
        :type config:
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/alarm/config/unblock' % (user_id)
        params = {
            "alarmName": alarm_name,
            "namespace": namespace
        }

        return self._send_csm_request(http_methods.POST, path, params=params, config=config)

    def get_site_metric_data(self, user_id=None, task_id=None, metric_name=None, statistics=None,
                             start_time=None, end_time=None, cycle=None,
                             dimensions=None, config=None):

        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param metric_name:
        :type metric_name: string
        :param statistics:
        :type statistics: list
        :param start_time:
        :type start_time: string
        :param end_time:
        :type end_time: string
        :param cycle:
        :type cycle: int
        :param dimensions:
        :type dimensions: string
        :param config:
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/metricSiteData' % (user_id)
        params = {
            "taskId": task_id,
        }

        if metric_name is not None:
            params[b'metricName'] = metric_name
        if dimensions is not None:
            params[b'dimensions'] = dimensions
        if statistics is not None and len(statistics) > 0:
            params[b'statistics'] = ",".join(statistics)
        if start_time is not None:
            params[b'startTime'] = start_time
        if end_time is not None:
            params[b'endTime'] = end_time
        if cycle is not None:
            params[b'cycle'] = cycle

        return self._send_csm_request(http_methods.GET, path, params=params,
                                      body_parser=bcm_handler.parse_json_list, config=config)

    def get_site_overall_view(self, user_id=None, task_id=None, config=None):

        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param config:
        :type config:
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/idc/overallView' % (user_id)
        params = {
            "taskId": task_id
        }

        return self._send_csm_request(http_methods.GET, path, params=params,
                                      body_parser=bcm_handler.parse_json_list, config=config)

    def get_site_provincial_view(self, user_id=None, task_id=None, isp=None, config=None):

        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param isp:
        :type isp: string
        :param config:
        :type config:
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/idc/provincialView' % (user_id)
        params = {
            "taskId": task_id,
            "isp": isp
        }

        return self._send_csm_request(http_methods.GET, path, params=params,
                                      body_parser=bcm_handler.parse_json_list, config=config)

    def get_site_agent(self, user_id=None, config=None):

        """
        :param user_id:
        :type user_id: string
        :param config:
        :type config:
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/agent/list' % (user_id)

        return self._send_csm_request(http_methods.GET, path, body_parser=bcm_handler.parse_json_list, config=config)

    def get_site_agent_for_task(self, user_id=None, task_id=None, config=None):

        """
        :param user_id:
        :type user_id: string
        :param task_id:
        :type task_id: string
        :param config:
        :type config:
        :return:
        """

        user_id = compat.convert_to_bytes(user_id)
        path = b'/userId/%s/site/agent/idcIsp' % (user_id)
        params = {
            "taskId": task_id
        }

        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def create_alarm_config(self, user_id, alias_name, scope, level, region, monitor_object, alarm_actions, rules,
                            src_type="INSTANCE", ok_actions=None, insufficient_actions=None, config_type="NORMAL",
                            insufficient_cycle=0, max_repeat_count=0, repeat_alarm_cycle=0, callback_url="",
                            callback_token="", description="", config=None):
        """
            create alarm config

            This site may help you: https://cloud.baidu.com/doc/BCM/s/Vks8iqqnx

            :param user_id: master account id
            :type user_id: string

            :param alias_name: alarm config alias name
            :type alias_name: string

            :param scope: scope
            :type scope: string

            :param level: alarm level
            :type level: string

            :param region: alarm region
            :type region: string

            :param monitor_object: monitor object
            :type monitor_object: MonitorObject

            :param alarm_actions: alarm actions
            :type alarm_actions: string array

            :param rules: alarm rules
            :type rules: AlarmRule double dimensional array

            :param src_type: src type
            :type src_type: string

            :param ok_actions: ok actions
            :type ok_actions: string array

            :param insufficient_actions: insufficient actions
            :type insufficient_actions: string array

            :param config_type: alarm config type
            :type config_type: string

            :param insufficient_cycle: insufficient cycle
            :type insufficient_cycle: int

            :param max_repeat_count: max repeat count
            :type max_repeat_count: int

            :param repeat_alarm_cycle: repeat alarm cycle
            :type repeat_alarm_cycle: int

            :param callback_url: callback url
            :type callback_url: string

            :param callback_token: callback token
            :type callback_token: string

            :param description: description
            :type description: string

            :param config:
            :type config: baidubce.BceClientConfiguration

        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(alias_name) <= 0:
            raise ValueError('alias_name should not be none or empty string')
        if len(scope) <= 0:
            raise ValueError('scope should not be none or empty string')
        if len(region) <= 0:
            raise ValueError('region should not be none or empty string')
        if len(level) <= 0:
            raise ValueError('level should not be none or empty string')
        if monitor_object is None:
            raise ValueError('monitor_object should not be none')
        if len(alarm_actions) <= 0:
            raise ValueError('alarm_actions should not be empty')
        if len(rules) <= 0:
            raise ValueError('rules should not be empty')
        if insufficient_actions is None:
            insufficient_actions = []
        if ok_actions is None:
            ok_actions = []

        path = b'/services/alarm/config/create'
        body = {
            "alarmDescription": description,
            "aliasName": alias_name,
            "userId": user_id,
            "scope": scope,
            "region": region,
            "level": level,
            "monitorObject": monitor_object,
            "alarmActions": alarm_actions,
            "okActions": ok_actions,
            "insufficientActions": insufficient_actions,
            "srcType": src_type,
            "type": config_type,
            "insufficientCycle": insufficient_cycle,
            "maxRepeatCount": max_repeat_count,
            "repeatAlarmCycle": repeat_alarm_cycle,
            "callbackUrl": callback_url,
            "callbackToken": callback_token,
            "rules": rules,
        }
        self._send_csm_request(http_methods.POST, path, body=json.dumps(body))

    def update_alarm_config(self, user_id, alarm_name, alias_name, scope, level, region,
                            monitor_object, alarm_actions, rules,
                            src_type="INSTANCE", ok_actions=None, insufficient_actions=None, config_type="NORMAL",
                            insufficient_cycle=0, max_repeat_count=0, repeat_alarm_cycle=0, callback_url="",
                            callback_token="", description="", config=None):
        """
            update alarm config

            This site may help you: https://cloud.baidu.com/doc/BCM/s/Vks8iqqnx

            :param user_id: master account id
            :type user_id: string

            :param alarm_name: alarm config name
            :type alarm_name: string

            :param alias_name: alarm config alias name
            :type alias_name: string

            :param scope: scope
            :type scope: string

            :param level: alarm level
            :type level: string

            :param region: alarm region
            :type region: string

            :param monitor_object: monitor object
            :type monitor_object: MonitorObject

            :param alarm_actions: alarm actions
            :type alarm_actions: string array

            :param rules: alarm rules
            :type rules: AlarmRule double dimensional array

            :param src_type: src type
            :type src_type: string

            :param ok_actions: ok actions
            :type ok_actions: string array

            :param insufficient_actions: insufficient actions
            :type insufficient_actions: string array

            :param config_type: alarm config type
            :type config_type: string

            :param insufficient_cycle: insufficient cycle
            :type insufficient_cycle: int

            :param max_repeat_count: max repeat count
            :type max_repeat_count: int

            :param repeat_alarm_cycle: repeat alarm cycle
            :type repeat_alarm_cycle: int

            :param callback_url: callback url
            :type callback_url: string

            :param callback_token: callback token
            :type callback_token: string

            :param description: description
            :type description: string

            :param config:
            :type config: baidubce.BceClientConfiguration

        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(alias_name) <= 0:
            raise ValueError('alias_name should not be none or empty string')
        if len(alarm_name) <= 0:
            raise ValueError('alarm_name should not be none or empty string')
        if len(scope) <= 0:
            raise ValueError('scope should not be none or empty string')
        if len(region) <= 0:
            raise ValueError('region should not be none or empty string')
        if len(level) <= 0:
            raise ValueError('level should not be none or empty string')
        if monitor_object is None:
            raise ValueError('monitor_object should not be none')
        if len(alarm_actions) <= 0:
            raise ValueError('alarm_actions should not be empty')
        if len(rules) <= 0:
            raise ValueError('rules should not be empty')
        if insufficient_actions is None:
            insufficient_actions = []
        if ok_actions is None:
            ok_actions = []

        path = b'/services/alarm/config/update'
        body = {
            "alarmDescription": description,
            "alarmName": alarm_name,
            "aliasName": alias_name,
            "userId": user_id,
            "scope": scope,
            "region": region,
            "level": level,
            "monitorObject": monitor_object,
            "alarmActions": alarm_actions,
            "okActions": ok_actions,
            "insufficientActions": insufficient_actions,
            "srcType": src_type,
            "type": config_type,
            "insufficientCycle": insufficient_cycle,
            "maxRepeatCount": max_repeat_count,
            "repeatAlarmCycle": repeat_alarm_cycle,
            "callbackUrl": callback_url,
            "callbackToken": callback_token,
            "rules": rules,
        }
        self._send_csm_request(http_methods.POST, path, body=json.dumps(body))

    def delete_alarm_config(self, user_id, alarm_name, scope, config=None):
        """
            delete alarm config

            This site may help you: https://cloud.baidu.com/doc/BCM/s/Vks8iqqnx

            :param user_id: master account id
            :type user_id: string

            :param alarm_name: alarm config name
            :type alarm_name: string

            :param scope: scope
            :type scope: string

            :param config:
            :type config: baidubce.BceClientConfiguration

        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(alarm_name) <= 0:
            raise ValueError('alarm_name should not be none or empty string')
        if len(scope) <= 0:
            raise ValueError('scope should not be none or empty string')

        path = b'/services/alarm/config/delete'
        params = {
            b"alarmName": alarm_name,
            b"userId": user_id,
            b"scope": scope,
        }
        self._send_csm_request(http_methods.POST, path, params=params, config=config)

    def block_alarm_config(self, user_id, alarm_name, scope, config=None):
        """
            block alarm config

            This site may help you: https://cloud.baidu.com/doc/BCM/s/Vks8iqqnx

            :param user_id: master account id
            :type user_id: string

            :param alarm_name: alarm config name
            :type alarm_name: string

            :param scope: scope
            :type scope: string

            :param config:
            :type config: baidubce.BceClientConfiguration

        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(alarm_name) <= 0:
            raise ValueError('alarm_name should not be none or empty string')
        if len(scope) <= 0:
            raise ValueError('scope should not be none or empty string')

        path = b'/services/alarm/config/block'
        params = {
            b"alarmName": alarm_name,
            b"userId": user_id,
            b"scope": scope,
        }
        self._send_csm_request(http_methods.POST, path, params=params, config=config)

    def unblock_alarm_config(self, user_id, alarm_name, scope, config=None):
        """
            unblock alarm config

            This site may help you: https://cloud.baidu.com/doc/BCM/s/Vks8iqqnx

            :param user_id: master account id
            :type user_id: string

            :param alarm_name: alarm config name
            :type alarm_name: string

            :param scope: scope
            :type scope: string

            :param config:
            :type config: baidubce.BceClientConfiguration

        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(alarm_name) <= 0:
            raise ValueError('alarm_name should not be none or empty string')
        if len(scope) <= 0:
            raise ValueError('scope should not be none or empty string')

        path = b'/services/alarm/config/unblock'
        params = {
            b"alarmName": alarm_name,
            b"userId": user_id,
            b"scope": scope,
        }
        self._send_csm_request(http_methods.POST, path, params=params, config=config)

    def get_alarm_config_detail(self, user_id, alarm_name, scope, config=None):
        """
            get alarm config detail

            This site may help you: https://cloud.baidu.com/doc/BCM/s/Vks8iqqnx

            :param user_id: master account id
            :type user_id: string

            :param alarm_name: alarm config name
            :type alarm_name: string

            :param scope: scope
            :type scope: string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(alarm_name) <= 0:
            raise ValueError('alarm_name should not be none or empty string')
        if len(scope) <= 0:
            raise ValueError('scope should not be none or empty string')

        path = b'/services/alarm/config'
        params = {
            b"alarmName": alarm_name,
            b"userId": user_id,
            b"scope": scope,
        }
        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def get_single_instance_alarm_configs(self, user_id, scope, page_no, page_size,
                                          region="bj", alarm_name_prefix="", action_enabled=None, dimensions="",
                                          order="desc", config=None):
        """
            get alarm config detail

            This site may help you: https://cloud.baidu.com/doc/BCM/s/Vks8iqqnx

            :param user_id: master account id
            :type user_id: string

            :param scope: scope
            :type scope: string

            :param region: region
            :type region: string

            :param page_no: page no
            :type page_no: int

            :param page_size: page size
            :type page_size: int

            :param alarm_name_prefix: alarm name prefix
            :type alarm_name_prefix: string

            :param action_enabled: action enable flag
            :type action_enabled: bool

            :param dimensions: dimensions
            :type dimensions: string

            :param order: order
            :type order: string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(scope) <= 0:
            raise ValueError('scope should not be none or empty string')
        if page_no <= 0:
            raise ValueError('page_no should be greater than 0')
        if page_size <= 0:
            raise ValueError('page_size should be greater than 0')

        path = b'/services/alarm/config/list'
        params = {
            b"region": region,
            b"userId": user_id,
            b"scope": scope,
            b"pageNo": page_no,
            b"pageSize": page_size,
            b"dimensions": dimensions,
            b"order": order,
            b"alarmNamePrefix": alarm_name_prefix,
        }
        if action_enabled is not None:
            if action_enabled:
                params["actionEnabled"] = "true"
            else:
                params["actionEnabled"] = "false"
        return self._send_csm_request(http_methods.GET, path, params=params, config=config)

    def get_alarm_metrics(self, user_id, scope, region="bj", dimensions="", metric_type="", locale="", config=None):
        """
            get alarm config detail

            This site may help you: https://cloud.baidu.com/doc/BCM/s/Vks8iqqnx

            :param user_id: master account id
            :type user_id: string

            :param scope: scope
            :type scope: string

            :param region: region
            :type region: string

            :param dimensions: dimensions
            :type dimensions: string

            :param metric_type: metric type
            :type metric_type: string

            :param locale: locale
            :type locale: string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(scope) <= 0:
            raise ValueError('scope should not be none or empty string')

        path = b'/services/alarm/config/metrics'
        params = {
            b"region": region,
            b"userId": user_id,
            b"scope": scope,
            b"dimensions": dimensions,
            b"type": metric_type,
            b"locale": locale,
        }
        return self._send_csm_request(http_methods.GET, path, params=params,
                                      body_parser=bcm_handler.parse_json_list, config=config)

    def create_alarm_config_v2(self, user_id, alias_name, scope, target_type, level, region, actions, policies,
                               target_instances=None, insufficient_period=0,
                               alarm_repeat_interval=0, alarm_repeat_count=0,
                               callback_url="", callback_token="", target_instance_tags=None,
                               target_instance_groups=None, resource_type="Instance", config=None):
        """
            get alarm config detail

            This site may help you: https://cloud.baidu.com/doc/BCM/s/blhrp7kdx

            :param user_id: master account id
            :type user_id: string

            :param alias_name: alarm config alias name
            :type alias_name: string

            :param scope: scope
            :type scope: string

            :param target_type: alarm config target type
            :type target_type: string

            :param level: alarm level
            :type level: string

            :param region: alarm config region
            :type region: string

            :param actions: alarm actions
            :type actions: AlarmAction array

            :param policies: alarm config policies
            :type policies: AlarmConfigPolicy array

            :param target_instances: alarm config target instances
            :type target_instances: TargetInstance array

            :param insufficient_period: insufficient data pending period
            :type insufficient_period: int

            :param alarm_repeat_interval: alarm repeat interval
            :type alarm_repeat_interval: int

            :param alarm_repeat_count: alarm repeat count
            :type alarm_repeat_count: int

            :param callback_url: callback url
            :type callback_url: string

            :param callback_token: callback token
            :type callback_token: string

            :param target_instance_tags: target instance tags
            :type target_instance_tags: KV array

            :param target_instance_groups: target instance groups
            :type target_instance_groups: string array

            :param resource_type: resource type
            :type resource_type: string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(scope) <= 0:
            raise ValueError('scope should not be none or empty string')
        if len(alias_name) <= 0:
            raise ValueError('alias_name should not be none or empty string')
        if len(target_type) <= 0:
            raise ValueError('target_type should not be none or empty string')
        if len(level) <= 0:
            raise ValueError('level should not be none or empty string')
        if len(region) <= 0:
            raise ValueError('region should not be none or empty string')
        if len(actions) <= 0:
            raise ValueError('actions should not be empty')
        if len(policies) <= 0:
            raise ValueError('policies should not be empty')
        if target_type == "TARGET_TYPE_MULTI_INSTANCES" and len(target_instances) <= 0:
            raise ValueError('target_instances should not be empty')
        if target_type == "TARGET_TYPE_INSTANCE_GROUP" and len(target_instance_groups) <= 0:
            raise ValueError('target_instance_groups should not be empty')
        if target_type == "TARGET_TYPE_INSTANCE_TAGS" and len(target_instance_tags) <= 0:
            raise ValueError('target_instance_tags should not be empty')
        if target_instance_groups is None:
            target_instance_groups = []
        if target_instance_tags is None:
            target_instance_tags = []
        if target_instances is None:
            target_instances = []

        path = b'/userId/%s/services/%s/alarm/config/create' % (user_id, scope)
        body = {
            "userId": user_id,
            "scope": scope,
            "aliasName": alias_name,
            "targetType": target_type,
            "resourceType": resource_type,
            "alarmLevel": level,
            "targetInstanceGroups": target_instance_groups,
            "targetInstanceTags": target_instance_tags,
            "callbackUrl": callback_url,
            "callbackToken": callback_token,
            "insufficientDataPendingPeriod": insufficient_period,
            "alarmRepeatInterval": alarm_repeat_interval,
            "alarmRepeatCount": alarm_repeat_count,
            "policies": policies,
            "targetInstances": target_instances,
            "actions": actions,
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body), config=config,
                                      version=BcmClient.version_v2)

    def update_alarm_config_v2(self, user_id, alarm_name, alias_name, scope, target_type, level, region,
                               actions, policies, target_instances=None, insufficient_period=0,
                               alarm_repeat_interval=0, alarm_repeat_count=0,
                               callback_url="", callback_token="", target_instance_tags=None,
                               target_instance_groups=None, resource_type="Instance", config=None):
        """
            get alarm config detail

            This site may help you: https://cloud.baidu.com/doc/BCM/s/blhrp7kdx

            :param user_id: master account id
            :type user_id: string

            :param alarm_name: alarm config name
            :type alarm_name: string

            :param alias_name: alarm config alias name
            :type alias_name: string

            :param scope: scope
            :type scope: string

            :param target_type: alarm config target type
            :type target_type: string

            :param level: alarm level
            :type level: string

            :param region: alarm config region
            :type region: string

            :param actions: alarm actions
            :type actions: AlarmAction array

            :param policies: alarm config policies
            :type policies: AlarmConfigPolicy array

            :param target_instances: alarm config target instances
            :type target_instances: TargetInstance array

            :param insufficient_period: insufficient data pending period
            :type insufficient_period: int

            :param alarm_repeat_interval: alarm repeat interval
            :type alarm_repeat_interval: int

            :param alarm_repeat_count: alarm repeat count
            :type alarm_repeat_count: int

            :param callback_url: callback url
            :type callback_url: string

            :param callback_token: callback token
            :type callback_token: string

            :param target_instance_tags: target instance tags
            :type target_instance_tags: KV array

            :param target_instance_groups: target instance groups
            :type target_instance_groups: string array

            :param resource_type: resource type
            :type resource_type: string

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(scope) <= 0:
            raise ValueError('scope should not be none or empty string')
        if len(alarm_name) <= 0:
            raise ValueError('alarm_name should not be none or empty string')
        if len(alias_name) <= 0:
            raise ValueError('alias_name should not be none or empty string')
        if len(target_type) <= 0:
            raise ValueError('target_type should not be none or empty string')
        if len(level) <= 0:
            raise ValueError('level should not be none or empty string')
        if len(region) <= 0:
            raise ValueError('region should not be none or empty string')
        if len(actions) <= 0:
            raise ValueError('actions should not be empty')
        if len(policies) <= 0:
            raise ValueError('policies should not be empty')
        if target_type == "TARGET_TYPE_MULTI_INSTANCES" and len(target_instances) <= 0:
            raise ValueError('target_instances should not be empty')
        if target_type == "TARGET_TYPE_INSTANCE_GROUP" and len(target_instance_groups) <= 0:
            raise ValueError('target_instance_groups should not be empty')
        if target_type == "TARGET_TYPE_INSTANCE_TAGS" and len(target_instance_tags) <= 0:
            raise ValueError('target_instance_tags should not be empty')
        if target_instance_tags is None:
            target_instance_tags = []
        if target_instance_groups is None:
            target_instance_groups = []
        if target_instances is None:
            target_instances = []

        path = b'/userId/%s/services/%s/alarm/config/update' % (user_id, scope)
        body = {
            "userId": user_id,
            "scope": scope,
            "aliasName": alias_name,
            "alarmName": alarm_name,
            "targetType": target_type,
            "resourceType": resource_type,
            "alarmLevel": level,
            "targetInstanceGroups": target_instance_groups,
            "targetInstanceTags": target_instance_tags,
            "callbackUrl": callback_url,
            "callbackToken": callback_token,
            "insufficientDataPendingPeriod": insufficient_period,
            "alarmRepeatInterval": alarm_repeat_interval,
            "alarmRepeatCount": alarm_repeat_count,
            "policies": policies,
            "targetInstances": target_instances,
            "actions": actions,
        }
        return self._send_csm_request(http_methods.PUT, path, body=json.dumps(body), config=config,
                                      version=BcmClient.version_v2)

    def block_alarm_config_v2(self, user_id, alarm_name, scope, config=None):
        """
            block alarm config v2

            This site may help you: https://cloud.baidu.com/doc/BCM/s/blhrp7kdx

            :param user_id: master account id
            :type user_id: string

            :param alarm_name: alarm config name
            :type alarm_name: string

            :param scope: scope
            :type scope: string

            :param config:
            :type config: baidubce.BceClientConfiguration

        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(alarm_name) <= 0:
            raise ValueError('alarm_name should not be none or empty string')
        if len(scope) <= 0:
            raise ValueError('scope should not be none or empty string')

        path = b'/userId/%s/services/%s/alarm/config/block' % (user_id, scope)
        params = {
            b"alarmName": alarm_name
        }
        self._send_csm_request(http_methods.POST, path, params=params, config=config,
                               version=BcmClient.version_v2)

    def unblock_alarm_config_v2(self, user_id, alarm_name, scope, config=None):
        """
            unblock alarm config v2

            This site may help you: https://cloud.baidu.com/doc/BCM/s/blhrp7kdx

            :param user_id: master account id
            :type user_id: string

            :param alarm_name: alarm config name
            :type alarm_name: string

            :param scope: scope
            :type scope: string

            :param config:
            :type config: baidubce.BceClientConfiguration

        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(alarm_name) <= 0:
            raise ValueError('alarm_name should not be none or empty string')
        if len(scope) <= 0:
            raise ValueError('scope should not be none or empty string')

        path = b'/userId/%s/services/%s/alarm/config/unblock' % (user_id, scope)
        params = {
            b"alarmName": alarm_name
        }
        self._send_csm_request(http_methods.POST, path, params=params, config=config,
                               version=BcmClient.version_v2)

    def get_alarm_config_detail_v2(self, user_id, alarm_name, scope, config=None):
        """
            get alarm config detail v2

            This site may help you: https://cloud.baidu.com/doc/BCM/s/blhrp7kdx

            :param user_id: master account id
            :type user_id: string

            :param alarm_name: alarm config name
            :type alarm_name: string

            :param scope: scope
            :type scope: string

            :param config:
            :type config: baidubce.BceClientConfiguration

        """
        if len(user_id) <= 0:
            raise ValueError('user_id should not be none or empty string')
        if len(alarm_name) <= 0:
            raise ValueError('alarm_name should not be none or empty string')
        if len(scope) <= 0:
            raise ValueError('scope should not be none or empty string')

        path = b'/userId/%s/services/%s/alarm/config' % (user_id, scope)
        params = {
            b"alarmName": alarm_name
        }
        self._send_csm_request(http_methods.GET, path, params=params, config=config, version=BcmClient.version_v2)

    @required(rules=list, insufficientActions=int, repeatAlarmCycle=int, maxRepeatCount=int)
    def create_custom_alarm_policy(self, user_id, alarm_name, namespace, level, comment="",
                                   action_enabled=True, policy_enabled=None, alarm_actions=None, ok_actions=None,
                                   insufficient_actions=None, insufficient_cycle=None, rules=None, region=None,
                                   callback_url=None, callback_token=None, tag="", repeat_alarm_cycle=0,
                                   max_repeat_count=0):

        """
        :param user_id:
        :type user_id: string
        :param alarm_name: alarm name
        :type alarm_name: string
        :param namespace: custom namespace
        :type namespace: string
        :param level: level
        :type level: string  enum: NOTICE, NOTICE, CRITICAL, MAJOR
        :param comment: comment
        :type comment: string
        :param action_enabled: is action enabled
        :type action_enabled: bool
        :param policy_enabled: is policy enabled
        :type policy_enabled: bool
        :param alarm_actions: alarm actions
        :type alarm_actions: list
        :param ok_actions: ok actions
        :type ok_actions: list of string
        :param insufficient_actions: insufficient actions
        :type insufficient_actions: list of string
        :param insufficient_cycle: insufficient cycle
        :type insufficient_cycle: int
        :param rules: rules
        :type rules: list of CustomAlarmRule
        :param region: region
        :type region: string
        :param callback_url: callback url
        :type callback_url: string
        :param callback_token: callback token
        :type callback_token: string
        :param tag: tag
        :type tag: string
        :param repeat_alarm_cycle: repeat alarm cycle
        :type repeat_alarm_cycle: int
        :param max_repeat_count: max repeat count
        :type max_repeat_count: int

        :return
        :rtype baidubce.bce_response.BceResponse
        """
        path = b'/custom/alarm/configs/create'
        body = {
            "userId": user_id,
            "alarmName": alarm_name,
            "namespace": namespace,
            "level": level,
            "comment": comment,
            "actionEnabled": action_enabled,
            "policyEnabled": policy_enabled,
            "alarmActions": alarm_actions,
            "okActions": ok_actions,
            "insufficientActions": insufficient_actions,
            "insufficientCycle": insufficient_cycle,
            "rules": rules,
            "region": region,
            "callbackUrl": callback_url,
            "callbackToken": callback_token,
            "repeatAlarmCycle": repeat_alarm_cycle,
            "maxRepeatCount": max_repeat_count,
            "tag": tag
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body))

    @required(custom_alarm_list=list)
    def delete_custom_alarm_policy(self, custom_alarm_list):
        """
        :param custom_alarm_list:
        :type custom_alarm_list:  list of custom alarm

        :return
        :rtype baidubce.bce_response.BceResponse
        """
        path = (b'/custom/alarm/configs/delete')
        body = {
            "customAlarmList": [
            ]
        }
        for custom_alarm in custom_alarm_list:
            body["customAlarmList"].append({
                "scope": custom_alarm["scope"],
                "userId": custom_alarm["userId"],
                "alarmName": custom_alarm["alarmName"]
            })
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body))

    @required(rules=list, insufficientActions=int, repeatAlarmCycle=int, maxRepeatCount=int)
    def update_custom_alarm_policy(self, user_id, alarm_name, namespace, level, comment="",
                                   action_enabled=True, policy_enabled=None, alarm_actions=None, ok_actions=None,
                                   insufficient_actions=None, insufficient_cycle=None, rules=None, region=None,
                                   callback_url=None, callback_token=None, tag="", repeat_alarm_cycle=0,
                                   max_repeat_count=0):

        """
        :param user_id:
        :type user_id: string
        :param alarm_name: alarm name
        :type alarm_name: string
        :param namespace: custom namespace
        :type namespace: string
        :param level: level
        :type level: string  enum: NOTICE, NOTICE, CRITICAL, MAJOR
        :param comment: comment
        :type comment: string
        :param action_enabled: is action enabled
        :type action_enabled: bool
        :param policy_enabled: is policy enabled
        :type policy_enabled: bool
        :param alarm_actions: alarm actions
        :type alarm_actions: list
        :param ok_actions: ok actions
        :type ok_actions: list of string
        :param insufficient_actions: insufficient actions
        :type insufficient_actions: list of string
        :param insufficient_cycle: insufficient cycle
        :type insufficient_cycle: int
        :param rules: rules
        :type rules: list of CustomAlarmRule
        :param region: region
        :type region: string
        :param callback_url: callback url
        :type callback_url: string
        :param callback_token: callback token
        :type callback_token: string
        :param tag: tag
        :type tag: string
        :param repeat_alarm_cycle: repeat alarm cycle
        :type repeat_alarm_cycle: int
        :param max_repeat_count: max repeat count
        :type max_repeat_count: int

        :return
        :rtype baidubce.bce_response.BceResponse
        """
        if alarm_actions is None:
            alarm_actions = []
        if ok_actions is None:
            alarm_actions = []
        if insufficient_actions is None:
            insufficient_actions = []

        path = b'/custom/alarm/configs/update'
        body = {
            "userId": user_id,
            "alarmName": alarm_name,
            "namespace": namespace,
            "level": level,
            "comment": comment,
            "actionEnabled": action_enabled,
            "policyEnabled": policy_enabled,
            "alarmActions": alarm_actions,
            "okActions": ok_actions,
            "insufficientActions": insufficient_actions,
            "insufficientCycle": insufficient_cycle,
            "rules": rules,
            "region": region,
            "callbackUrl": callback_url,
            "callbackToken": callback_token,
            "repeatAlarmCycle": repeat_alarm_cycle,
            "maxRepeatCount": max_repeat_count,
            "tag": tag
        }
        return self._send_csm_request(http_methods.PUT, path, body=json.dumps(body))

    def list_custom_policy(self, user_id, page_no, page_size, alarm_name=None, namespace=None, action_enabled=None):
        """
        :param user_id:
        :type user_id: string
        :param page_no: page number
        :type page_no: int
        :param page_size: page size
        :type page_size: int
        :param alarm_name: alarm name
        :type alarm_name: string
        :param namespace: namespace
        :type namespace: string
        :param action_enabled: is action enabled
        :type action_enabled: bool

        :return
        :rtype baidubce.bce_response.BceResponse
        """
        params = {
            b'pageNo': page_no,
            b'pageSize': page_size,
            b'userId': user_id,
            b'alarmName': alarm_name,
            b'actionEnabled': action_enabled,
            b'namespace': namespace
        }
        path = b'/custom/alarm/configs/list'
        return self._send_csm_request(http_methods.GET, path, params=params)

    def detail_custom_policy(self, user_id, namespace, alarm_name):
        """
        :param user_id:
        :type user_id: string
        :param namespace: namespace
        :type namespace: string
        :param alarm_name: alarm name
        :type alarm_name: string

        :return: Returns detailed information about a custom policy.
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {
            b'userId': user_id,
            b'alarmName': alarm_name,
            b'namespace': namespace
        }
        path = b'/custom/alarm/configs/detail'
        return self._send_csm_request(http_methods.GET, path, params=params)

    def block_custom_policy(self, user_id, namespace, alarm_name):
        """
        :param user_id: User's identifier
        :type user_id: string
        :param namespace: Namespace
        :type namespace: string
        :param alarm_name: Alarm name
        :type alarm_name: string

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {
            b'userId': user_id,
            b'alarmName': alarm_name,
            b'namespace': namespace
        }
        path = b'/custom/alarm/configs/block'
        return self._send_csm_request(http_methods.POST, path, params=params)

    def unblock_custom_policy(self, user_id, namespace, alarm_name):
        """
        :param user_id: User's identifier
        :type user_id: str
        :param namespace: Namespace
        :type namespace: str
        :param alarm_name: Alarm name
        :type alarm_name: str

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {
            b'userId': user_id,
            b'alarmName': alarm_name,
            b'namespace': namespace
        }
        path = b'/custom/alarm/configs/unblock'
        return self._send_csm_request(http_methods.POST, path, params=params)

    def create_site_once_task(self, site_once_type, user_id, address, idc, timeout, protocol_type, once_config,
                              task_type="NET_QUAILTY", ip_type="ipv4", advanced_flag=False,
                              advanced_config=None, group_id=None):
        """
        :param site_once_type: Type of site
        :type site_once_type: str
        :param user_id: User's identifier
        :type user_id: str
        :param address: Address
        :type address: str
        :param idc: IDC
        :type idc: str
        :param timeout: Timeout
        :type timeout: int
        :param protocol_type: Protocol type
        :type protocol_type: str
        :param once_config: Configuration for once
        :type once_config: dict
        :param task_type: Task type
        :type task_type: str
        :param ip_type: IP type
        :type ip_type: str
        :param advanced_flag: Advanced flag
        :type advanced_flag: bool
        :param advanced_config: Advanced configuration
        :type advanced_config: dict
        :param group_id: Group identifier
        :type group_id: str

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        types = ["HTTP", "HTTPS", "PING", "FTP", "TCP", "UDP", "DNS"]
        if site_once_type is not None and site_once_type not in types:
            raise ValueError('site_once_type must be none or one of %s' % str(types))
        path = (b'/site/once/%s/taskCreate' % compat.convert_to_bytes(site_once_type))
        if advanced_config is None:
            advanced_config = {}
        body = {
            "userId": user_id,
            "address": address,
            "idc": idc,
            "timeout": timeout,
            "protocolType": protocol_type,
            "onceConfig": once_config,
            "taskType": task_type,
            "ipType": ip_type,
            "advancedFlag": advanced_flag,
            "advancedConfig": advanced_config,
            "groupId": group_id
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body))

    def list_site_once_records(self, user_id=None, url=None, page_no=1, page_size=10,
                               order=None, order_by=None, group_id=None):
        """
        :param user_id: User's identifier, defaults to None
        :type user_id: str
        :param url: URL
        :type url: str
        :param page_no: Page number
        :type page_no: int
        :param page_size: Page size
        :type page_size: int
        :param order: Order
        :type order: str
        :param order_by: Order by
        :type order_by: str
        :param group_id: Group identifier
        :type group_id: str

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/site/once/taskList'
        body = {
            "userId": user_id,
            "url": url,
            "pageNo": page_no,
            "pageSize": page_size,
            "order": order,
            "orderBy": order_by,
            "groupId": group_id
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body))

    def delete_site_once_record(self, user_id, site_id):
        """
        :param user_id: User's identifier
        :type user_id: str
        :param site_id: Site identifier
        :type site_id: str

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/site/once/taskDelete'
        body = {
            "userId": user_id,
            "siteId": site_id,
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body))

    def detail_site_once_result(self, user_id, site_id, page_no=1, page_size=10, order=None, order_by=None,
                                filter_area=None, filter_isp=None):
        """
        :param user_id: User's identifier
        :type user_id: str
        :param site_id: Site identifier
        :type site_id: str
        :param page_no: Page number
        :type page_no: int
        :param page_size: Page size
        :type page_size: int
        :param order: Order
        :type order: str
        :param order_by: Order by
        :type order_by: str
        :param filter_area: Filter area
        :type filter_area: str
        :param filter_isp: Filter ISP
        :type filter_isp: str

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/site/once/loadData'
        body = {
            "userId": user_id,
            "siteId": site_id,
            "pageNo": page_no,
            "pageSize": page_size,
            "order": order,
            "orderBy": order_by,
            "filterArea": filter_area,
            "filterIsp": filter_isp
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body))

    def detail_site_once(self, user_id, site_id=None, site_ids=None, group_id=None, page_no=1, page_size=10,
                         order=None, order_by=None, filter_area=None, filter_isp=None):
        """
        :param user_id: User's identifier
        :type user_id: str
        :param site_id: Site identifier
        :type site_id: str
        :param site_ids: List of site identifiers
        :type site_ids: list
        :param group_id: Group identifier
        :type group_id: str
        :param page_no: Page number
        :type page_no: int
        :param page_size: Page size
        :type page_size: int
        :param order: Order
        :type order: str
        :param order_by: Order by
        :type order_by: str
        :param filter_area: Filter area
        :type filter_area: str
        :param filter_isp: Filter ISP
        :type filter_isp: str

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/site/once/groupTask'
        body = {
            "userId": user_id,
            "siteId": site_id,
            "siteIds": site_ids,
            "groupId": group_id,
            "pageNo": page_no,
            "pageSize": page_size,
            "order": order,
            "orderBy": order_by,
            "filterArea": filter_area,
            "filterIsp": filter_isp
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body))

    def again_exec_site_once(self, user_id, site_id):
        """
        :param user_id: User's identifier
        :type user_id: str
        :param site_id: Site identifier
        :type site_id: str

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/site/once/createFromTask'
        body = {
            "userId": user_id,
            "siteId": site_id
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body))

    def list_site_once_history(self, user_id="", site_id="", group_id=""):
        """
        :param user_id: User's identifier
        :type user_id: str
        :param site_id: Site identifier
        :type site_id: str
        :param group_id: group identifier
        :type group_id: str
        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        path = b'/site/once/groupTaskList'
        body = {
            "userId": user_id,
            "groupId": group_id,
            "siteId": site_id
        }
        return self._send_csm_request(http_methods.POST, path, body=json.dumps(body))

    def get_site_once_agent(self, user_id, ip_type="ipv4"):
        """
        :param user_id: User's identifier
        :type user_id: str
        :param ip_type: the type of ip, enum: ipv4, ipv6
        :type ip_type: str

        :return:
        :rtype: baidubce.bce_response.BceResponse
        """
        types = ["ipv4", "ipv6"]
        if ip_type is not None and ip_type not in types:
            raise ValueError('ip_type must be none or one of %s' % str(types))
        params = {
            b'userId': user_id,
            b'ipType': ip_type,
        }
        path = b'/site/once/siteAgent'
        return self._send_csm_request(http_methods.GET, path, params=params)

    @required(user_id=str, scope=str, region=str, resource_type=str, dimensions=list,
              metric_names=list, timestamp=str, statistics=list, cycle=int)
    def get_multi_dimension_latest_metrics(self, user_id, scope, region=None, resource_type=None, dimensions=None,
                                           metric_names=None, timestamp=None, statistics=None, cycle=None):
        """
        :param user_id: str
        :param scope: str
        :param region: str
        :param resource_type: str
        :param dimensions: list
        :param metric_names: list
        :param timestamp: str
        :param statistics: list
        :param cycle: int

        :return:
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(scope) <= 0:
            raise ValueError("scope should not be null")
        if metric_names is None:
            raise ValueError("metric_names should not be null")
        if len(dimensions) > MAX_INSTANCE_NUMBER:
            raise ValueError("dimensions size cannot more than " + MAX_INSTANCE_NUMBER)
        if cycle is None:
            cycle = 60
        body = {
            "userId": user_id,
            "scope": scope,
            "cycle": cycle
        }
        metric_names_req = []
        for res in metric_names:
            metric_names_req.append(res)
        body["metricNames"] = metric_names_req
        if region is not None:
            body["region"] = region
        if resource_type is not None:
            body["resourceType"] = resource_type
        if dimensions is not None:
            dimensions_res = []
            for res in dimensions:
                dimensions_res.append(res)
            body["dimensions"] = dimensions_res
        if timestamp is not None:
            body["timestamp"] = timestamp
        if statistics is not None:
            body["statistics"] = statistics
        user_id = compat.convert_to_bytes(user_id)
        scope = compat.convert_to_bytes(scope)
        path = b'/userId/%s/services/%s/data/metricData/latest/batch' % (user_id, scope)
        return self._send_csm_request(http_methods.POST, path, version=b'/v2', body=json.dumps(body))


    def get_metrics_by_partial_dimensions(self, user_id, scope, statistics, metric_name, start_time, end_time,
                                          region=None, resource_type=None, dimensions=None, cycle=None,
                                          pageNo=None, pageSize=None):
        """
        :param user_id: str
        :param scope: str
        :param statistics: list
        :param metric_name: str
        :param start_time: str
        :param end_time: str
        :param region: str
        :param resource_type: str
        :param dimensions: list
        :param cycle: int
        :param pageNo: int
        :param pageSize: int

        :return:
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(scope) <= 0:
            raise ValueError("scope should not be null")
        if len(metric_name) <= 0:
            raise ValueError("metric_name should not be null")
        if len(start_time) <= 0:
            raise ValueError("start_time should not be null")
        if len(end_time) <= 0:
            raise ValueError("end_time should not be null")
        if len(statistics) <= 0:
            raise ValueError("statistics should not be null")
        if len(dimensions) > MAX_INSTANCE_NUMBER:
            raise ValueError("dimensions size cannot more than " + MAX_INSTANCE_NUMBER)
        body = {
            "userId": user_id,
            "scope": scope,
            "startTime": start_time,
            "endTime": end_time,
            "statistics": statistics,
            "metricName": metric_name
        }
        if region is not None:
            body["region"] = region
        if resource_type is not None:
            body["resourceType"] = resource_type
        if dimensions is not None:
            dimensions_res = []
            for res in dimensions:
                dimensions_res.append(res)
            body["dimensions"] = dimensions_res
        if cycle is not None:
            body["cycle"] = cycle
        if pageNo is not None:
            body["pageNo"] = pageNo
        if pageSize is not None:
            body["pageSize"] = pageSize
        user_id = compat.convert_to_bytes(user_id)
        scope = compat.convert_to_bytes(scope)
        path = b'/userId/%s/services/%s/data/metricData/PartialDimension' % (user_id, scope)
        return self._send_csm_request(http_methods.POST, path, version=b'/v2', body=json.dumps(body))

    def get_all_data_metrics_v2(self, user_id, scope, region, dimensions, metric_names, statistics,
                                start_time, end_time, type="Instance", cycle=60):

        """
        :param user_id: user_id
        :type string

        :param scope: scope
        :type string

        :param region: region
        :type string

        :param type: resource type
        :type string

        :param dimensions: dimensions
        :type double string array

        :param metric_names: metric names
        :type  string array

        :param statistics: statistics
        :type  string array

        :param cycle: cycle
        :type  int

        :param start_time: start time
        :type  string

        :param end_time: end time
        :type  string
        :return:
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(scope) <= 0:
            raise ValueError("scope should not be null")
        if len(region) <= 0:
            raise ValueError("region should not be null")
        if metric_names is None:
            raise ValueError("metric_names should not be null")
        if dimensions is None:
            raise ValueError("dimensions should not be null")
        if statistics is None:
            raise ValueError("statistics should not be null")
        if len(dimensions) > MAX_INSTANCE_NUMBER:
            raise ValueError("dimensions size cannot more than " + MAX_INSTANCE_NUMBER)
        body = {
            "userId": user_id,
            "scope": scope,
            "cycle": cycle,
            "region": region,
            "startTime": start_time,
            "endTime": end_time,
            "metricNames": metric_names,
            "dimensions": dimensions,
            "statistics": statistics
        }
        if type is not None:
            body["type"] = type

        path = b'/data/metricAllData'
        return self._send_csm_request(http_methods.POST, path, version=b'/v2', body=json.dumps(body))

    def batch_get_all_data_metrics_v2(self, user_id, scope, region, dimensions, metric_names, statistics,
                                      start_time, end_time, type="Instance", cycle=60):

        """
        :param user_id: user_id
        :type string

        :param scope: scope
        :type string

        :param region: region
        :type string

        :param dimensions: dimensions
        :type double dimensional dict array

        :param metric_names: metric names
        :type  string array

        :param statistics: statistics
        :type  string array

        :param start_time: start time
        :type  string

        :param end_time: end time
        :type  string

        :param type: type
        :type string

        :param cycle: cycle
        :type  int
        :return:
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(scope) <= 0:
            raise ValueError("scope should not be null")
        if len(region) <= 0:
            raise ValueError("region should not be null")
        if len(metric_names) <= 0:
            raise ValueError("metric_names should not be null")
        if len(dimensions) <= 0:
            raise ValueError("dimensions should not be null")
        if len(statistics) <= 0:
            raise ValueError("statistics should not be null")
        if len(dimensions) > MAX_INSTANCE_NUMBER:
            raise ValueError("dimensions size cannot more than " + MAX_INSTANCE_NUMBER)
        body = {
            "userId": user_id,
            "scope": scope,
            "cycle": cycle,
            "region": region,
            "startTime": start_time,
            "endTime": end_time,
            "metricNames": metric_names,
            "dimensions": dimensions,
            "statistics": statistics
        }
        if type is not None:
            body["type"] = type

        path = b'/data/metricAllData/batch'
        return self._send_csm_request(http_methods.POST, path, version=b'/v2', body=json.dumps(body))


    def get_metric_dimension_top(self, user_id, scope, region, dimensions, metric_name, statistics, labels,
                                 start_time, end_time, order="top", topNum=10):

        """
        :param user_id: user_id
        :type string

        :param scope: scope
        :type string

        :param region: region
        :type string

        :param dimensions: dimensions
        :type map

        :param metric_name: metric_name
        :type string

        :param statistics: statistics
        :type string

        :param labels: labels
        :type set

        :param start_time: start_time
        :type string

        :param end_time: end_time
        :type string

        :param order: order default top
        :type string

        :param topNum: topNum default 10
        :type int

        :return:
        """
        if len(user_id) <= 0:
            raise ValueError("user_id should not be null")
        if len(scope) <= 0:
            raise ValueError("scope should not be null")
        if len(region) <= 0:
            raise ValueError("region should not be null")
        if len(metric_name) <= 0:
            raise ValueError("metric_name should not be null")
        if len(dimensions) <= 0:
            raise ValueError("dimensions should not be null")
        if len(labels) <= 0:
            raise ValueError("lables should not be null")
        if len(statistics) <= 0:
            raise ValueError("statistics should not be null")
        if len(start_time) <= 0:
            raise ValueError("start_time should not be null")
        if len(end_time) <= 0:
            raise ValueError("end_time should not be null")

        body = {
            "userId": user_id,
            "scope": scope,
            "region": region,
            "startTime": start_time,
            "endTime": end_time,
            "metricName": metric_name,
            "dimensions": dimensions,
            "statistics": statistics,
            "labels": labels,
            "order": order,
            "topNum": topNum,
        }

        path = b'/dimensions/top'
        return self._send_csm_request(http_methods.POST, path, version=b'/v2', body=json.dumps(body))


