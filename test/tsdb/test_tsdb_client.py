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
Unit tests for tsdb client.
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

from baidubce.services.tsdb.tsdb_client import TsdbClient
import tsdb_test_config

class TestTsdbClient(unittest.TestCase):
    """
    Test class for tsdb sdk client
    """
    def setUp(self):
        self.tsdb_client = TsdbClient(tsdb_test_config.config)
        self.query_list = [{
            "metric": "cpu_idle",
            "field": "value",
            "filters": {
                "start": 1465376157006,
                "tags": {
                    "host": ["server1", "server2"]
                },
                "value": ">= 10"
            },
            "groupBy": [{
                "name": "Tag",
                "tags": ["rack"]
            }],
            "limit": 1000,
            "aggregators": [{
                "name": "Sum",
                "sampling": "10 minutes"
            }]    
        }]
        self.datapoints = [{
            "metric": "cpu_idle",
            "field": "field1",
            "tags": {
                "host": "server1",
                "rack": "rack1"
            },
            "timestamp": 1465376157007,
            "value": 51
            },
            {
            "metric": "cpu_idle",
            "field": "field2",
            "tags": {
                "host": "server2",
                "rack": "rack2"
            },
            "values": [
                [1465376269769, 67],
                [1465376325057, 60]
            ]
        },{
            "metric": "cpu_idle",
            "field": "value",
            "tags": {
                "host": "server1",
                "rack": "rack1"
            },
            "timestamp": 1465376157007,
            "value": 51
        }]
    def tearDown(self):
        print("ok")

    def test_write_datapoints(self):
        """
        test_write_datapoints
        """
        error = None
        try:
            response = self.tsdb_client.write_datapoints(self.datapoints)
            print(response)
        except BaseException as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_write_datapoints_no_gzip(self):
        """
        test_write_datapoints_no_gzip
        """
        error = None
        try:
            response = self.tsdb_client.write_datapoints(self.datapoints, False)
            print('test_write_datapoints_no_gzip', response)
        except BaseException as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_metrics(self):
        """
        test_get_metrics
        """
        error = None
        try:
            response = self.tsdb_client.get_metrics()
            print(response)
        except BaseException as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_fields(self):
        """
        test_get_fields
        """
        error = None
        try:
            response = self.tsdb_client.get_fields('cpu_idle')
            print(response)
        except BaseException as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_tags(self):
        """
        test_get_tags
        """
        error = None
        try:
            response = self.tsdb_client.get_tags('cpu_idle')
            print(response)
        except BaseException as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_get_datapoints(self):
        """
        test_get_datapoints
        """
        error = None
        try:
            response = self.tsdb_client.get_datapoints(self.query_list)
            print("test_get_datapoints", response)
        except BaseException as e:
            error = e
        finally:
            self.assertIsNone(error)
    
    def test_get_rows_with_sql(self):
        """
        test get rows with sql 
        """
        error = None
        try:
            statements = [
                "select timestamp from cpu_idle",
                "select value from cpu_idle",
                "select host from cpu_idle",
                "select timestamp,field1 from cpu_idle",
                "select * from cpu_idle",
                "select timestamp, value from cpu_idle order by timestamp ",
                "select timestamp, value from cpu_idle order by timestamp desc",
                '''select timestamp, value from cpu_idle
                    where value > 30 and timestamp >150937263000''',
                "select host, count(1) from cpu_idle group by host",
                '''select time_bucket(timestamp, '2 days') as DAY, sum(value) as SUM
                    from cpu_idle group by time_bucket(timestamp, '2 days')
                        order by time_bucket(timestamp, '2 days')''',
                "select timestamp, ((field2 - field1) * 10) as RESULT, host from cpu_idle",
                "select timestamp from cpu_idle",
                '''SELECT field1, CASE field1 WHEN 1 THEN 'one' WHEN 2 THEN 'two' ELSE 'many' END
                    FROM cpu_idle''',
                "SELECT field1, IF(field1>100,1,0) as result FROM cpu_idle",
                "SELECT field1, field2, COALESCE (field1, field2) as result FROM cpu_idle",
                "SELECT field1, abs (field1) as result FROM cpu_idle",
                "SELECT field1, sqrt (field1) as result FROM cpu_idle",
                "SELECT field1, cbrt (field1) as result FROM cpu_idle",
                "SELECT field1, ceil (field1) as result FROM cpu_idle",
                "SELECT field1, floor (field1) as result FROM cpu_idle",
                "SELECT 'str1' || 'str2' as result FROM cpu_idle",
                '''SELECT time_bucket(timestamp, '2 days') as DAY, avg(field1) as result 
                    FROM cpu_idle group by time_bucket(timestamp, '2 days')
                    order by time_bucket(timestamp, '2 days')''',
                ''' SELECT count(*) as result 
                    FROM cpu_idle where timestamp < 1525611901''',
                ''' SELECT time_bucket(timestamp, '2 days') as DAY, count(field1) as count 
                    FROM cpu_idle group by time_bucket(timestamp, '2 days')
                    order by time_bucket(timestamp, '2 days')''',
                '''SELECT max_by(field1,field2) as result 
                    FROM cpu_idle where timestamp < 1525611901000 ''',
                '''SELECT min_by(field1,field2) as result 
                    FROM cpu_idle where timestamp < 1525611901000	''',
                '''SELECT max(field1) as result 
                    FROM cpu_idle where timestamp < 1525611901000''',
                '''SELECT min(field1) as result 
                    FROM cpu_idle where timestamp < 1525611901000''',
                '''SELECT time_bucket(timestamp, '2 days') as DAY, sum(field1) as sum 
                    FROM cpu_idle group by time_bucket(timestamp, '2 days')
                    order by time_bucket(timestamp, '2 days')'''
            ]
            for statement in statements:
                response = self.tsdb_client.get_rows_with_sql(statement)
                print(statement, response)
        except BaseException as e:
            error = e
        finally:
            self.assertIsNone(error)
    
    def test_generate_pre_signed_url(self):
        """
        test_generate_pre_signed_url
        """
        error = None
        try:
            response = self.tsdb_client.generate_pre_signed_url(self.query_list)
            print(response)
        except BaseException as e:
            error = e
        finally:
            self.assertIsNone(error)

    def test_generate_pre_signed_url_with_sql(self):
        """
        test_generate_pre_signed_url_with_sql
        """

        error = None
        try:
            statement = "select timestamp from cpu_idle"
            response = self.tsdb_client.generate_pre_signed_url_with_sql(statement)
            print(response)
        except BaseException as e:
            error = e
        finally:
            self.assertIsNone(error)
        
if __name__ == "__main__":
    unittest.main()