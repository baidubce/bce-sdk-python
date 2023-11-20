# coding=utf-8
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
This module defines some Argument classes for BTS
"""


class CreateInstanceArgs(object):
    """
    Create Instance Args
    :param storage_type  instance's storage type. eg.CommonPerformance
    :type storage_type string
    """
    def __init__(self, storage_type=None):
        self.storage_type = storage_type


def create_instance_args_2_dict(args):
    """
    change create_instance_args to dict

    :param args: create instance args
    :type args: CreateInstanceArgs

    :return:
    :rtype dict
    """
    return {
        'storageType': args.storage_type
    }


class CreateTableArgs(object):
    """
    Create Table Args
    :param table_version  table's version
    :type table_version int64
    :param compress_type  table's compress type. eg.SNAPPY_ALL
    :type compress_type string
    :param ttl  time to live
    :type ttl int
    :param storage_type  instance's storage type. eg.CommonPerformance
    :type storage_type string
    :param max_versions  table's max data versions.
    :type max_versions int
    """
    def __init__(self, table_version=0, compress_type=None, ttl=0, storage_type=None, max_versions=1):
        self.table_version = table_version
        self.compress_type = compress_type
        self.ttl = ttl
        self.storage_type = storage_type
        self.max_versions = max_versions


def create_table_args_2_dict(args):
    """
    change create_table_args to dict

    :param args: create table args
    :type args: CreateTableArgs

    :return:
    :rtype dict
    """
    return {
        'tableVersion': args.table_version,
        'compressType': args.compress_type,
        'ttl': args.ttl,
        'storageType': args.storage_type,
        'maxVersions': args.max_versions
    }


class UpdateTableArgs(object):
    """
    Update Table Args
    :param table_version  table's version
    :type table_version int64
    :param compress_type  table's compress type. eg.SNAPPY_ALL
    :type compress_type string
    :param ttl time to live
    :type ttl int
    :param max_versions  table's max data versions.
    :type max_versions int
    """
    # 不能将table_version初始化为None，否则后端会认为是创建表
    def __init__(self, table_version=1, compress_type=None, ttl=None, max_versions=None):
        self.table_version = table_version
        self.compress_type = compress_type
        self.ttl = ttl
        self.max_versions = max_versions


def update_table_args_2_dict(args):
    """
    change update_table_args to dict

    :param args: update table args
    :type args: UpdateTableArgs

    :return:
    :rtype dict
    """
    return {
        'tableVersion': args.table_version,
        'compressType': args.compress_type,
        'ttl': args.ttl,
        'maxVersions': args.max_versions
    }


class Cell(object):
    """
    Cell
    :param column
    :type column string
    :param value
    :type value string
    """
    def __init__(self, column="", value=""):
        self.column = column
        self.value = value

    def to_dict(self):
        """
        Convert the Cell instance into a dictionary with keys for column and value.

        :return: A dictionary with 'column' and 'value' as keys, representing
                 the cell's data.
        :rtype: dict
        """
        return {
            'column': self.column,
            'value': self.value
        }


class Row(object):
    """
    Row
    :param rowkey
    :type rowkey string
    :param cells
    :type cells []
    """
    def __init__(self, rowkey=""):
        self.rowkey = rowkey
        self.cells = []

    def append_cell(self, cell):
        """
        append cell

        :param cell: column & value
        :type cell: Cell

        :return:
        :rtype
        """
        self.cells.append(cell)

    def get_cell(self):
        """
        get cell

        :return cells:
        :rtype Cell[]
        """
        return self.cells

    def to_dict(self):
        """
        Convert the Row instance into a dictionary suitable for serialization.

        :return: A dictionary with 'rowkey' as the unique identifier and 'cells'
                 containing a list of cell data in dictionary form.
        :rtype: dict
        """
        cells = []
        for cell in self.cells:
            if isinstance(cell, Cell):
                cells.append(cell.to_dict())
            elif isinstance(cell, dict):
                cells.append(cell)
        return {
            'rowkey': self.rowkey,
            'cells': cells
        }


class BatchPutRowArgs(object):
    """
    Batch Put Row Args
    :param rows
    :type rows []
    """
    def __init__(self):
        self.rows = []

    def append_row(self, row):
        """
        append row

        :param row:
        :type row: Row

        :return:
        :rtype
        """
        self.rows.append(row)

    def get_row(self):
        """
        get row

        :return rows:
        :rtype Row[]
        """
        return self.rows


class QueryCell(object):
    """
    Query Cell
    :param column
    :type column string
    """
    def __init__(self, column=""):
        self.column = column

    def to_dict(self):
        """
        Convert the QueryCell instance into a dictionary

        :return: A dictionary representation of the QueryCell, with 'column' as the key.
        :rtype: dict
        """
        return {
            'column': self.column,
        }

class QueryRowArgs(object):
    """
    Query Row Arg
    :param rowkey
    :type rowkey string
    :param max_versions
    :type max_versions int
    :param cells
    :type cells []
    """
    def __init__(self, rowkey="", max_versions=0):
        self.rowkey = rowkey
        self.max_versions = max_versions
        self.cells = []

    def append_cell(self, cell):
        """
        append cell

        :param cell: column & value
        :type cell: Cell

        :return:
        :rtype
        """
        self.cells.append(cell)

    def get_cell(self):
        """
        get cell

        :return cells:
        :rtype Cell[]
        """
        return self.cells

    def to_dict(self):
        """
        Convert the QueryRowArgs instance into a dictionary suitable for serialization.

        :return: A dictionary representation of the QueryRowArgs, including the rowkey and cells.
        :rtype: dict
        """
        cells_dict = [cell.to_dict() if hasattr(cell, 'to_dict') else cell for cell in self.cells]
        return {
            'rowkey': self.rowkey,
            'cells': cells_dict,
        }


def query_row_args_2_dict(args):
    """
    change query_row_args to dict

    :param args: query row args
    :type args: QueryRowArgs

    :return:
    :rtype dict
    """
    return {
        'rowkey': args.rowkey,
        'maxVersions': args.max_versions,
        'cells': args.cells
    }


class BatchQueryRowArgs(object):
    """
    Batch Query Row Args
    :param rows
    :type rows []
    :param max_versions
    :type max_versions int
    """
    def __init__(self, max_versions=0):
        self.rows = []
        self.max_versions = max_versions

    def append_row(self, row):
        """
        append row

        :param row:
        :type row: Row

        :return:
        :rtype
        """
        self.rows.append(row)

    def get_rows(self):
        """
        get row

        :return rows:
        :rtype Row[]
        """
        return self.rows

    def to_dict(self):
        """
        Convert the BatchQueryRowArgs instance to a dictionary for JSON serialization.

        :return: A dictionary representation of the BatchQueryRowArgs instance with
                'rows' key containing a list of rows and 'max_versions' key
                containing the maximum number of versions.
        :rtype: dict
        """
        rows_data = []
        for row_arg in self.rows:
            if isinstance(row_arg, QueryRowArgs):
                # Assuming QueryRowArgs has a to_dict method
                row_data = row_arg.to_dict()
            elif isinstance(row_arg, dict):
                row_data = row_arg
            rows_data.append(row_data)
        return {
            'rows': rows_data,
            'max_versions': self.max_versions
        }


def batch_query_row_args_2_dict(args):
    """
    change batch_query_row_args to dict

    :param args: batch query row args
    :type args: BatchQueryRowArgs

    :return:
    :rtype dict
    """
    return {
        'maxVersions': args.max_versions,
        'rows': args.rows
    }


class ScanArgs(object):
    """
    Scan Args
    :param start_rowkey
    :type start_rowkey string
    :param include_start
    :type include_start bool
    :param stop_rowkey
    :type stop_rowkey string
    :param include_stop
    :type include_stop bool
    :param limit
    :type limit int
    :param max_versions
    :type max_versions int
    :param selector
    :type selector []
    """
    def __init__(self, start_rowkey="", include_start=True, stop_rowkey="",
                 include_stop=False, limit=0, max_versions=0):
        self.start_rowkey = start_rowkey
        self.include_start = include_start
        self.stop_rowkey = stop_rowkey
        self.include_stop = include_stop
        self.limit = limit
        self.max_versions = max_versions
        self.selector = []

    def append_selector(self, query_cell):
        """
        append selector

        :param query_cell:
        :type query_cell: QueryCell

        :return:
        :rtype
        """
        self.selector.append(query_cell)

    def get_selector(self):
        """
        get selector

        :return selector:
        :rtype query_cell[]
        """
        return self.selector

    def to_dict(self):
        """
        Convert the ScanArgs instance into a dictionary

        :return: A dictionary representation of the scan arguments.
        :rtype: dict
        """
        selector = []
        for item in self.selector:
            if isinstance(item, QueryCell):
                selector.append({'column': item.column})
            elif isinstance(item, dict):
                selector.append(item)

        return {
            'startRowkey': self.start_rowkey,
            'includeStart': self.include_start,
            'stopRowkey': self.stop_rowkey,
            'includeStop': self.include_stop,
            'selector': selector,
            'maxVersions': self.max_versions,
            'limit': self.limit
        }


def scan_args_2_dict(args):
    """
    change scan_args to dict

    :param args: scan row args
    :type args: ScanArgs

    :return:
    :rtype dict
    """
    return {
        'startRowkey': args.start_rowkey,
        'includeStart': args.include_start,
        'stopRowkey': args.stop_rowkey,
        'includeStop': args.include_stop,
        'selector': args.selector,
        'limit': args.limit,
        'maxVersions': args.max_versions
    }

