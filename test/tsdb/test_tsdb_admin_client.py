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
Unit tests for tsdb admin client.
"""
import json
import os
import random
import string
import sys
import unittest

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

if sys.version_info[0] == 2 :
    reload(sys)
    sys.setdefaultencoding('utf-8')

from baidubce.services.tsdb.tsdb_admin_client import TsdbAdminClient
import tsdb_admin_test_config

class TestTsdbAdminClient(unittest.TestCase):
    """
    Test class for tsdb sdk client
    """
    def setUp(self):
        self.tsdb_admin_client = TsdbAdminClient(tsdb_admin_test_config.config)

    def tearDown(self):
        print("ok")

    def test_create_database(self):
        """
        test_create_database
        """
        error = None
        try:
            response = self.tsdb_admin_client.create_database(client_token=b'abttta',
                database_name=b'python43', description=b'pythonsdktest',
                ingest_datapoints_monthly=1, purchase_length=1,
                store_bytes_quota=0, coupon_name = b'xxxxxxx' )
            print(response)
        except BaseException as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_delete_database(self):
        """
        test_delete_database
        """
        error = None
        try:
            response = self.tsdb_admin_client.delete_database(b'tsdb-xxxxxxxx')
            print(response)
        except BaseException as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_database(self):
        """
        test_get_database
        """
        error = None
        try:
            response = self.tsdb_admin_client.get_database(b'tsdb-xxxxxxxxx')
            print(response)
        except BaseException as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_all_databases(self):
        """
        test_get_all_databases
        """
        error = None
        try:
            response = self.tsdb_admin_client.get_all_databases()
            print(response)
        except BaseException as e:
            error = e
        finally:
            self.assertIsNone(error)
if __name__ == "__main__":
    unittest.main()