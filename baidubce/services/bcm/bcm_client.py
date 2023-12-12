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
import uuid

from baidubce import bce_base_client, utils, compat
from baidubce.auth import bce_v1_signer
from baidubce.http import handler, bce_http_client, http_methods
from baidubce.services.bcm import bcm_model, bcm_handler


class BcmClient(bce_base_client.BceBaseClient):
    """
    BCM base sdk client
    """

    prefix = b'/json-api'
    csm_prefix = b'/csm/api'
    version = b'/v1'

    content_type_header_key = b"content-type"
    content_type_header_value = b"application/json;charset=utf-8"
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
                compat.convert_to_bytes(namespace), compat.convert_to_bytes(metric_name)))
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
                compat.convert_to_bytes(namespace), compat.convert_to_bytes(metric_name)))
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
