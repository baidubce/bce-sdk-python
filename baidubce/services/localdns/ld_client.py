# !/usr/bin/env python
# coding=UTF-8
#
# Copyright 2023 Baidu, Inc.
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
This module provides a client class for ld.
"""

import json
import logging
from urllib.parse import quote

from baidubce import bce_base_client
from baidubce.services.localdns.api.ld_api import ld_apis

_logger = logging.getLogger(__name__)


class LdClient(bce_base_client.BceBaseClient):
    """
    ld base sdk client
    """

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)

    def add_record(self, zone_id=None, add_record_request=None, client_token=None):
        """

        :param zone_id:
        :desc zone的id
        :type zone_id: str

        :param add_record_request:
        :desc 
        :type add_record_request: json

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(ld_apis, "add_record")
        self._add_path_param(api_config, "zoneId", zone_id)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(add_record_request))

    def bind_vpc(self, zone_id=None, bind_vpc_request=None, client_token=None):
        """

        :param zone_id:
        :desc zone的id
        :type zone_id: str

        :param bind_vpc_request:
        :desc 
        :type bind_vpc_request: json

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(ld_apis, "bind_vpc")
        self._add_path_param(api_config, "zoneId", zone_id)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(bind_vpc_request))

    def create_private_zone(self, create_private_zone_request=None, client_token=None):
        """
        

        :param create_private_zone_request:
        :desc 
        :type create_private_zone_request: json

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(ld_apis, "create_private_zone")
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(create_private_zone_request))

    def delete_private_zone(self, zone_id=None, client_token=None):
        """
        

        :param zone_id:
        :desc zone的id
        :type zone_id: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(ld_apis, "delete_private_zone")
        self._add_path_param(api_config, "zoneId", zone_id)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def delete_record(self, record_id=None, delete_record_request=None, client_token=None):
        """
        

        :param record_id:
        :desc 解析记录ID
        :type record_id: str

        :param delete_record_request:
        :desc 
        :type delete_record_request: json

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(ld_apis, "delete_record")
        self._add_path_param(api_config, "recordId", record_id)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(delete_record_request))

    def disable_record(self, record_id=None, client_token=None):
        """
        

        :param record_id:
        :desc 解析记录ID
        :type record_id: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(ld_apis, "disable_record")
        self._add_path_param(api_config, "recordId", record_id)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def enable_record(self, record_id=None, client_token=None):
        """
        

        :param record_id:
        :desc 解析记录ID
        :type record_id: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(ld_apis, "enable_record")
        self._add_path_param(api_config, "recordId", record_id)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def get_private_zone(self, zone_id=None):
        """
        

        :param zone_id:
        :desc zone的ID
        :type zone_id: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(ld_apis, "get_private_zone")
        self._add_path_param(api_config, "zoneId", zone_id)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def list_private_zone(self, marker=None, max_keys=None):
        """
        

        :param marker:
        :desc 批量获取列表的查询的起始位置，是一个由系统生成的字符串
        :type marker: str

        :param max_keys:
        :desc 每页包含的最大数量，最大数量通常不超过1000。缺省值为1000
        :type max_keys: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(ld_apis, "list_private_zone")
        self._add_query(api_config, "marker", marker)
        self._add_query(api_config, "maxKeys", max_keys)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def list_record(self, zone_id=None):
        """
        

        :param zone_id:
        :desc Zone的ID
        :type zone_id: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(ld_apis, "list_record")
        self._add_path_param(api_config, "zoneId", zone_id)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def unbind_vpc(self, zone_id=None, unbind_vpc_request=None, client_token=None):
        """

        :param zone_id:
        :desc zone的id
        :type zone_id: str

        :param unbind_vpc_request:
        :desc 
        :type unbind_vpc_request: json

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(ld_apis, "unbind_vpc")
        self._add_path_param(api_config, "zoneId", zone_id)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(unbind_vpc_request))

    def update_record(self, record_id=None, update_record_request=None, client_token=None):
        """
        

        :param record_id:
        :desc 解析记录的ID
        :type record_id: str

        :param update_record_request:
        :desc 
        :type update_record_request: json

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(ld_apis, "update_record")
        self._add_path_param(api_config, "recordId", record_id)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(update_record_request))

