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

from baidubce import bce_base_client, compat
from baidubce.auth import bce_v1_signer
from baidubce.http import handler, bce_http_client, http_methods
from baidubce.services.bls import bls_handler

if sys.version_info[0] == 2:
    value_type = (str, unicode)
else:
    value_type = (str, bytes)

MAX_BATCH_RECORD_NUMBER = 1000
DEFAULT_BATCH_RECORD_NUMBER = 100
DEFAULT_SORT = "desc"


class BlsClient(bce_base_client.BceBaseClient):
    """
    BLS base sdk client
    """

    log_prefix = b'/logstore'
    version = b'/v1'
    version_v2 = b'/v2'
    version_v3 = b'/v3'

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

    def _send_request(self, http_method, path, version=b'/v1',
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
            config, bce_v1_signer.sign, [bls_handler.parse_error, body_parser],
            http_method, version + BlsClient.log_prefix + path, body, headers, params)

    def pull_log_records(self, log_store_name, start_time, end_time, log_stream_name, project=None,
                         limit=None, marker=None, config=None):
        """
        Pull log records from specified log store.

        :param config:
        :param marker:
        :param limit:
        :param project:
        :param log_stream_name:
        :param log_store_name: The name of log store which will be pulled.
        :type log_store_name: string
        :param start_time: Start time of pulling log records.
        :type start_time: string
        :param end_time: End time of pulling log records.
        :type end_time: string
        :return: A list of log records.
        :rtype: list
        """
        log_store_name = compat.convert_to_bytes(log_store_name)
        path = b'/%s/logrecord' % log_store_name
        params = {b'startDateTime': start_time, b'endDateTime': end_time, b'logStreamName': log_stream_name}

        if project is not None:
            params[b'project'] = project
        if limit is None:
            params[b'limit'] = DEFAULT_BATCH_RECORD_NUMBER
        if limit is not None:
            if limit > MAX_BATCH_RECORD_NUMBER:
                limit = MAX_BATCH_RECORD_NUMBER
            params[b'limit'] = limit
        if marker is not None:
            params[b'marker'] = marker

        return self._send_request(http_methods.GET, path, params=params, config=config)

    def push_log_records(self, log_store_name, log_stream_name, log_records, project=None, type=None, tags=None,
                         config=None):
        """
        Push log records into the specified log stream in the given log store.

        :param log_store_name: The name of the log store which will receive the log records.
        :type log_store_name: str

        :param log_stream_name: The name of the log stream to write to.
        :type log_stream_name: str

        :param log_records: A list of log records to push.
                            Each record should be an instance of `LogRecordModel`.
                            Example:
                            [
                                LogRecordModel(message="test log", timestamp=1715231012000),
                                LogRecordModel(message="another log", timestamp=1715231044000)
                            ]
        :type log_records: List[LogRecordModel]

        :param project: (Optional) The project name to which the log store belongs.
        :type project: str or None

        :param type: (Optional) Type of logs, defaults to 'TEXT' if not specified.
        :type type: str or None

        :param tags: (Optional) A list of tags associated with the push.
                     Each tag should be an instance of `TagModel`.
                     Example:
                     [
                         TagModel("env", "prod"),
                         TagModel("service", "auth")
                     ]
        :type tags: List[TagModel] or None

        :param config: (Optional) Custom request config.
        :type config: baidubce.BceClientConfiguration or None

        :return: A dictionary containing the result of the push operation.
        :rtype: dict
        """
        log_store_name = compat.convert_to_bytes(log_store_name)
        path = b'/%s/logrecord' % log_store_name
        params = {}

        tags_list = [dict(tag) for tag in tags]
        type = type if type is not None else 'TEXT'
        records_payload = [dict(record) for record in log_records]
        if project is not None:
            params['project'] = project
        body = {
            "logStreamName": log_stream_name,
            "tags": tags_list,
            "type": type,
            "logRecords": records_payload
        }
        return self._send_request(http_methods.POST, path, params=params, body=json.dumps(body), config=config)

    def query_log_records(self, log_store_name, start_time, end_time, log_stream_name, project=None, query=None,
                          sort=None, limit=None, marker=None, config=None):
        """
        query log records from specified log store.

        :param sort: desc or asc
        :type sort: string
        :param query: query statement, eg: match *
        :type query: string
        :param config:
        :param marker:
        :param limit:
        :param project:
        :param log_stream_name:
        :param log_store_name: The name of log store which will be pulled.
        :type log_store_name: string
        :param start_time: Start time of pulling log records.
        :type start_time: string
        :param end_time: End time of pulling log records.
        :type end_time: string
        :return: A list of log records.
        :rtype: list
        """
        log_store_name = compat.convert_to_bytes(log_store_name)
        path = b'/%s/logrecord' % log_store_name
        params = {b'startDateTime': start_time, b'endDateTime': end_time, b'logStreamName': log_stream_name}

        if project is not None:
            params[b'project'] = project
        if limit is None:
            params[b'limit'] = DEFAULT_BATCH_RECORD_NUMBER
        if limit is not None:
            if limit > MAX_BATCH_RECORD_NUMBER:
                limit = MAX_BATCH_RECORD_NUMBER
            params[b'limit'] = limit
        if marker is not None:
            params[b'marker'] = marker

        if query is not None:
            params[b'query'] = query

        if sort is not None:
            if sort == 'asc':
                params[b'sort'] = sort
            else:
                params[b'sort'] = DEFAULT_SORT

        return self._send_request(http_methods.GET, path, params=params, config=config)

    def pull_log_records_v3(self, log_store_name, start_time, end_time, log_stream_name, project=None, query=None,
                            limit=None, marker=None, sort=None, config=None):
        """
        Pull log records v3 from specified log store.

        :param query: query statement, eg: match *
        :type query: string
        :param sort: desc or asc
        :type: sort: string
        :param config:
        :param marker:
        :param limit:
        :param project:
        :param log_stream_name:
        :param log_store_name: The name of log store which will be pulled.
        :type log_store_name: string
        :param start_time: Start time of pulling log records.
        :type start_time: string
        :param end_time: End time of pulling log records.
        :type end_time: string
        :return: A list of log records.
        :rtype: list
        """
        log_store_name = compat.convert_to_bytes(log_store_name)
        path = b'/%s/logrecord/pull' % log_store_name
        params = {b'startDateTime': start_time, b'endDateTime': end_time, b'logStreamName': log_stream_name}

        if project is not None:
            params[b'project'] = project
        if limit is None:
            params[b'limit'] = DEFAULT_BATCH_RECORD_NUMBER
        if limit is not None:
            if limit > MAX_BATCH_RECORD_NUMBER:
                limit = MAX_BATCH_RECORD_NUMBER
            params[b'limit'] = limit
        if marker is not None:
            params[b'marker'] = marker
        if sort is not None:
            if sort == 'asc':
                params[b'sort'] = sort
            else:
                params[b'sort'] = DEFAULT_SORT
        if query is not None:
            params[b'query'] = query

        return self._send_request(http_methods.GET, path, version=self.version_v3, params=params, config=config)
