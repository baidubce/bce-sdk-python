# !/usr/bin/env python
# coding=UTF-8
#
# Copyright 2022 Baidu, Inc.
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
This module provides a client class for dns.
"""

import json
import logging
from urllib.parse import quote

from baidubce import bce_base_client
from baidubce.services.dns.api.dns_api import dns_apis

_logger = logging.getLogger(__name__)


class DnsClient(bce_base_client.BceBaseClient):
    """
    dns base sdk client
    """

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)

    def add_line_group(self, add_line_group_request=None, client_token=None):
        """
        

        :param add_line_group_request:
        :desc 
        :type add_line_group_request: json

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串。
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(dns_apis, "add_line_group")
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(add_line_group_request))

    def create_paid_zone(self, create_paid_zone_request=None, client_token=None):
        """
        

        :param create_paid_zone_request:
        :desc 
        :type create_paid_zone_request: json

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串。
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(dns_apis, "create_paid_zone")
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(create_paid_zone_request))

    def create_record(self, zone_name=None, create_record_request=None, client_token=None):
        """
        

        :param zone_name:
        :desc 域名名称。
        :type zone_name: str

        :param create_record_request:
        :desc 
        :type create_record_request: json

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串。
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(dns_apis, "create_record")
        self._add_path_param(api_config, "zoneName", zone_name)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(create_record_request))

    def create_zone(self, create_zone_request=None, client_token=None):
        """
        

        :param create_zone_request:
        :desc 
        :type create_zone_request: json

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(dns_apis, "create_zone")
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(create_zone_request))

    def delete_line_group(self, line_id=None, client_token=None):
        """
        

        :param line_id:
        :desc 线路组id。
        :type line_id: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串。
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(dns_apis, "delete_line_group")
        self._add_path_param(api_config, "lineId", line_id)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def delete_record(self, zone_name=None, record_id=None, client_token=None):
        """
        

        :param zone_name:
        :desc 域名名称。
        :type zone_name: str

        :param record_id:
        :desc 解析记录id。
        :type record_id: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串。
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(dns_apis, "delete_record")
        self._add_path_param(api_config, "zoneName", zone_name)
        self._add_path_param(api_config, "recordId", record_id)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def delete_zone(self, zone_name=None, delete_zone_request=None, client_token=None):
        """
        

        :param zone_name:
        :desc 域名的名称。
        :type zone_name: str

        :param delete_zone_request:
        :desc 
        :type delete_zone_request: json

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串。
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(dns_apis, "delete_zone")
        self._add_path_param(api_config, "zoneName", zone_name)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(delete_zone_request))

    def list_line_group(self, list_line_group_request=None, marker=None, max_keys=None):
        """
        

        :param list_line_group_request:
        :desc 
        :type list_line_group_request: json

        :param marker:
        :desc 批量获取列表的查询的起始位置，是一个由系统生成的字符串。
        :type marker: str

        :param max_keys:
        :desc 每页包含的最大数量，最大数量通常不超过1000，缺省值为1000。
        :type max_keys: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(dns_apis, "list_line_group")
        self._add_query(api_config, "marker", marker)
        self._add_query(api_config, "maxKeys", max_keys)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(list_line_group_request))

    def list_record(self, zone_name=None, list_record_request=None, rr=None, id=None, marker=None, max_keys=None):
        """
        

        :param zone_name:
        :desc 域名的名称。
        :type zone_name: str

        :param list_record_request:
        :desc 
        :type list_record_request: json

        :param rr:
        :desc 主机记录，例如“www”。
        :type rr: str

        :param id:
        :desc 解析记录id。
        :type id: str

        :param marker:
        :desc 批量获取列表的查询的起始位置，是一个由系统生成的字符串。
        :type marker: str

        :param max_keys:
        :desc 每页包含的最大数量，最大数量通常不超过1000。缺省值为1000。
        :type max_keys: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(dns_apis, "list_record")
        self._add_path_param(api_config, "zoneName", zone_name)
        self._add_query(api_config, "rr", rr)
        self._add_query(api_config, "id", id)
        self._add_query(api_config, "marker", marker)
        self._add_query(api_config, "maxKeys", max_keys)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(list_record_request))

    def list_zone(self, list_zone_request=None, name=None, marker=None, max_keys=None):
        """
        

        :param list_zone_request:
        :desc 
        :type list_zone_request: json

        :param name:
        :desc 域名的名称，支持模糊搜索。
        :type name: str

        :param marker:
        :desc 批量获取列表的查询的起始位置，是一个由系统生成的字符串
        :type marker: str

        :param max_keys:
        :desc 每页包含的最大数量，最大数量通常不超过1000。缺省值为1000
        :type max_keys: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(dns_apis, "list_zone")
        self._add_query(api_config, "name", name)
        self._add_query(api_config, "marker", marker)
        self._add_query(api_config, "maxKeys", max_keys)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(list_zone_request))

    def renew_zone(self, name=None, renew_zone_request=None, client_token=None):
        """
        

        :param name:
        :desc 续费的域名。
        :type name: str

        :param renew_zone_request:
        :desc 
        :type renew_zone_request: json

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串。
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(dns_apis, "renew_zone")
        self._add_path_param(api_config, "name", name)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(renew_zone_request))

    def update_line_group(self, line_id=None, update_line_group_request=None, client_token=None):
        """
        

        :param line_id:
        :desc 线路组id。
        :type line_id: str

        :param update_line_group_request:
        :desc 
        :type update_line_group_request: json

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串。
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(dns_apis, "update_line_group")
        self._add_path_param(api_config, "lineId", line_id)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(update_line_group_request))

    def update_record(self, zone_name=None, record_id=None, update_record_request=None, client_token=None):
        """
        

        :param zone_name:
        :desc 域名名称。
        :type zone_name: str

        :param record_id:
        :desc 解析记录id。
        :type record_id: str

        :param update_record_request:
        :desc 
        :type update_record_request: json

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串。
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(dns_apis, "update_record")
        self._add_path_param(api_config, "zoneName", zone_name)
        self._add_path_param(api_config, "recordId", record_id)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(update_record_request))

    def update_record_disable(self, zone_name=None, record_id=None, client_token=None):
        """
        

        :param zone_name:
        :desc 域名名称。
        :type zone_name: str

        :param record_id:
        :desc 解析记录id。
        :type record_id: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串。
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(dns_apis, "update_record_disable")
        self._add_path_param(api_config, "zoneName", zone_name)
        self._add_path_param(api_config, "recordId", record_id)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def update_record_enable(self, zone_name=None, record_id=None, client_token=None):
        """
        

        :param zone_name:
        :desc 域名名称。
        :type zone_name: str

        :param record_id:
        :desc 解析记录id。
        :type record_id: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串。
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(dns_apis, "update_record_enable")
        self._add_path_param(api_config, "zoneName", zone_name)
        self._add_path_param(api_config, "recordId", record_id)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def upgrade_zone(self, upgrade_zone_request=None, client_token=None):
        """
        

        :param upgrade_zone_request:
        :desc 
        :type upgrade_zone_request: json

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串。
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(dns_apis, "upgrade_zone")
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(upgrade_zone_request))

