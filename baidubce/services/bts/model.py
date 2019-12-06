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
    def __init__(self, storage_type=None):
        self.storage_type = storage_type


def create_instance_args_2_dict(args):
    return {
        'storageType': args.storage_type
    }


class CreateTableArgs(object):
    def __init__(self, table_version=0, compress_type="NONE", ttl=0, storage_type=None, max_versions=1):
        self.table_version = table_version
        self.compress_type = compress_type
        self.ttl = ttl
        self.storage_type = storage_type
        self.max_versions = max_versions


def create_table_args_2_dict(args):
    return {
        'tableVersion': args.table_version,
        'compressType': args.compress_type,
        'ttl': args.ttl,
        'storageType': args.storage_type,
        'maxVersions': args.max_versions
    }


class UpdateTableArgs(object):
    def __init__(self, table_version=1, compress_type=None, ttl=None, max_versions=None):
        self.table_version = table_version
        self.compress_type = compress_type
        self.ttl = ttl
        self.max_versions = max_versions


def update_table_args_2_dict(args):
    return {
        'tableVersion': args.table_version,
        'compressType': args.compress_type,
        'ttl': args.ttl,
        'maxVersions': args.max_versions
    }


class Cell(object):
    def __init__(self, column, value):
        self.column = column
        self.value = value


class Row(object):
    def __init__(self, rowkey=None):
        self.rowkey = rowkey
        self.cells = []

    def append_cell(self, cell):
        self.cells.append(cell)

    def get_cell(self):
        return self.cells


class BatchPutRowArgs(object):
    def __init__(self):
        self.rows = []

    def append_row(self, row):
        self.rows.append(row)

    def get_row(self):
        return self.rows


class QueryCell(object):
    def __init__(self, column=None):
        self.column = column


class QueryRowArgs(object):
    def __init__(self, rowkey=None, max_versions=None):
        self.rowkey = rowkey
        self.max_versions = max_versions
        self.cells = []

    def append_cell(self, cell):
        self.cells.append(cell)

    def get_cell(self):
        return self.cells


def query_row_args_2_dict(args):
    return {
        'rowkey': args.rowkey,
        'maxVersions': args.max_versions,
        'cells': args.cells
    }


class BatchQueryRowArgs(object):
    def __init__(self, max_versions=1):
        self.rows = []
        self.max_versions = max_versions

    def append_row(self, row):
        self.rows.append(row)

    def get_rows(self):
        return self.rows


def batch_query_row_args_2_dict(args):
    return {
        'maxVersions': args.max_versions,
        'rows': args.rows
    }


class ScanArgs(object):
    def __init__(self, start_rowkey=None, include_start=True, stop_rowkey=None,
                 include_stop=False, limit=None, max_versions=1):
        self.start_rowkey = start_rowkey
        self.include_start = include_start
        self.stop_rowkey = stop_rowkey
        self.include_stop = include_stop
        self.limit = limit
        self.max_versions = max_versions
        self.selector = []

    def append_selector(self, query_cell):
        self.selector.append(query_cell)

    def get_selector(self):
        return self.selector


def scan_args_2_dict(args):
    return {
        'startRowkey': args.start_rowkey,
        'includeStart': args.include_start,
        'stopRowkey': args.stop_rowkey,
        'includeStop': args.include_stop,
        'selector': args.selector,
        'limit': args.limit,
        'maxVersions': args.max_versions
    }

