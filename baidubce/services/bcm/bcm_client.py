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


class BcmClient(bce_base_client.BceBaseClient):
    """
    BCM base sdk client
    """

    prefix = b'/json-api'
    csm_prefix = b'/csm/api'
    version = b'/v1'

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

    def _send_csm_request(self, http_method, path,
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
            http_method, BcmClient.csm_prefix + BcmClient.version + path, body, headers, params)

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
