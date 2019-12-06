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
Samples for bts client.
"""

import bts_sample_conf

from baidubce.services.bts.bts_client import BtsClient
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

'''
# inorder to both support python2 and python3
import os
import sys

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    from sample.bts import bts_sample_conf
else:
    import bts_sample_conf
'''

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger(__name__)

    # create a bts client
    bts_client = BtsClient(bts_sample_conf.config)

    ######################################################################################################
    #            instance operation samples
    ######################################################################################################

    # create instance
    instance_name = b'instance1'
    createInstanceArgs = CreateInstanceArgs('CommonPerformance')
    response = bts_client.create_instance(instance_name, createInstanceArgs)
    print(response)

    instance_name = b'instance2'
    response = bts_client.create_instance(instance_name)
    print(response)

    # show instance
    instance_name = b'instance1'
    response = bts_client.show_instance(instance_name)
    print(response)

    # list instances
    response = bts_client.list_instances()
    print(response.instances)

    # drop instance
    instance_name = b'instance2'
    response = bts_client.drop_instance(instance_name)
    print(response)

    ######################################################################################################
    #            table operation samples
    ######################################################################################################
    instance_name = b'instance1'

    # create table
    table_name = b'tab01'
    createTableArgs = CreateTableArgs()
    createTableArgs.table_version = 0
    createTableArgs.compress_type = "SNAPPY_ALL"
    createTableArgs.ttl = 0
    createTableArgs.storage_type = "CommonPerformance"
    createTableArgs.max_versions = 10
    response = bts_client.create_table(instance_name, table_name, createTableArgs)
    print(response)

    # show table
    table_name = b'tab01'
    response = bts_client.show_table(instance_name, table_name)
    print(response)

    # list tables
    response = bts_client.list_tables(instance_name)
    print(response)

    # update table
    table_name = b'tab01'
    show_table_response = bts_client.show_table(instance_name, table_name)
    updateTableArgs = UpdateTableArgs()
    updateTableArgs.table_version = show_table_response.table_version
    updateTableArgs.compress_type = "NONE"
    updateTableArgs.max_versions = 20
    updateTableArgs.time_to_live = 86400
    response = bts_client.update_table(instance_name, table_name, updateTableArgs)
    print(response)

    # drop table
    table_name = b'tab03'
    response = bts_client.drop_table(instance_name, table_name)
    print(response)

    ######################################################################################################
    #            row operation samples
    ######################################################################################################
    instance_name = b'instance1'
    table_name = b'tab01'

    # put row
    row = Row()
    row.rowkey = "row1"
    cell1 = Cell("c1", "v1_1")
    cell2 = Cell("c2", "v2_1")
    cells = [cell1.__dict__, cell2.__dict__]
    row.cells = cells

    response = bts_client.put_row(instance_name, table_name, row)
    print(response)

    # batch put row
    batchPutRow = BatchPutRowArgs()
    for i in range(2, 15):
        row = Row()
        row.rowkey = "row" + str(i)
        for j in range(3):
            col = "c" + str(j)
            val = "v" + str(j) + "_1"
            cell = Cell(col, val)
            row.cells.append(cell.__dict__)
        batchPutRow.rows.append(row.__dict__)

    response = bts_client.batch_put_row(instance_name, table_name, batchPutRow)
    print(response)

    # delete row
    queryRowArgs = QueryRowArgs()
    queryRowArgs.rowkey = "row1"
    cell1 = QueryCell()
    cell1.column = "c1"
    queryRowArgs.cells.append(cell1.__dict__)
    response = bts_client.delete_row(instance_name, table_name, queryRowArgs)
    print(response)

    # batch delete row
    batchQueryRowArgs = BatchQueryRowArgs()
    queryRowArgs1 = QueryRowArgs()
    queryRowArgs1.rowkey = "row1"
    queryRowArgs1.cells.append(QueryCell("c0").__dict__)
    queryRowArgs1.cells.append(QueryCell("c1").__dict__)
    batchQueryRowArgs.rows.append(queryRowArgs1.__dict__)

    queryRowArgs2 = QueryRowArgs()
    queryRowArgs2.rowkey = "row2"
    queryRowArgs2.cells.append(QueryCell("c1").__dict__)
    queryRowArgs2.cells.append(QueryCell("c2").__dict__)
    batchQueryRowArgs.rows.append(queryRowArgs2.__dict__)

    response = bts_client.batch_delete_row(instance_name, table_name, batchQueryRowArgs)
    print(response)

    # get row
    queryRowArgs = QueryRowArgs()
    queryRowArgs.rowkey = "row1"
    queryRowArgs.cells.append(QueryCell("c1").__dict__)
    queryRowArgs.cells.append(QueryCell("c2").__dict__)
    queryRowArgs.max_versions = 2
    response = bts_client.get_row(instance_name, table_name, queryRowArgs)
    print(response)

    # batch get row
    batchQueryRowArgs = BatchQueryRowArgs()
    batchQueryRowArgs.max_versions = 2

    queryRowArgs1 = QueryRowArgs()
    queryRowArgs1.rowkey = "row12"
    queryRowArgs1.cells.append(QueryCell("c0").__dict__)
    queryRowArgs1.cells.append(QueryCell("c1").__dict__)
    batchQueryRowArgs.rows.append(queryRowArgs1.__dict__)

    queryRowArgs2 = QueryRowArgs()
    queryRowArgs2.rowkey = "row13"
    queryRowArgs2.cells.append(QueryCell("c1").__dict__)
    queryRowArgs2.cells.append(QueryCell("c2").__dict__)
    batchQueryRowArgs.rows.append(queryRowArgs2.__dict__)

    response = bts_client.batch_get_row(instance_name, table_name, batchQueryRowArgs)
    print(response)

    # scan
    scanArgs = ScanArgs()
    scanArgs.start_rowkey = "row10"
    scanArgs.include_start = "false"
    scanArgs.stop_rowkey = "row14"
    scanArgs.include_stop = "true"
    scanArgs.selector.append(QueryCell("c0").__dict__)
    scanArgs.selector.append(QueryCell("c1").__dict__)
    scanArgs.selector.append(QueryCell("c2").__dict__)
    scanArgs.max_versions = 2
    scanArgs.limit = 20

    response = bts_client.scan(instance_name, table_name, scanArgs)
    print(response)

