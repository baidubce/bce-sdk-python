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
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_content_types
from baidubce.http import http_headers
from baidubce.http import http_methods
from baidubce.services import bts
from baidubce.services.bts.model import batch_query_row_args_2_dict
from baidubce.services.bts.model import create_instance_args_2_dict
from baidubce.services.bts.model import CreateInstanceArgs
from baidubce.services.bts.model import create_table_args_2_dict
from baidubce.services.bts.model import update_table_args_2_dict
from baidubce.services.bts.model import query_row_args_2_dict
from baidubce.services.bts.model import scan_args_2_dict

_logger = logging.getLogger(__name__)


class BtsClient(BceBaseClient):
    """
    BTS Client
    """
    def __init__(self, config=None):
        BceBaseClient.__init__(self, config)

    # ------------- instance operation -----------
    def create_instance(self, instance_name, create_instance_args=None, config=None):
        print("------- create instance -------")
        path = bts.URL_PREFIX + b"/" + instance_name
        if create_instance_args is None:
            create_instance_args = CreateInstanceArgs()
        return self._send_request(http_methods.PUT, path=path, config=config,
                                  body=json.dumps(create_instance_args, default=create_instance_args_2_dict),
                                  headers={http_headers.CONTENT_TYPE: http_content_types.JSON})

    def drop_instance(self, instance_name, config=None):
        print("------- drop instance -------")
        path = bts.URL_PREFIX + b"/" + instance_name
        return self._send_request(http_methods.DELETE, path=path, config=config)

    def list_instances(self, config=None):
        print("------- list instances -------")
        path = b"/v1/instances"
        return self._send_request(http_methods.GET, path=path, config=config)

    def show_instance(self, instance_name, config=None):
        print("------- show instance -------")
        path = bts.URL_PREFIX + b"/" + instance_name
        return self._send_request(http_methods.GET, path=path, config=config)

    # ------------- table operation -----------
    def create_table(self, instance_name, table_name, create_table_args, config=None):
        print("------- create table -------")
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name
        return self._send_request(http_methods.PUT, path=path, config=config,
                                  body=json.dumps(create_table_args, default=create_table_args_2_dict),
                                  headers={http_headers.CONTENT_TYPE: http_content_types.JSON})

    def update_table(self, instance_name, table_name, update_table_args, config=None):
        print("------- update table -------")
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name
        return self._send_request(http_methods.PUT, path=path, config=config,
                                  body=json.dumps(update_table_args, default=update_table_args_2_dict),
                                  headers={http_headers.CONTENT_TYPE: http_content_types.JSON})

    def drop_table(self, instance_name, table_name, config=None):
        print("------- drop table -------")
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name
        return self._send_request(http_methods.DELETE, path=path, config=config)

    def show_table(self, instance_name, table_name, config=None):
        print("------- show table -------")
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name
        return self._send_request(http_methods.GET, path=path, config=config)

    def list_tables(self, instance_name, config=None):
        print("------- list table -------")
        path = bts.URL_PREFIX + b"/" + instance_name + b"/tables"
        return self._send_request(http_methods.GET, path=path, config=config)

    # ------------- row operation -----------
    def put_row(self, instance_name, table_name, put_row_args, config=None):
        print("------- put row -------")
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name + b"/row"
        return self._send_request(http_methods.PUT, path=path, config=config,
                                  body=json.dumps(put_row_args.__dict__),
                                  headers={http_headers.CONTENT_TYPE: http_content_types.JSON})

    def batch_put_row(self, instance_name, table_name, batch_put_row_args, config=None):
        print("------- batch put row -------")
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name + b"/rows"
        return self._send_request(http_methods.PUT, path=path, config=config,
                                  body=json.dumps(batch_put_row_args.__dict__),
                                  headers={http_headers.CONTENT_TYPE: http_content_types.JSON})

    def delete_row(self, instance_name, table_name, delete_row_args, config=None):
        print("------- delete row -------")
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name + b"/row"
        return self._send_request(http_methods.DELETE, path=path, config=config,
                                  body=json.dumps(delete_row_args, default=query_row_args_2_dict),
                                  headers={http_headers.CONTENT_TYPE: http_content_types.JSON})

    def batch_delete_row(self, instance_name, table_name, batch_delete_row_args, config=None):
        print("------- batch delete row -------")
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name + b"/rows"
        return self._send_request(http_methods.DELETE, path=path, config=config,
                                  body=json.dumps(batch_delete_row_args, default=batch_query_row_args_2_dict),
                                  headers={http_headers.CONTENT_TYPE: http_content_types.JSON})

    def get_row(self, instance_name, table_name, get_row_args, config=None):
        print("------- get row -------")
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name + b"/row"
        return self._send_request(http_methods.GET, path=path, config=config,
                                  body=json.dumps(get_row_args, default=query_row_args_2_dict),
                                  headers={http_headers.CONTENT_TYPE: http_content_types.JSON})

    def batch_get_row(self, instance_name, table_name, batch_get_row_args, config=None):
        print("------- batch get row -------")
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name + b"/rows"
        return self._send_request(http_methods.GET, path=path, config=config,
                                  body=json.dumps(batch_get_row_args, default=batch_query_row_args_2_dict),
                                  headers={http_headers.CONTENT_TYPE: http_content_types.JSON})

    def scan(self, instance_name, table_name, scan_args, config=None):
        print("------- scan -------")
        path = bts.URL_PREFIX + b"/" + instance_name + b"/table/" + table_name + b"/rows"

        print(json.dumps(scan_args, default=scan_args_2_dict))
        return self._send_request(http_methods.GET, path=path, config=config,
                                  body=json.dumps(scan_args, default=scan_args_2_dict),
                                  headers={http_headers.CONTENT_TYPE: http_content_types.JSON})

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
