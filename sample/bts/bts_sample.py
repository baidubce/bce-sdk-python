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
Samples for bts client.
"""

import bts_sample_conf

from baidubce import exception
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
    createInstanceArgs = CreateInstanceArgs()
    createInstanceArgs.storage_type = 'CommonPerformance'
    response = bts_client.create_instance(instance_name, createInstanceArgs)
    print(response)

    instance_name = b'instance3'
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
    instance_name = b'instance3'
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
    
    table_name = b'tab02'
    createTableArgs = CreateTableArgs()
    createTableArgs.table_version = 0
    response = bts_client.create_table(instance_name, table_name, createTableArgs)
    print(response)

    # show table
    table_name = b'tab02'
    response = bts_client.show_table(instance_name, table_name)
    print(response)

    # list tables
    response = bts_client.list_tables(instance_name)
    print(response)
    
    # update table
    table_name = b'tab02'
    show_table_response = bts_client.show_table(instance_name, table_name)
    updateTableArgs = UpdateTableArgs()
    updateTableArgs.table_version = show_table_response.table_version
    updateTableArgs.compress_type = "NONE"
    updateTableArgs.max_versions = 27
    updateTableArgs.ttl = 86400
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
    table_name = b'tab02'

    # put row
    row1 = Row()
    row1.rowkey = "row1"
    cell1 = Cell("c1", "v1_1")
    cell2 = Cell("c2", "v2_1")
    cells = [cell1.__dict__, cell2.__dict__]
    row1.cells = cells

    try:
        response = bts_client.put_row(instance_name, table_name, row1)
        print(response)
    except exception.BceError as e:
        __logger.debug(e)
    
    # put row
    row2 = Row()
    row2.rowkey = "row1 11a_+你好  hi  _/  hi2 + + "
    cell1 = Cell("c1", "v1_1  ++值是1—4— ， ；可")
    cell2 = Cell("c2", "v2_1")
    cells = [cell1.__dict__, cell2.__dict__]
    row2.cells = cells

    try:
        response = bts_client.put_row(instance_name, table_name, row2)
        print(response)
    except exception.BceError as e:
        __logger.debug(e)

    # batch put row
    batchPutRow1 = BatchPutRowArgs()
    for i in range(2, 15):
        row = Row()
        row.rowkey = "row" + str(i)
        for j in range(3):
            col = "c" + str(j)
            val = "v" + str(j) + "_2"
            cell = Cell(col, val)
            row.cells.append(cell.__dict__)
        batchPutRow1.rows.append(row.__dict__)

    try:
        response = bts_client.batch_put_row(instance_name, table_name, batchPutRow1)
        print(response)
    except exception.BceError as e:
        __logger.debug(e)
    
    # batch put row
    batchPutRow2 = BatchPutRowArgs()
    for i in range(2, 5):
        row = Row()
        row.rowkey = "row +" + str(i) + "jk@ +行 +  "
        for j in range(3):
            col = "c" + str(j)
            val = "v" + str(j) + "_4——值  =+  "
            cell = Cell(col, val)
            row.cells.append(cell.__dict__)
        batchPutRow2.rows.append(row.__dict__)

    try:
        response = bts_client.batch_put_row(instance_name, table_name, batchPutRow2)
        print(response)
    except exception.BceError as e:
        __logger.debug(e)
    
    # delete row
    queryRowArgs1 = QueryRowArgs()
    queryRowArgs1.rowkey = "row2"
    cell1 = QueryCell()
    cell1.column = "c1"
    queryRowArgs1.cells.append(cell1.__dict__)

    try:
        response = bts_client.delete_row(instance_name, table_name, queryRowArgs1)
        print(response)
    except exception.BceError as e:
        __logger.debug(e)

    # delete row
    queryRowArgs2 = QueryRowArgs()
    queryRowArgs2.rowkey = "row +" + str(4) + "jk@ +行 +  "
    cell2 = QueryCell()
    cell2.column = "c1"
    queryRowArgs2.cells.append(cell2.__dict__)

    try:
        response = bts_client.delete_row(instance_name, table_name, queryRowArgs2)
        print(response)
    except exception.BceError as e:
        __logger.debug(e)
    
    # batch delete row
    batchQueryRowArgs1 = BatchQueryRowArgs()
    queryRowArgs1 = QueryRowArgs()
    queryRowArgs1.rowkey = "row1"
    queryRowArgs1.cells.append(QueryCell("c0").__dict__)
    queryRowArgs1.cells.append(QueryCell("c1").__dict__)
    batchQueryRowArgs1.rows.append(queryRowArgs1.__dict__)

    queryRowArgs2 = QueryRowArgs()
    queryRowArgs2.rowkey = "row2"
    queryRowArgs2.cells.append(QueryCell("c1").__dict__)
    queryRowArgs2.cells.append(QueryCell("c2").__dict__)
    batchQueryRowArgs1.rows.append(queryRowArgs2.__dict__)

    try:
        response = bts_client.batch_delete_row(instance_name, table_name, batchQueryRowArgs1)
        print(response)
    except exception.BceError as e:
        __logger.debug(e)

    # batch delete row
    batchQueryRowArgs2 = BatchQueryRowArgs()
    queryRowArgs3 = QueryRowArgs()
    queryRowArgs3.rowkey = "row +" + str(3) + "jk@ +行 +  "
    queryRowArgs3.cells.append(QueryCell("c0").__dict__)
    queryRowArgs3.cells.append(QueryCell("c1").__dict__)
    batchQueryRowArgs2.rows.append(queryRowArgs3.__dict__)

    queryRowArgs4 = QueryRowArgs()
    queryRowArgs4.rowkey = "row +" + str(4) + "jk@ +行 +  "
    queryRowArgs4.cells.append(QueryCell("c1").__dict__)
    queryRowArgs4.cells.append(QueryCell("c2").__dict__)
    batchQueryRowArgs2.rows.append(queryRowArgs4.__dict__)

    try:
        response = bts_client.batch_delete_row(instance_name, table_name, batchQueryRowArgs2)
        print(response)
    except exception.BceError as e:
        __logger.debug(e)
    
    # get row
    queryRowArgs1 = QueryRowArgs()
    queryRowArgs1.rowkey = "row4"
    queryRowArgs1.cells.append(QueryCell("c0").__dict__)
    queryRowArgs1.cells.append(QueryCell("c1").__dict__)
    queryRowArgs1.max_versions = 2

    try:
        response = bts_client.get_row(instance_name, table_name, queryRowArgs1)
        if response.result is not None:
            print("rowkey: " + response.result[0].rowkey)
            for i in range(len(response.result[0].cells)):
                print("  column: " + response.result[0].cells[i].column)
                print("  value: " + response.result[0].cells[i].value)
                print("  timestamp: " + str(response.result[0].cells[i].timestamp))
    except exception.BceError as e:
        __logger.debug(e)

    # get row
    queryRowArgs2 = QueryRowArgs()
    queryRowArgs2.rowkey = "row +" + str(2) + "jk@ +行 +  "
    queryRowArgs2.cells.append(QueryCell("c1").__dict__)
    queryRowArgs2.cells.append(QueryCell("c2").__dict__)
    queryRowArgs2.max_versions = 2

    try:
        response = bts_client.get_row(instance_name, table_name, queryRowArgs2)
        if response.result is not None:
            print("rowkey: " + response.result[0].rowkey)
            for i in range(len(response.result[0].cells)):
                print("  column: " + response.result[0].cells[i].column)
                print("  value: " + response.result[0].cells[i].value)
                print("  timestamp: " + str(response.result[0].cells[i].timestamp))
    except exception.BceError as e:
        __logger.debug(e)

    # batch get row
    batchQueryRowArgs1 = BatchQueryRowArgs()
    batchQueryRowArgs1.max_versions = 2

    queryRowArgs1 = QueryRowArgs()
    queryRowArgs1.rowkey = "row12"
    queryRowArgs1.cells.append(QueryCell("c0").__dict__)
    queryRowArgs1.cells.append(QueryCell("c1").__dict__)
    batchQueryRowArgs1.rows.append(queryRowArgs1.__dict__)

    queryRowArgs2 = QueryRowArgs()
    queryRowArgs2.rowkey = "row13"
    queryRowArgs2.cells.append(QueryCell("c1").__dict__)
    queryRowArgs2.cells.append(QueryCell("c2").__dict__)
    batchQueryRowArgs1.rows.append(queryRowArgs2.__dict__)

    try:
        response = bts_client.batch_get_row(instance_name, table_name, batchQueryRowArgs1)
        if response.result is not None:
            for i in range(len(response.result)):
                print("rowkey: " + response.result[i].rowkey)
                for j in range(len(response.result[i].cells)):
                    print("  column: " + response.result[i].cells[j].column)
                    print("  value: " + response.result[i].cells[j].value)
                    print("  timestamp: " + str(response.result[i].cells[j].timestamp))
    except exception.BceError as e:
        __logger.debug(e)

    # batch get row
    batchQueryRowArgs2 = BatchQueryRowArgs()
    batchQueryRowArgs2.max_versions = 2

    queryRowArgs3 = QueryRowArgs()
    queryRowArgs3.rowkey = "row +" + str(2) + "jk@ +行 +  "
    queryRowArgs3.cells.append(QueryCell("c0").__dict__)
    queryRowArgs3.cells.append(QueryCell("c1").__dict__)
    batchQueryRowArgs2.rows.append(queryRowArgs3.__dict__)

    queryRowArgs4 = QueryRowArgs()
    queryRowArgs4.rowkey = "row +" + str(3) + "jk@ +行 +  "
    queryRowArgs4.cells.append(QueryCell("c0").__dict__)
    queryRowArgs4.cells.append(QueryCell("c2").__dict__)
    batchQueryRowArgs2.rows.append(queryRowArgs4.__dict__)

    try:
        response = bts_client.batch_get_row(instance_name, table_name, batchQueryRowArgs2)
        if response.result is not None:
            for i in range(len(response.result)):
                print("rowkey: " + response.result[i].rowkey)
                for j in range(len(response.result[i].cells)):
                    print("  column: " + response.result[i].cells[j].column)
                    print("  value: " + response.result[i].cells[j].value)
                    print("  timestamp: " + str(response.result[i].cells[j].timestamp))
    except exception.BceError as e:
        __logger.debug(e)

    # scan
    scanArgs1 = ScanArgs()
    scanArgs1.start_rowkey = "row2"
    scanArgs1.include_start = True
    scanArgs1.stop_rowkey = "row3"
    scanArgs1.include_stop = True
    scanArgs1.selector.append(QueryCell("c0").__dict__)
    scanArgs1.selector.append(QueryCell("c1").__dict__)
    scanArgs1.selector.append(QueryCell("c2").__dict__)
    scanArgs1.max_versions = 2
    scanArgs1.limit = 100

    try:
        response = bts_client.scan(instance_name, table_name, scanArgs1)
        if response.result is not None:
            for i in range(len(response.result)):
                print("rowkey: " + response.result[i].rowkey)
                for j in range(len(response.result[i].cells)):
                    print("  column: " + response.result[i].cells[j].column)
                    print("  value: " + response.result[i].cells[j].value)
                    print("  timestamp: " + str(response.result[i].cells[j].timestamp))
    except exception.BceError as e:
        __logger.debug(e)

    # scan
    scanArgs2 = ScanArgs()
    scanArgs2.start_rowkey = "row +" + str(2) + "jk@ +行 +  "
    scanArgs2.include_start = True
    scanArgs2.stop_rowkey = "row +" + str(4) + "jk@ +行 +  "
    scanArgs2.include_stop = True
    scanArgs2.selector.append(QueryCell("c0").__dict__)
    scanArgs2.selector.append(QueryCell("c1").__dict__)
    scanArgs2.selector.append(QueryCell("c2").__dict__)
    scanArgs2.max_versions = 2
    scanArgs2.limit = 200

    try:
        response = bts_client.scan(instance_name, table_name, scanArgs2)
        if response.result is not None:
            for i in range(len(response.result)):
                print("rowkey: " + response.result[i].rowkey)
                for j in range(len(response.result[i].cells)):
                    print("  column: " + response.result[i].cells[j].column)
                    print("  value: " + response.result[i].cells[j].value)
                    print("  timestamp: " + str(response.result[i].cells[j].timestamp))
    except exception.BceError as e:
        __logger.debug(e)



