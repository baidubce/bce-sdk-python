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
Unit tests for bls client.
"""
import sys
import time
import unittest

import baidubce
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.bls import bls_client
from baidubce.services.bls.bls_model import LogRecordModel, TagModel

PY2 = sys.version_info[0] == 2
if PY2:
    reload(sys)
    sys.setdefaultencoding('utf8')

HOST = b'bls-log.bj.baidubce.com'
AK = b'your ak'
SK = b'your sk'

log_store_name = "bls-test"
log_stream_name = ""
project = "BLS_Self"
start_time = "2025-05-08T06:00:00Z"
end_time = "2025-05-09T06:00:00Z"


class TestBcmClient(unittest.TestCase):
    """
    Test class for bls sdk client
    """

    def setUp(self):
        config = BceClientConfiguration(credentials=BceCredentials(AK, SK),
                                        endpoint=HOST)
        self.client = bls_client.BlsClient(config)

    def test_pull_log_records(self):
        """
        test get log data
        """
        response = self.client.pull_log_records(log_store_name=log_store_name, log_stream_name=log_stream_name,
                                                start_time=start_time, end_time=end_time, project=project)

        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)

    def test_push_log_records(self):
        """
        test put log data
        """
        now_ts = int(time.time() * 1000)
        log_records = [
            LogRecordModel(message="First log line", timestamp=now_ts),
            LogRecordModel(message="Second log line", timestamp=now_ts + 1)
        ]

        tags = [
            TagModel("env", "test"),
            TagModel("module", "logging")
        ]
        response = self.client.push_log_records(log_store_name=log_store_name, log_stream_name=log_stream_name,
                                                log_records=log_records, tags=tags, project=project)
        self.assertEqual(type(response), baidubce.bce_response.BceResponse)
        print(response)