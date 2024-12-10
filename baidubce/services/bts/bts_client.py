# Copyright 2014 Baidu, Inc.
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
This module provides a client class for BTS.
"""

import copy
import json
import logging

from baidubce.auth import bce_v1_signer
from baidubce.bce_base_client import BceBaseClient
from baidubce.exception import BceClientError
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_content_types
from baidubce.http import http_headers
from baidubce.http import http_methods
from baidubce.services import bts
from baidubce.services.bts import INVALID_ARGS_ERROR
from baidubce.services.bts.model import create_instance_args_2_dict
from baidubce.services.bts.model import CreateInstanceArgs
from baidubce.services.bts.model import Row
from baidubce.services.bts.model import Cell
from baidubce.services.bts.model import QueryCell
from baidubce.services.bts.model import BatchQueryRowArgs
from baidubce.services.bts.model import QueryRowArgs
from baidubce.services.bts.model import ScanArgs
from baidubce.services.bts.model import create_table_args_2_dict
from baidubce.services.bts.model import update_table_args_2_dict
from baidubce.services.bts.util import _decode
from baidubce.services.bts.util import _encode

_logger = logging.getLogger(__name__)


class BtsClient(BceBaseClient):
    """
    BTS Client
    """
    def __init__(self, config=None):
        BceBaseClient.__init__(self, config)

    # ------------- instance operation -----------
    def create_instance(self, instance_name, create_instance_args=None, config=None):
        """
        create instance

        :param instance_name: instance name
        :type instance_name: string
        :param create_instance_args: arguments for create instance
        :type create_instance_args: CreateInstanceArgs
        :param config: None
        :type config: BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = bts.URL_PREFIX + b"/" + instance_name
        if create_instance_args is None:
            create_instance_args = CreateInstanceArgs()
        return self._send_request(http_methods.PUT, path=path, config=config,
                                  body=json.dumps(create_instance_args, default=create_instance_args_2_dict),
                                  headers={http_headers.CONTENT_TYPE: http_content_types.JSON})

    def drop_instance(self, instance_name, config=None):
        """
        drop instance

        :param instance_name: instance name
        :type instance_name: string
        :param config: None
        :type config: BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = bts.URL_PREFIX + b"/" + instance_name
        return self._send_request(http_methods.DELETE, path=path, config=config)

    def list_instances(self, config=None):
        """
        list instances

        :param config: None
        :type config: BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = b"/v1/instances"
        return self._send_request(http_methods.GET, path=path, config=config)

    def show_instance(self, instance_name, config=None):
        """
        show instance

        :param instance_name: instance name
        :type instance_name: string
        :param config: None
        :type config: BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = bts.URL_PREFIX + b"/" + instance_name
        return self._send_request(http_methods.GET, path=path, config=config)

    # ------------- table operation -----------
    def create_table(self, instance_name, table_name, create_table_args, config=None):
        """
        create table

        :param instance_name: instance name
        :type instance_name: string
        :param table_name: table name
        :type table_name: string
        :param create_table_args: arguments for create table
        :type create_table_args: CreateTableArgs
        :param config: None
        :type config: BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name
        return self._send_request(http_methods.PUT, path=path, config=config,
                                  body=json.dumps(create_table_args, default=create_table_args_2_dict),
                                  headers={http_headers.CONTENT_TYPE: http_content_types.JSON})

    def update_table(self, instance_name, table_name, update_table_args, config=None):
        """
        update table

        :param instance_name: instance name
        :type instance_name: string
        :param table_name: table name
        :type table_name: string
        :param update_table_args: arguments for update table
        :type update_table_args: UpdateTableArgs
        :param config: None
        :type config: BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name
        return self._send_request(http_methods.PUT, path=path, config=config,
                                  body=json.dumps(update_table_args, default=update_table_args_2_dict),
                                  headers={http_headers.CONTENT_TYPE: http_content_types.JSON})

    def drop_table(self, instance_name, table_name, config=None):
        """
        drop table

        :param instance_name: instance name
        :type instance_name: string
        :param table_name: table name
        :type table_name: string
        :param config: None
        :type config: BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name
        return self._send_request(http_methods.DELETE, path=path, config=config)

    def show_table(self, instance_name, table_name, config=None):
        """
        show table

        :param instance_name: instance name
        :type instance_name: string
        :param table_name: table name
        :type table_name: string
        :param config: None
        :type config: BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name
        return self._send_request(http_methods.GET, path=path, config=config)

    def list_tables(self, instance_name, config=None):
        """
        list tables

        :param instance_name: instance name
        :type instance_name: string
        :param config: None
        :type config: BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = bts.URL_PREFIX + b"/" + instance_name + b"/tables"
        return self._send_request(http_methods.GET, path=path, config=config)

    # ------------- row operation -----------
    def put_row(self, instance_name, table_name, put_row_args, config=None):
        """
        put row

        :param instance_name: instance name
        :type instance_name: string
        :param table_name: table name
        :type table_name: string
        :param put_row_args: arguments for put row
        :type put_row_args: Row
        :param config: None
        :type config: BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        if put_row_args is None or put_row_args.rowkey == "":
            ex = BceClientError(INVALID_ARGS_ERROR)
            _logger.debug(ex)
            raise ex
        row_data = {
            'rowkey': _encode(put_row_args.rowkey),
            'cells': []
        }
        try:
            for cell in put_row_args.cells:
                if isinstance(cell, Cell):
                    cell_dict = cell.to_dict()
                    cell_dict['value'] = _encode(cell_dict['value'])
                    row_data['cells'].append(cell_dict)
                elif isinstance(cell, dict):
                    cell['value'] = _encode(cell['value'])
                    row_data['cells'].append(cell)
                else:
                    raise BceClientError(INVALID_ARGS_ERROR)
        except Exception as ex:
            raise ex

        body = json.dumps(row_data)
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name + b"/row"
        return self._send_request(http_methods.PUT, path=path, config=config,
                                  body=body,
                                  headers={http_headers.CONTENT_TYPE: http_content_types.JSON})

    def batch_put_row(self, instance_name, table_name, batch_put_row_args, config=None):
        """
        batch put row

        :param instance_name: instance name
        :type instance_name: string
        :param table_name: table name
        :type table_name: string
        :param batch_put_row_args: arguments for batch put row
        :type batch_put_row_args: BatchPutRowArgs
        :param config: None
        :type config: BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        if batch_put_row_args is None:
            ex = BceClientError(INVALID_ARGS_ERROR)
            _logger.debug(ex)
            raise ex

        rows_data = []
        for row in batch_put_row_args.rows:
            try:
                if isinstance(row, Row):
                    row_data = row.to_dict()
                    if row_data["rowkey"] == "":
                        raise BceClientError(INVALID_ARGS_ERROR)
                elif isinstance(row, dict):
                    row_data = copy.deepcopy(row)
                    if row_data.get("rowkey") == "":
                        raise BceClientError(INVALID_ARGS_ERROR)
                else:
                    raise BceClientError(INVALID_ARGS_ERROR)
                row_data["rowkey"] = _encode(row_data["rowkey"])
                for cell in row_data.get("cells", []):
                    cell["value"] = _encode(cell["value"])
                rows_data.append(row_data)
            except Exception as ex:
                raise ex

        body = json.dumps({'rows': rows_data})
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name + b"/rows"
        return self._send_request(http_methods.PUT, path=path, config=config,
                                  body=body,
                                  headers={http_headers.CONTENT_TYPE: http_content_types.JSON})

    def delete_row(self, instance_name, table_name, delete_row_args, config=None):
        """
        delete row

        :param instance_name: instance name
        :type instance_name: string
        :param table_name: table name
        :type table_name: string
        :param delete_row_args: arguments for delete row
        :type delete_row_args: QueryRowArgs
        :param config: None
        :type config: BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        if delete_row_args is None or not hasattr(delete_row_args, 'rowkey') or delete_row_args.rowkey == "":
            ex = BceClientError(INVALID_ARGS_ERROR)
            _logger.debug(ex)
            raise ex
        delete_row_data = {
            'rowkey': _encode(delete_row_args.rowkey),
            'cells': []
        }
        try:
            if hasattr(delete_row_args, 'cells') and delete_row_args.cells:
                for cell in delete_row_args.cells:
                    if isinstance(cell, QueryCell):
                        delete_row_data['cells'].append(cell.to_dict())
                    elif isinstance(cell, dict):
                        delete_row_data['cells'].append(cell)
                    else:
                        raise BceClientError(INVALID_ARGS_ERROR)
        except Exception as ex:
            raise ex

        body = json.dumps(delete_row_data)
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name + b"/row"
        return self._send_request(http_methods.DELETE, path=path, config=config,
                              body=body,
                              headers={http_headers.CONTENT_TYPE: http_content_types.JSON})

    def batch_delete_row(self, instance_name, table_name, batch_delete_row_args, config=None):
        """
        batch delete row

        :param instance_name: instance name
        :type instance_name: string
        :param table_name: table name
        :type table_name: string
        :param batch_delete_row_args: arguments for batch delete row
        :type batch_delete_row_args: BatchQueryRowArgs
        :param config: None
        :type config: BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        if batch_delete_row_args is None or not isinstance(batch_delete_row_args, BatchQueryRowArgs):
            raise BceClientError(INVALID_ARGS_ERROR)
        rows_data = []
        try:
            for row in batch_delete_row_args.rows:
                if isinstance(row, QueryRowArgs):
                    row_data = row.to_dict()
                elif isinstance(row, dict):
                    row_data = row
                else:
                    raise BceClientError(INVALID_ARGS_ERROR)

                if "rowkey" in row_data and row_data["rowkey"]:
                    row_data["rowkey"] = _encode(row_data["rowkey"])
                else:
                    raise BceClientError(INVALID_ARGS_ERROR)
                rows_data.append(row_data)
        except Exception as ex:
            raise ex

        batch_delete_row_data = {'rows': rows_data}
        body = json.dumps(batch_delete_row_data)
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name + b"/rows"
        return self._send_request(http_methods.DELETE, path=path, config=config,
                                body=body,
                                headers={http_headers.CONTENT_TYPE: http_content_types.JSON})

    def get_row(self, instance_name, table_name, get_row_args, config=None):
        """
        get row

        :param instance_name: instance name
        :type instance_name: string
        :param table_name: table name
        :type table_name: string
        :param get_row_args: arguments for get row
        :type get_row_args: QueryRowArg
        :param config: None
        :type config: BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        if isinstance(get_row_args, dict):
            rowkey = get_row_args.get('rowkey')
        elif isinstance(get_row_args, QueryRowArgs):
            rowkey = get_row_args.rowkey
        else:
            raise BceClientError(INVALID_ARGS_ERROR)

        if not rowkey:
            raise BceClientError(INVALID_ARGS_ERROR)

        get_row_data = {
            'rowkey': _encode(rowkey),
            'cells': []
        }

        if hasattr(get_row_args, 'cells') and get_row_args.cells:
            for cell in get_row_args.cells:
                if isinstance(cell, QueryCell):
                    get_row_data['cells'].append(cell.to_dict())
                elif isinstance(cell, dict):
                    get_row_data['cells'].append(cell)
                else:
                    raise BceClientError(INVALID_ARGS_ERROR)

        body = json.dumps(get_row_data)
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name + b"/row"
        response = self._send_request(http_methods.POST, path=path, config=config,
                                    body=body,
                                    headers={http_headers.CONTENT_TYPE: http_content_types.JSON,
                                             http_headers.BTS_METHOD_HEADER: http_methods.GET})
        try:
            if response.result is not None:
                response.result[0].rowkey = _decode(str(response.result[0].rowkey))
                for i in range(len(response.result[0].cells)):
                    response.result[0].cells[i].value = _decode(str(response.result[0].cells[i].value))
        except Exception as ex:
            raise ex
        return response

    def batch_get_row(self, instance_name, table_name, batch_get_row_args, config=None):
        """
        batch get row

        :param instance_name: instance name
        :type instance_name: string
        :param table_name: table name
        :type table_name: string
        :param batch_get_row_args: arguments for batch get row
        :type batch_get_row_args: BatchQueryRowArgs
        :param config: None
        :type config: BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        batch_get_row_data = {}

        if isinstance(batch_get_row_args, BatchQueryRowArgs):
            rows_data = []
            for row_arg in batch_get_row_args.rows:
                if isinstance(row_arg, QueryRowArgs):
                    row_data = row_arg.to_dict()
                elif isinstance(row_arg, dict):
                    row_data = row_arg
                else:
                    raise BceClientError(INVALID_ARGS_ERROR)

                if "rowkey" in row_data and row_data["rowkey"]:
                    row_data["rowkey"] = _encode(row_data["rowkey"])
                else:
                    raise BceClientError(INVALID_ARGS_ERROR)

                rows_data.append(row_data)
            batch_get_row_data['rows'] = rows_data

        elif isinstance(batch_get_row_args, dict):
            batch_get_row_data = batch_get_row_args

        else:
            raise BceClientError(INVALID_ARGS_ERROR)

        body = json.dumps(batch_get_row_data)
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name + b"/rows"
        response = self._send_request(http_methods.POST, path=path, config=config,
                                    body=body,
                                    headers={http_headers.CONTENT_TYPE: http_content_types.JSON,
                                             http_headers.BTS_METHOD_HEADER: http_methods.GET})

        try:
            if response.result is not None:
                for i in range(len(response.result)):
                    response.result[i].rowkey = _decode(str(response.result[i].rowkey))
                    for j in range(len(response.result[i].cells)):
                        response.result[i].cells[j].value = _decode(str(response.result[i].cells[j].value))
        except Exception as ex:
            raise ex
        return response

    def scan(self, instance_name, table_name, scan_args, config=None):
        """
        scan

        :param instance_name: instance name
        :type instance_name: string
        :param table_name: table name
        :type table_name: string
        :param scan_args: arguments for scan
        :type scan_args: ScanArgs
        :param config: None
        :type config: BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        if isinstance(scan_args, ScanArgs):
            # Convert ScanArgs to a dictionary if necessary
            scan_args_dict = scan_args.to_dict()  # Assuming ScanArgs has a to_dict() method
        elif isinstance(scan_args, dict):
            scan_args_dict = scan_args
        else:
            raise BceClientError(INVALID_ARGS_ERROR)

        if "startRowkey" in scan_args_dict and scan_args_dict["startRowkey"]:
            scan_args_dict["startRowkey"] = _encode(scan_args_dict["startRowkey"])
        if "stopRowkey" in scan_args_dict and scan_args_dict["stopRowkey"]:
            scan_args_dict["stopRowkey"] = _encode(scan_args_dict["stopRowkey"])

        body = json.dumps(scan_args_dict)
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name + b"/rows"
        response = self._send_request(http_methods.GET, path=path, config=config,
                                    body=body,
                                    headers={http_headers.CONTENT_TYPE: http_content_types.JSON})

        try:
            if response.result is not None:
                for i in range(len(response.result)):
                    response.result[i].rowkey = _decode(str(response.result[i].rowkey))
                    for j in range(len(response.result[i].cells)):
                        response.result[i].cells[j].value = _decode(str(response.result[i].cells[j].value))
        except Exception as ex:
            raise ex
        return response

    def _merge_config(self, config):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    # ------------- Http Request -----------
    def _send_request(
            self, http_method, path,
            body=None, headers=None, params=None,
            config=None,
            body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json

        if config.security_token is not None:
            headers = headers or {}
            headers[http_headers.STS_SECURITY_TOKEN] = config.security_token

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, path, body, headers, params)


