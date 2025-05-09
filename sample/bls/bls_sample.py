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
import time

# !/usr/bin/env python
# coding=utf-8
from baidubce.exception import BceHttpClientError, BceServerError
import bls_sample_conf
from baidubce.services.bls.bls_client import BlsClient
from baidubce.services.bls.bls_model import LogRecordModel, TagModel

if __name__ == '__main__':

    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    log_store_name = "bls-test"
    log_stream_name = ""
    project = "BLS_Self"
    start_time = "2025-05-08T06:00:00Z"
    end_time = "2025-05-09T06:00:00Z"

    # create a bls client
    bls_client = BlsClient(bls_sample_conf.config)

    # query log data from bls interface
    try:
        response = bls_client.pull_log_records(log_store_name=log_store_name, log_stream_name=log_stream_name,
                                               start_time=start_time, end_time=end_time, project=project)

        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)

    try:
        now_ts = int(time.time() * 1000)
        log_records = [
            LogRecordModel(message="First log line", timestamp=now_ts),
            LogRecordModel(message="Second log line", timestamp=now_ts + 1)
        ]

        tags = [
            TagModel("env", "test"),
            TagModel("module", "logging")
        ]
        response = bls_client.push_log_records(log_store_name=log_store_name, log_stream_name=log_stream_name,
                                               log_records=log_records, tags=tags, project=project)

        print(response)
    except BceHttpClientError as e:
        if isinstance(e.last_error, BceServerError):
            __logger.error('send request failed. Response %s, code: %s, msg: %s'
                           % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            __logger.error('send request failed. Unknown exception: %s' % e)
