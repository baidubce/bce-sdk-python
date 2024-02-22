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
This module provides a client class for csn.
"""

import json
import logging
from urllib.parse import quote

from baidubce import bce_base_client
from baidubce.services.csn.csn_api import csn_apis

_logger = logging.getLogger(__name__)


class CsnClient(bce_base_client.BceBaseClient):
    """
    csn base sdk client
    """

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)

    def attach_instance(self, csn_id, instance_type, instance_id, instance_region,
                        instance_account_id=None, client_token=None):
        """
        ​将网络实例加载进云智能网。

        :param csn_id:
        :desc 云智能网的ID
        :type csn_id: str

        :param instance_type:
        :desc 实例类型
        :type instance_type: str

        :param instance_id:
        :desc 实例ID
        :type instance_id: str

        :param instance_region:
        :desc 实例所属的地域
        :type instance_region: str

        :param instance_account_id:
        :desc 实例所属的账号ID
        :type instance_account_id: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串，详见ClientToken幂等性
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "attach_instance")
        self._add_path_param(api_config, "csnId", csn_id)
        self._add_query(api_config, "attach", '')
        self._add_query(api_config, "clientToken", client_token)
        body = {
            "instanceType": instance_type,
            "instanceId": instance_id,
            "instanceRegion": instance_region,
            "instanceAccountId": instance_account_id
        }

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(body))

    def bind_csn_bp(self, csn_bp_id, csn_id, client_token=None):
        """
        带宽包绑定云智能网。

        :param csn_bp_id:
        :desc 带宽包的ID
        :type csn_bp_id: str

        :param csn_id:
        :desc 云智能网ID
        :type csn_id

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "bind_csn_bp")
        self._add_path_param(api_config, "csnBpId", csn_bp_id)
        self._add_query(api_config, "bind", '')
        self._add_query(api_config, "clientToken", client_token)
        body = {
            "csnId": csn_id,
        }

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(body))

    def create_association(self, csn_rt_id, attach_id, description=None, client_token=None):
        """
        ​创建路由表的关联关系。

        :param csn_rt_id:
        :desc 云智能网路由表的ID
        :type csn_rt_id: str

        :param attach_id:
        :desc 网络实例在云智能网中的身份ID
        :type attach_id: str
        
        :param description:
        :desc 路由表的关联关系的描述
        :type description: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串，详见ClientToken幂等性
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "create_association")
        self._add_path_param(api_config, "csnRtId", csn_rt_id)
        self._add_query(api_config, "clientToken", client_token)
        body = {
            'attachId': attach_id,
            'description': description,
        }

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(body))

    def create_csn(self, name, description=None, client_token=None):
        """
        ​创建云智能网。

        :param name:
        :desc 云智能网的名称
        :type name: str

        :param description:
        :desc 云智能网的描述
        :type description: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串，详见ClientToken幂等性
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "create_csn")
        self._add_query(api_config, "clientToken", client_token)
        body = {
            'name': name,
            'description': description,
        }
        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(body))

    def create_csn_bp(self, name, bandwidth, geographic_a, geographic_b, billing,
                      interwork_type=None, client_token=None):
        """
        ​创建云智能网共享带宽包。

        :param name:
        :desc 带宽包的名称
        :type name: str

        :param interwork_type:
        :desc 云智能网共享带宽包的互通类型，取值：
        :type interwork_type: str

        :param bandwidth:
        :desc 带宽包的带宽，单位Mbps
        :type bandwidth: int

        :param geographic_a:
        :desc 带宽包的A地
        :type geographic_a: str

        :param geographic_b:
        :desc 带宽包的B地
        :type geographic_b: str

        :param billing:
        :desc 带宽包的计费信息
        :type billing: Billing

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "create_csn_bp")
        self._add_query(api_config, "clientToken", client_token)
        body = {
            'name': name,
            'interworkType': interwork_type,
            'bandwidth': bandwidth,
            'geographicA': geographic_a,
            'geographicB': geographic_b,
            'billing': billing.__dict__,
        }

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(body))

    def create_csn_bp_limit(self, csn_bp_id, local_region, peer_region, bandwidth, client_token=None):
        """
        创建带宽包中两个地域间的地域带宽。

        :param csn_bp_id:
        :desc 带宽包的ID
        :type csn_bp_id: str

        :param local_region:
        :desc 地域带宽的本端region，云边互通场景中表示云端region
        :type local_region: str
        
        :param peer_region:
        :desc 地域带宽的对端region，云边互通场景中表示边缘region
        :type peer_region: str
        
        :param bandwidth:
        :desc 地域带宽的带宽值
        :type bandwidth: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "create_csn_bp_limit")
        self._add_path_param(api_config, "csnBpId", csn_bp_id)
        self._add_query(api_config, "clientToken", client_token)
        body = {
            'localRegion': local_region,
            'peerRegion': peer_region,
            'bandwidth': bandwidth,
        }
        
        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(body))

    def create_propagation(self, csn_rt_id, attach_id, description=None, client_token=None):
        """
        创建路由表的学习关系。

        :param csn_rt_id:
        :desc 云智能网路由表的ID
        :type csn_rt_id: str

        :param attach_id:
        :desc 网络实例在云智能网中的身份的ID
        :type create_propagation_request: json

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串，详见ClientToken幂等性
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "create_propagation")
        self._add_path_param(api_config, "csnRtId", csn_rt_id)
        self._add_query(api_config, "clientToken", client_token)

        body = {
            'attachId': attach_id,
            'description': description,
        }

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(body))

    def create_route_rule(self, csn_rt_id, attach_id, destAddress, routeType="custom", client_token=None):
        """
        添加云智能网路由表的路由条目。

        :param csn_rt_id:
        :desc 云智能网路由表的ID
        :type csn_rt_id: str

        :param attach_id:
        :desc 网络实例在云智能网中的身份的ID
        :type attach_id: str

        :param destAddress:
        :desc 目的地址
        :type destAddress: str

        :param routeType:
        :desc 路由类型，目前只支持"custom"
        :type routeType: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串，详见ClientToken幂等性
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "create_route_rule")
        self._add_path_param(api_config, "csnRtId", csn_rt_id)
        self._add_query(api_config, "clientToken", client_token)

        body = {
            "attachId": attach_id,
            "destAddress": destAddress,
            "routeType": routeType,
        }

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(body))

    def delete_association(self, csn_rt_id=None, attach_id=None, client_token=None):
        """
        删除云智能网路由表的关联关系。

        :param csn_rt_id:
        :desc 路由表的ID
        :type csn_rt_id: str

        :param attach_id:
        :desc 网络实例在云智能网中的身份ID
        :type attach_id: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串，详见ClientToken幂等性
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "delete_association")
        self._add_path_param(api_config, "csnRtId", csn_rt_id)
        self._add_path_param(api_config, "attachId", attach_id)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def delete_csn(self, csn_id, client_token=None):
        """
        ​删除云智能网。  已经加载了网络实例的云智能网不能直接删除，必须先卸载实例。

        :param csn_id:
        :desc 云智能网的ID
        :type csn_id: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串，详见ClientToken幂等性
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "delete_csn")
        self._add_path_param(api_config, "csnId", csn_id)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def delete_csn_bp(self, csn_bp_id, client_token=None):
        """
        ​删除带宽包。

        :param csn_bp_id:
        :desc 带宽包的ID
        :type csn_bp_id: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "delete_csn_bp")
        self._add_path_param(api_config, "csnBpId", csn_bp_id)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def delete_csn_bp_limit(self, csn_bp_id, local_region, peer_region, client_token=None):
        """
        ​删除带宽包中两个地域间的地域带宽。

        :param csn_bp_id:
        :desc 带宽包的ID
        :type csn_bp_id: str

        :param local_region:
        :desc 地域带宽的本端region，云边互通场景中表示云端region
        :type local_region: str
        
        :param peer_region:
        :desc 地域带宽的对端region，云边互通场景中表示边缘region
        :type peer_region: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "delete_csn_bp_limit")
        self._add_path_param(api_config, "csnBpId", csn_bp_id)
        self._add_query(api_config, "clientToken", client_token)
        body = {
            'localRegion': local_region,
            'peerRegion': peer_region,
        }
        
        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(body))

    def delete_propagation(self, csn_rt_id, attach_id, client_token=None):
        """
        ​删除云智能网路由表的学习关系。

        :param csn_rt_id:
        :desc 路由表的ID
        :type csn_rt_id: str

        :param attach_id:
        :desc 网络实例在云智能网中的身份ID
        :type attach_id: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串，详见ClientToken幂等性
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "delete_propagation")
        self._add_path_param(api_config, "csnRtId", csn_rt_id)
        self._add_path_param(api_config, "attachId", attach_id)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def delete_route_rule(self, csn_rt_id=None, csn_rt_rule_id=None, client_token=None):
        """
        ​删除云智能网路由表的指定路由条目。

        :param csn_rt_id:
        :desc 路由表的ID
        :type csn_rt_id: str

        :param csn_rt_rule_id:
        :desc 路由条目的ID
        :type csn_rt_rule_id: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串，详见ClientToken幂等性
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "delete_route_rule")
        self._add_path_param(api_config, "csnRtId", csn_rt_id)
        self._add_path_param(api_config, "csnRtRuleId", csn_rt_rule_id)
        self._add_query(api_config, "clientToken", client_token)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def detach_instance(self, csn_id, instance_type, instance_id, instance_region,
                        instance_account_id=None, client_token=None):
        """
        ​从云智能网中移出指定的网络实例。

        :param csn_id:
        :desc 云智能网的ID
        :type csn_id: str

        :param instance_type:
        :desc 实例类型
        :type instance_type: str

        :param instance_id:
        :desc 实例ID
        :type instance_id: str

        :param instance_region:
        :desc 实例所属的地域
        :type instance_region: str

        :param instance_account_id:
        :desc 实例所属的账号ID
        :type instance_account_id: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串，详见ClientToken幂等性
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "detach_instance")
        self._add_path_param(api_config, "csnId", csn_id)
        self._add_query(api_config, "detach", '')
        self._add_query(api_config, "clientToken", client_token)
        body = {
            "instanceType": instance_type,
            "instanceId": instance_id,
            "instanceRegion": instance_region,
            "instanceAccountId": instance_account_id
        }

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(body))

    def get_csn(self, csn_id):
        """
        查询云智能网详情。

        :param csn_id:
        :desc csnId
        :type csn_id: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "get_csn")
        self._add_path_param(api_config, "csnId", csn_id)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def get_csn_bp(self, csn_bp_id=None):
        """
        查询指定云智能网带宽包详情。

        :param csn_bp_id:
        :desc 带宽包的ID
        :type csn_bp_id: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "get_csn_bp")
        self._add_path_param(api_config, "csnBpId", csn_bp_id)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def list_association(self, csn_rt_id=None):
        """
        查询指定云智能网路由表的关联关系。

        :param csn_rt_id:
        :desc 云智能网路由表的ID
        :type csn_rt_id: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "list_association")
        self._add_path_param(api_config, "csnRtId", csn_rt_id)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def list_csn(self, marker=None, max_keys=None):
        """
        查询云智能网列表。

        :param marker:
        :desc 批量获取列表的查询的起始位置
        :type marker: str

        :param max_keys:
        :desc 每页包含的最大数量，最大数量不超过1000，缺省值为1000
        :type max_keys: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "list_csn")
        self._add_query(api_config, "marker", marker)
        self._add_query(api_config, "maxKeys", max_keys)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def list_csn_bp(self, marker=None, max_keys=None):
        """
        查询云智能网带宽包列表。

        :param marker:
        :desc 批量获取列表的查询的起始位置，是一个由系统生成的字符串
        :type marker: str

        :param max_keys:
        :desc 每页包含的最大数量，最大数量不超过1000，缺省值为1000
        :type max_keys: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "list_csn_bp")
        self._add_query(api_config, "marker", marker)
        self._add_query(api_config, "maxKeys", max_keys)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def list_csn_bp_limit(self, csn_bp_id=None):
        """
        查询带宽包的地域带宽列表。

        :param csn_bp_id:
        :desc
        :type csn_bp_id: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "list_csn_bp_limit")
        self._add_path_param(api_config, "csnBpId", csn_bp_id)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def list_csn_bp_limit_by_csn_id(self, csn_id):
        """
        查询云智能网的地域带宽列表。

        :param csn_id:
        :desc 云智能网的ID
        :type csn_id: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "list_csn_bp_limit_by_csn_id")
        self._add_path_param(api_config, "csnId", csn_id)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def list_instance(self, csn_id, marker=None, max_keys=None):
        """
        查询指定云智能网下加载的网络实例信息。

        :param csn_id:
        :desc 云智能网的ID
        :type csn_id: str

        :param marker:
        :desc 批量获取列表的查询的起始位置
        :type marker: str

        :param max_keys:
        :desc 每页包含的最大数量，最大数量不超过1000，缺省值为1000
        :type max_keys: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "list_instance")
        self._add_path_param(api_config, "csnId", csn_id)
        self._add_query(api_config, "marker", marker)
        self._add_query(api_config, "maxKeys", max_keys)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def list_propagation(self, csn_rt_id):
        """
        查询指定云智能网路由表的学习关系。

        :param csn_rt_id:
        :desc 云智能网路由表的ID
        :type csn_rt_id: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "list_propagation")
        self._add_path_param(api_config, "csnRtId", csn_rt_id)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def list_route_rule(self, csn_rt_id, marker=None, max_keys=None):
        """
        查询指定云智能网路由表的路由条目。

        :param csn_rt_id:
        :desc 云智能网路由表的ID
        :type csn_rt_id: str

        :param marker:
        :desc 批量获取列表的查询的起始位置，是一个由系统生成的字符串
        :type marker: str

        :param max_keys:
        :desc 每页包含的最大数量，最大数量不超过1000。缺省值为1000
        :type max_keys: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "list_route_rule")
        self._add_path_param(api_config, "csnRtId", csn_rt_id)
        self._add_query(api_config, "marker", marker)
        self._add_query(api_config, "maxKeys", max_keys)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def list_route_table(self, csn_id, marker=None, max_keys=None):
        """
        查询云智能网的路由表列表。

        :param csn_id:
        :desc 云智能网的ID
        :type csn_id: str

        :param marker:
        :desc 批量获取列表的查询的起始位置，是一个由系统生成的字符串
        :type marker: str

        :param max_keys:
        :desc 每页包含的最大数量，最大数量不超过1000，缺省值为1000
        :type max_keys: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "list_route_table")
        self._add_path_param(api_config, "csnId", csn_id)
        self._add_query(api_config, "marker", marker)
        self._add_query(api_config, "maxKeys", max_keys)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def list_tgw(self, csn_id=None, marker=None, max_keys=None):
        """
        查询云智能网TGW列表。

        :param csn_id:
        :desc 云智能网的ID
        :type csn_id: str

        :param marker:
        :desc 批量获取列表的查询的起始位置，是一个由系统生成的字符串
        :type marker: str

        :param max_keys:
        :desc 每页包含的最大数量，最大数量不超过1000，缺省值为1000
        :type max_keys: int

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "list_tgw")
        self._add_path_param(api_config, "csnId", csn_id)
        self._add_query(api_config, "marker", marker)
        self._add_query(api_config, "maxKeys", max_keys)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def list_tgw_rule(self, csn_id=None, tgw_id=None, marker=None, max_keys=None):
        """
        查询指定TGW的路由条目。

        :param csn_id:
        :desc 云智能网的ID
        :type csn_id: str

        :param tgw_id:
        :desc TGW的ID
        :type tgw_id: str

        :param marker:
        :desc 批量获取列表的查询的起始位置，是一个由系统生成的字符串
        :type marker: str

        :param max_keys:
        :desc 每页包含的最大数量，最大数量不超过1000，缺省值为1000
        :type max_keys: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "list_tgw_rule")
        self._add_path_param(api_config, "csnId", csn_id)
        self._add_path_param(api_config, "tgwId", tgw_id)
        self._add_query(api_config, "marker", marker)
        self._add_query(api_config, "maxKeys", max_keys)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"])

    def resize_csn_bp(self, csn_bp_id, bandwidth, client_token=None):
        """
        带宽包的带宽升降级。

        :param csn_bp_id:
        :desc 带宽包的ID
        :type csn_bp_id: str

        :param bandwidth:
        :desc 升降级的带宽值，最大值为10000
        :type bandwidth: int

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "resize_csn_bp")
        self._add_path_param(api_config, "csnBpId", csn_bp_id)
        self._add_query(api_config, "resize", '')
        self._add_query(api_config, "clientToken", client_token)
        body = {
            'bandwidth': bandwidth,
        }

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(body))

    def unbind_csn_bp(self, csn_bp_id, csn_id, client_token=None):
        """
        带宽包解绑云智能网。

        :param csn_bp_id:
        :desc 带宽包的ID
        :type csn_bp_id: str

        :param csn_id:
        :desc 云智能网ID
        :type csn_id

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "unbind_csn_bp")
        self._add_path_param(api_config, "csnBpId", csn_bp_id)
        self._add_query(api_config, "unbind", '')
        self._add_query(api_config, "clientToken", client_token)
        body = {
            'csnId': csn_id,
        }

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(body))

    def update_csn(self, csn_id, name=None, description=None, client_token=None):
        """
        ​更新云智能网。  更新云智能网的名称和描述。

        :param csn_id:
        :desc 云智能网ID
        :type csn_id: str

        :param name:
        :desc 云智能网的名称
        :type name: str

        :param description:
        :desc 云智能网的描述
        :type description: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串，详见ClientToken幂等性
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "update_csn")
        self._add_path_param(api_config, "csnId", csn_id)
        self._add_query(api_config, "clientToken", client_token)
        body = {
            "name": name,
            "description": description
        }
        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(body))

    def update_csn_bp(self, csn_bp_id, name=None, client_token=None):
        """
        ​更新带宽包的名称信息。

        :param csn_bp_id:
        :desc 带宽包的ID
        :type csn_bp_id: str

        :param name:
        :desc 带宽包的名称
        :type name: str

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "update_csn_bp")
        self._add_path_param(api_config, "csnBpId", csn_bp_id)
        self._add_query(api_config, "clientToken", client_token)
        body = {
            "name": name
        }

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(body))

    def update_csn_bp_limit(self, csn_bp_id, local_region, peer_region, bandwidth, client_token=None):
        """
        ​更新带宽包中两个地域间的地域带宽。

        :param csn_bp_id:
        :desc 带宽包的ID
        :type csn_bp_id: str

        :param local_region:
        :desc 地域带宽的本端region，云边互通场景中表示云端region
        :type local_region: str
        
        :param peer_region:
        :desc 地域带宽的对端region，云边互通场景中表示边缘region
        :type peer_region: str
        
        :param bandwidth:
        :desc 地域带宽的带宽值
        :type bandwidth: int

        :param client_token:
        :desc 幂等性Token，是一个长度不超过64位的ASCII字符串
        :type client_token: str

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "update_csn_bp_limit")
        self._add_path_param(api_config, "csnBpId", csn_bp_id)
        self._add_query(api_config, "clientToken", client_token)
        body = {
            'localRegion': local_region,
            'peerRegion': peer_region,
            'bandwidth': bandwidth,
        }

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(body))

    def update_tgw(self, csn_id=None, tgw_id=None, update_tgw_request=None):
        """
        更新TGW的名称、描述。

        :param csn_id:
        :desc 云智能网的ID
        :type csn_id: str

        :param tgw_id:
        :desc TGW实例的ID
        :type tgw_id: str

        :param update_tgw_request:
        :desc
        :type update_tgw_request: json

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        api_config = self._get_config(csn_apis, "update_tgw")
        self._add_path_param(api_config, "csnId", csn_id)
        self._add_path_param(api_config, "tgwId", tgw_id)

        return self._send_request(api_config["method"], quote(api_config["path"]).encode("utf8"), api_config["headers"],
                                  api_config["queries"], json.dumps(update_tgw_request))

