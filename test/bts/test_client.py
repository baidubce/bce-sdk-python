#!/usr/bin/env python
#coding=utf8

# Copyright 2014 Baidu, Inc.
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
Test models of BTS.
"""

import unittest
import os
import sys
import json

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    import unittest.mock as mock
else:
    import mock as mock

from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.services.bts import bts_client as bts
from baidubce.services.bts.model import BatchPutRowArgs
from baidubce.services.bts.model import BatchQueryRowArgs
from baidubce.services.bts.model import Cell
from baidubce.services.bts.model import CreateInstanceArgs
from baidubce.services.bts.model import CreateTableArgs
from baidubce.services.bts.model import QueryCell
from baidubce.services.bts.model import QueryRowArgs
from baidubce.services.bts.model import Row
from baidubce.services.bts.model import ScanArgs
from baidubce.services.bts.model import UpdateTableArgs


class MockHttpResponse(object):
    """
    Mock HttpResponse
    """

    def __init__(self, status, result=None, header_list=None):
        self.status = status
        self.result = result
        self.header_list = header_list

    def read(self):
        """
        mock HttpResponse.read()

        :return: self.content
        """
        return self.result

    def getheaders(self):
        """
        mock HttpResponse.getheaders()

        :return: self.header_list
        """
        return self.header_list

    def close(self):
        """
        mock HttpResponse.close()
        """
        return


class TestBtsClient(unittest.TestCase):
    """
    Test class for bts client
    """
    def setUp(self):
        HOST = 'host'
        AK = 'ak'
        SK = 'sk'
        config = BceClientConfiguration(
            credentials=BceCredentials(AK, SK),
            endpoint=HOST
        )
        self.bts_client = bts.BtsClient(config)

    def test_create_instance(self):
        """
        test case for create_instance
        """
        mock_http_response = MockHttpResponse(
            200,
            result=json.dumps({}),
            header_list=[
                ('x-bce-request-id', '7869616F-7A68-6977-656E-406261696475'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
        send_http_request = mock.Mock(return_value=mock_http_response)
        self.bts_client._send_request = send_http_request

        instance_name = b"ins01"
        create_instance_args = CreateInstanceArgs('CommonPerformance')
        res = self.bts_client.create_instance(instance_name, create_instance_args)

        self.assertEqual(res.status, 200)

    def test_drop_instance(self):
        """
        test case for drop_instance
        """
        mock_http_response = MockHttpResponse(
            200,
            result=json.dumps({}),
            header_list=[
                ('x-bce-request-id', '7869616F-7A68-6977-656E-406261696475'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
        send_http_request = mock.Mock(return_value=mock_http_response)
        self.bts_client._send_request = send_http_request

        res = self.bts_client.drop_instance(b"ins02")
        self.assertEqual(res.status, 200)

    def test_list_instances(self):
        """
        test case for list_instances
        """
        res_body = {
            "instances": [
                {
                    "id": "btsi-123456789",
                    "name": "ins1",
                    "region": "bd",
                    "state": "Normal",
                    "createTime": "2018-05-06T14:32:09Z",
                    "storageType": "HighPerformance"
                },
                {
                    "id": "btsi-345678932",
                    "name": "ins2",
                    "region": "bd",
                    "state": "Normal",
                    "createTime": "2018-05-06T14:32:09Z",
                    "storageType": "CommonPerformance"
                }
            ]
        }
        mock_http_response = MockHttpResponse(
            200,
            result=json.dumps(res_body),
            header_list=[
                ('x-bce-request-id', '7869616F-7A68-6977-656E-406261696475'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
        send_http_request = mock.Mock(return_value=mock_http_response)
        self.bts_client._send_request = send_http_request

        res = self.bts_client.list_instances()
        self.assertEqual(res.status, 200)

    def test_show_instance(self):
        """
        test case for show_instance
        """
        res_body = {
            "id": "btsi-123456789",
            "name": "ins1",
            "region": "bd",
            "state": "Normal",
            "createTime": "2018-05-06T11:22:33Z",
            "storageType": "HighPerformance"
        }
        mock_http_response = MockHttpResponse(
            200,
            result=json.dumps(res_body),
            header_list=[
                ('x-bce-request-id', '7869616F-7A68-6977-656E-406261696475'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
        send_http_request = mock.Mock(return_value=mock_http_response)
        self.bts_client._send_request = send_http_request

        res = self.bts_client.show_instance(b"ins01")
        self.assertEqual(res.status, 200)

    def test_create_table(self):
        """
        test case for create_table
        """
        mock_http_response = MockHttpResponse(
            200,
            result=json.dumps({}),
            header_list=[
                ('x-bce-request-id', '7869616F-7A68-6977-656E-406261696475'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
        send_http_request = mock.Mock(return_value=mock_http_response)
        self.bts_client._send_request = send_http_request

        instance_name = b"ins01"
        table_name = b"tab01"
        create_table_args = CreateTableArgs()
        create_table_args.table_version = 0
        create_table_args.compress_type = "SNAPPY_ALL"
        create_table_args.ttl = 0
        create_table_args.storage_type = "CommonPerformance"
        create_table_args.max_versions = 10
        res = self.bts_client.create_table(instance_name, table_name, create_table_args)
        self.assertEqual(res.status, 200)

    def test_update_table(self):
        """
        test case for update_table
        """
        mock_http_response = MockHttpResponse(
            200,
            result=json.dumps({}),
            header_list=[
                ('x-bce-request-id', '7869616F-7A68-6977-656E-406261696475'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
        send_http_request = mock.Mock(return_value=mock_http_response)
        self.bts_client._send_request = send_http_request

        instance_name = b"ins01"
        table_name = b"tab01"
        update_table_args = UpdateTableArgs()
        update_table_args.table_version = "1534587498000000"
        update_table_args.compress_type = "NONE"
        update_table_args.max_versions = 20
        update_table_args.ttl = 86400
        res = self.bts_client.update_table(instance_name, table_name, update_table_args)
        self.assertEqual(res.status, 200)

    def test_drop_table(self):
        """
        test case for drop_table
        """
        mock_http_response = MockHttpResponse(
            200,
            result=json.dumps({}),
            header_list=[
                ('x-bce-request-id', '7869616F-7A68-6977-656E-406261696475'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
        send_http_request = mock.Mock(return_value=mock_http_response)
        self.bts_client._send_request = send_http_request

        instance_name = b'ins01'
        table_name = b'tab01'
        res = self.bts_client.drop_table(instance_name, table_name)
        self.assertEqual(res.status, 200)

    def test_show_table(self):
        """
        test case for show_table
        """
        res_body = {
            "instance": "ins01",
            "tableName": "tab01",
            "tableState": "Normal",
            "tableVersion": 1531308455483091,
            "createTime": "2018-05-06T14:32:09Z",
            "compressType": "NONE",
            "ttl": 0,
            "maxVersions": 1
        }
        mock_http_response = MockHttpResponse(
            200,
            result=json.dumps(res_body),
            header_list=[
                ('x-bce-request-id', '7869616F-7A68-6977-656E-406261696475'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
        send_http_request = mock.Mock(return_value=mock_http_response)
        self.bts_client._send_request = send_http_request

        res = self.bts_client.show_table(b'ins01', b'tab01')
        self.assertEqual(res.status, 200)

    def test_list_tables(self):
        """
        test case for list_tables
        """
        res_body = {
            "tables": [
                {
                    "tableName": "tab01",
                    "tableState": "Normal",
                    "tableVersion": 1562345678,
                    "maxVersions": 1
                },
                {
                    "tableName": "tab02",
                    "tableState": "Creating",
                    "tableVersion": 1562345678,
                    "maxVersions": 1
                }
            ]
        }
        mock_http_response = MockHttpResponse(
            200,
            result=json.dumps(res_body),
            header_list=[
                ('x-bce-request-id', '7869616F-7A68-6977-656E-406261696475'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
        send_http_request = mock.Mock(return_value=mock_http_response)
        self.bts_client._send_request = send_http_request

        res = self.bts_client.list_tables(b'ins01')
        self.assertEqual(res.status, 200)

    def test_put_row(self):
        """
        test case for put_row
        """
        mock_http_response = MockHttpResponse(
            200,
            result=json.dumps({}),
            header_list=[
                ('x-bce-request-id', '7869616F-7A68-6977-656E-406261696475'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
        send_http_request = mock.Mock(return_value=mock_http_response)
        self.bts_client._send_request = send_http_request

        instance_name = b'ins01'
        table_name = b'tab01'
        # First way: using dict value
        row = Row()
        row.rowkey = "row01"
        cell1 = TestCell("c1", "v1")
        cell2 = TestCell("c2", "v2")
        cells = [cell1.__dict__, cell2.__dict__]
        row.cells = cells
        res = self.bts_client.put_row(instance_name, table_name, row)
        self.assertEqual(res.status, 200)

        row = Row()
        row.rowkey = "row01"
        cell1 = Cell("c1", "v1")
        cell2 = Cell("c2", "v2")

        # Second way: use object
        row.cells.append(cell1)
        row.cells.append(cell2)
        res = self.bts_client.put_row(instance_name, table_name, row)
        self.assertEqual(res.status, 200)

    def test_batch_put_row(self):
        """
        test case for batch_put_row
        """
        mock_http_response = MockHttpResponse(
            200,
            result=json.dumps({}),
            header_list=[
                ('x-bce-request-id', '7869616F-7A68-6977-656E-406261696475'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
        send_http_request = mock.Mock(return_value=mock_http_response)
        self.bts_client._send_request = send_http_request

        instance_name = b'ins01'
        table_name = b'tab01'
        # First way: using dict value
        batch_put_row = BatchPutRowArgs()
        for i in range(2, 15):
            row = Row()
            row.rowkey = "row" + str(i)
            for j in range(3):
                col = "c" + str(j)
                val = "v" + str(j)
                cell = TestCell(col, val)
                row.cells.append(cell.__dict__)
            batch_put_row.rows.append(row.__dict__)
        res = self.bts_client.batch_put_row(instance_name, table_name, batch_put_row)
        self.assertEqual(res.status, 200)

        # Second way: use object
        batch_put_row = BatchPutRowArgs()
        for i in range(2, 15):
            row = Row()
            row.rowkey = "row" + str(i)
            for j in range(3):
                col = "c" + str(j)
                val = "v" + str(j)
                cell = Cell(col, val)
                row.cells.append(cell)
            batch_put_row.rows.append(row)
        res = self.bts_client.batch_put_row(instance_name, table_name, batch_put_row)
        self.assertEqual(res.status, 200)

    def test_delete_row(self):
        """
        test case for delete_row
        """
        mock_http_response = MockHttpResponse(
            200,
            result=json.dumps({}),
            header_list=[
                ('x-bce-request-id', '7869616F-7A68-6977-656E-406261696475'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
        send_http_request = mock.Mock(return_value=mock_http_response)
        self.bts_client._send_request = send_http_request

        instance_name = b'ins01'
        table_name = b'tab01'
        query_row_args = QueryRowArgs()
        query_row_args.rowkey = "row011"
        cell1 = QueryCell()
        cell1.column = "c1"

        # First way: using dict value
        query_row_args.cells.append(cell1.__dict__)
        res = self.bts_client.delete_row(instance_name, table_name, query_row_args)
        self.assertEqual(res.status, 200)

        # Reset cells for next test
        query_row_args.cells = []

        # Second way: use object
        query_row_args.cells.append(cell1)
        res = self.bts_client.delete_row(instance_name, table_name, query_row_args)
        self.assertEqual(res.status, 200)

    def test_batch_delete_row(self):
        """
        test case for batch_delete_row
        """
        mock_http_response = MockHttpResponse(
            200,
            result=json.dumps({}),
            header_list=[
                ('x-bce-request-id', '7869616F-7A68-6977-656E-406261696475'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
        send_http_request = mock.Mock(return_value=mock_http_response)
        self.bts_client._send_request = send_http_request

        instance_name = b'ins01'
        table_name = b'tab01'
        batch_query_row_args = BatchQueryRowArgs()
        batch_query_row_args.max_version = 2

        # First way: using dict value
        query_row_args1 = QueryRowArgs()
        query_row_args1.rowkey = "row8"
        query_row_args1.cells.append(QueryCell("c0").__dict__)
        query_row_args1.cells.append(QueryCell("c1").__dict__)
        batch_query_row_args.rows.append(query_row_args1)

        # Second way: use object
        query_row_args2 = QueryRowArgs()
        query_row_args2.rowkey = "row9"
        query_row_args2.cells.append(QueryCell("c1"))
        query_row_args2.cells.append(QueryCell("c2"))
        batch_query_row_args.rows.append(query_row_args2)

        # Perform the batch delete operation
        res = self.bts_client.batch_delete_row(instance_name, table_name, batch_query_row_args)
        self.assertEqual(res.status, 200)

    def test_get_row(self):
        """
        test case for get_row
        """
        res_body = {
            "result": [
                {
                    "rowkey": "row1",
                    "cells": [
                        {
                            "column": "c1",
                            "value": "v1",
                            "timestamp": 1571049818321
                        },
                        {
                            "column": "c2",
                            "value": "v2",
                            "timestamp": 1571049818321
                        }
                    ]
                }
            ]
        }

        res = Results()
        row1 = Row("row1")
        cell1 = TestCell("c1", "v1_1", 1571049818321)
        cell2 = TestCell("c2", "v2_1", 1571049818321)
        row1.cells.append(cell1)
        row1.cells.append(cell2)
        res.result.append(row1)

        mock_http_response = MockHttpResponse(
            200,
            result=res.result,
            header_list=[
                ('x-bce-request-id', '7869616F-7A68-6977-656E-406261696475'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
        send_http_request = mock.Mock(return_value=mock_http_response)
        self.bts_client._send_request = send_http_request

        instance_name = b'ins01'
        table_name = b'tab01'
        # First way: using dict value
        query_row_args = QueryRowArgs()
        query_row_args.rowkey = "row1"
        query_row_args.cells.append(QueryCell("c1").__dict__)
        query_row_args.cells.append(QueryCell("c2").__dict__)
        query_row_args.max_versions = 2
        res1 = self.bts_client.get_row(instance_name, table_name, query_row_args)
        self.assertEqual(res1.status, 200)

        # Second way: use object
        query_row_args = QueryRowArgs()
        query_row_args.rowkey = "row1"
        query_row_args.cells.append(QueryCell("c1"))
        query_row_args.cells.append(QueryCell("c2"))
        query_row_args.max_versions = 2
        res2 = self.bts_client.get_row(instance_name, table_name, query_row_args)
        self.assertEqual(res2.status, 200)

    def test_batch_get_row(self):
        """
        test case for batch_get_row
        """
        res_body = {
            "result": [
                {
                    "rowkey": "row1",
                    "cells": [
                        {
                            "column": "c1",
                            "value": "v1",
                            "timestamp": 1571049818321
                        },
                        {
                            "column": "c2",
                            "value": "v2",
                            "timestamp": 1571049818321
                        }
                    ]
                },
                {
                    "rowkey": "row2",
                    "cells": [
                        {
                            "column": "c3",
                            "value": "v3",
                            "timestamp": 1571049818321
                        },
                        {
                            "column": "c4",
                            "value": "v4",
                            "timestamp": 1571049818321
                        }
                    ]
                }
            ]
        }

        res = Results()
        row1 = Row("row1")
        cell1 = TestCell("c1", "v1_1", 1571049818321)
        cell2 = TestCell("c2", "v2_1", 1571049818321)
        row1.cells.append(cell1)
        row1.cells.append(cell2)
        res.result.append(row1)

        row2 = Row("row2")
        cell3 = TestCell("c3", "v3_1", 1571049818321)
        row2.cells.append(cell3)
        cell4 = TestCell("c4", "v4_1", 1571049818321)
        row2.cells.append(cell4)
        res.result.append(row2)

        mock_http_response = MockHttpResponse(
            200,
            result=res.result,
            header_list=[
                ('x-bce-request-id', '7869616F-7A68-6977-656E-406261696475'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
        send_http_request = mock.Mock(return_value=mock_http_response)
        self.bts_client._send_request = send_http_request

        instance_name = b'ins01'
        table_name = b'tab01'
        batch_query_row_args1 = BatchQueryRowArgs()
        batch_query_row_args1.max_versions = 2
        # First way: using a dictionary
        query_row_args1 = QueryRowArgs()
        query_row_args1.rowkey = "row1"
        query_row_args1.cells.append(QueryCell("c1").__dict__)
        query_row_args1.cells.append(QueryCell("c2").__dict__)
        batch_query_row_args1.rows.append(query_row_args1.__dict__)
        # Second way: use object
        query_row_args2 = QueryRowArgs()
        query_row_args2.rowkey = "row2"
        query_row_args2.cells.append(QueryCell("c1").__dict__)
        query_row_args2.cells.append(QueryCell("c2").__dict__)
        batch_query_row_args1.rows.append(query_row_args2.__dict__)
        res1 = self.bts_client.batch_get_row(instance_name, table_name, batch_query_row_args1)
        self.assertEqual(res1.status, 200)

        batch_query_row_args2 = BatchQueryRowArgs()
        batch_query_row_args2.max_versions = 2
        for row_key in ["row1", "row2"]:
            query_row_args = QueryRowArgs()
            query_row_args.rowkey = row_key
            query_row_args.cells.append(QueryCell("c1"))
            query_row_args.cells.append(QueryCell("c2"))
            batch_query_row_args2.rows.append(query_row_args)

        res2 = self.bts_client.batch_get_row(instance_name, table_name, batch_query_row_args2)
        self.assertEqual(res2.status, 200)

    def test_scan(self,):
        """
        test case for scan
        """
        res_body = {
            "result": [
                {
                    "rowkey": "row1",
                    "cells": [
                        {
                            "column": "c1",
                            "value": "v1",
                            "timestamp": 1571049818321
                        },
                        {
                            "column": "c2",
                            "value": "v2",
                            "timestamp": 1571049818321
                        }
                    ]
                },
                {
                    "rowkey": "row2",
                    "cells": [
                        {
                            "column": "c2",
                            "value": "v2",
                            "timestamp": 1571049818321
                        }
                    ]
                }
            ]
        }

        res = Results()
        row1 = Row("row1")
        cell1 = TestCell("c1", "v1_1", 1571049818321)
        cell2 = TestCell("c2", "v2_1", 1571049818321)
        row1.cells.append(cell1)
        row1.cells.append(cell2)
        res.result.append(row1)

        row2 = Row("row2")
        cell3 = TestCell("c2", "v2_1", 1571049818321)
        row2.cells.append(cell3)
        res.result.append(row2)


        mock_http_response = MockHttpResponse(
            200,
            result=res.result,
            header_list=[
                ('x-bce-request-id', '7869616F-7A68-6977-656E-406261696475'),
                ('content-type', 'application/json;charset=UTF-8')
            ])
        send_http_request = mock.Mock(return_value=mock_http_response)
        self.bts_client._send_request = send_http_request

        instance_name = b"ins01"
        table_name = b"tab01"
        # First way: using a dictionary
        scan_args = ScanArgs()
        scan_args.start_rowkey = "row1"
        scan_args.include_start = "true"
        scan_args.stop_rowkey = "row2"
        scan_args.include_stop = "true"
        scan_args.selector.append(QueryCell("c1").__dict__)
        scan_args.selector.append(QueryCell("c2").__dict__)
        scan_args.max_versions = 1
        scan_args.limit = 20
        res1 = self.bts_client.scan(instance_name, table_name, scan_args)
        self.assertEqual(res1.status, 200)

        # Second way: using object
        scan_args_obj = ScanArgs()
        scan_args_obj.start_rowkey = "row1"
        scan_args_obj.include_start = True  # This should be a boolean, not a string
        scan_args_obj.stop_rowkey = "row2"
        scan_args_obj.include_stop = True  # This should be a boolean, not a string
        scan_args_obj.selector.append(QueryCell("c1"))  # Assuming QueryCell has a proper initializer
        scan_args_obj.selector.append(QueryCell("c2"))  # Assuming QueryCell has a proper initializer
        scan_args_obj.max_versions = 1
        scan_args_obj.limit = 20
        res2 = self.bts_client.scan(instance_name, table_name, scan_args_obj)
        self.assertEqual(res2.status, 200)


class TestCell(object):
    """
    Cell
    :param column
    :type column string
    :param value
    :type value string
    """
    def __init__(self, column="", value="", timestamp=0):
        self.column = column
        self.value = value
        self.timestamp = timestamp


class Result(object):
    """
    Result
    :param rowkey
    :type rowkey string
    :param cells
    :type cells []
    """
    def __init__(self, rowkey=""):
        self.rowkey = rowkey
        self.cells = []


class Results(object):
    """
    ScanResult
    :param result
    :type result []
    """

    def __init__(self):
        self.result = []


if __name__ == '__main__':
    unittest.main()

