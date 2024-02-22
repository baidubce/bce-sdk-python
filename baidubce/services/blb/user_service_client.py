# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.

"""
This module provides a client class for User Service.
"""

import copy
import json
import logging
import uuid
import sys

from baidubce import bce_base_client
from baidubce.auth import bce_v1_signer
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods
from baidubce import utils
from baidubce.utils import required
from baidubce import compat

if sys.version < '3':
    reload(sys)
    sys.setdefaultencoding('utf-8')

_logger = logging.getLogger(__name__)


class UserServiceClient(bce_base_client.BceBaseClient):
    """
    BLB base sdk client
    """
    version = b'/v1'

    def __init__(self, config=None):
        """初始化BceClient对象。

        Args:
            config (dict，可选参数，默认值为None): BceClient的配置字典。

        """
        bce_base_client.BceBaseClient.__init__(self, config)

    def _merge_config(self, config=None):
        """
        :param config:
        :type config: baidubce.BceClientConfiguration
        :return:
        """
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, path,
                      body=None, headers=None, params=None,
                      config=None, body_parser=None):
        """
        发送请求方法

        Args:
            http_method (str): 请求的方法，可选值包括"GET", "POST", "PUT", "DELETE"。
            path (str): 请求路径。
            body (Any, optional): 请求体内容，可以是任意类型。默认值为None。
            headers (dict[bytes, bytes], optional): 请求头信息，以键值对形式存储。默认值为None。
            params (dict[str, str], optional): 请求参数，以键值对形式存储。默认值为None。
            config (dict, optional): 配置信息。
            body_parser (func, optional): 解析响应体的函数。如果为空则默认使用parse_json方法。

        Returns:
            Any: 返回请求返回的内容。
        """
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json
        if headers is None:
            headers = {b'Accept': b'*/*',
                       b'Content-Type': b'application/json;charset=utf-8'}
        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, path, body, headers, params)

    @required(name=(bytes, str),
              serviceName=(bytes, str),
              instanceId=(bytes, str))
    def create_user_service(self, name, desc, serviceName,
                            instanceId, client_token=None,
                            authList=None, config=None):
        """
        Create user service for specified LoadBalancer

        :param name:
                name of user service
        :type name: string

        :param desc:
                description of user service
        :type desc: string

        :param serviceName:
                The name of service
        :type serviceName: string

        :param instanceId:
                The id of LoadBalancer
        :type instanceId: string

        :param client_token:
                If the clientToken is not specified by the user,
                a random String generated by default algorithm will be used.
        :type client_token: string

        :param authList:
                List of Auth information
        :type service: list<Auth>

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = utils.append_uri(self.version, 'service')
        params = {}

        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        body = {}
        if desc is not None:
            body['description'] = compat.convert_to_string(desc)
        body['name'] = name
        body['serviceName'] = serviceName
        body['instanceId'] = instanceId
        if authList is not None:
            body['authList'] = authList
        else:
            body['authList'] = [{"uid": "*", "auth": "deny"}]

        return self._send_request(http_methods.POST, path,
                                  body=json.dumps(body), params=params,
                                  config=config)

    @required(service=(bytes, str))
    def update_user_service(self, name=None, desc=None, service=None,
                            client_token=None, config=None):
        """
        Update user service for specified LoadBalancer

        :param name:
                name of user service
        :type name: string

        :param desc:
                description of user service
        :type desc: string

        :param service:
                domain name of the service
        :type service: string

        :param client_token:
                If the clientToken is not specified by the user,
                a random String generated by default algorithm will be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = utils.append_uri(self.version, 'service', service)
        params = {}

        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        params[b'modifyAttribute'] = None

        body = {}
        if desc is not None:
            body['description'] = compat.convert_to_string(desc)
        if name is not None:
            body["name"] = name

        return self._send_request(http_methods.PUT, path,
                                  body=json.dumps(body), params=params,
                                  config=config)

    @required(service=(bytes, str),
              instanceId=(bytes, str))
    def user_service_bind_instance(self, instanceId, service,
                                   client_token=None, config=None):
        """
        Bind a specified LoadBalancer to user service

        :param instanceId:
                The id of LoadBalancer
        :type instanceId: string

        :param service:
                domain name of the service
        :type service: string

        :param client_token:
                If the clientToken is not specified by the user,
                a random String generated by default algorithm will be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        path = utils.append_uri(self.version, 'service', service)
        params = {}

        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        params[b'bind'] = None

        body = {}
        body['instanceId'] = instanceId

        return self._send_request(http_methods.PUT, path,
                                  body=json.dumps(body), params=params,
                                  config=config)

    @required(service=(bytes, str))
    def user_service_unbind_instance(self, service,
                                     client_token=None, config=None):
        """
        Unbind a specified LoadBalancer from user service

        :param service:
                domain name of the service
        :type service: string

        :param client_token:
                If the clientToken is not specified by the user,
                a random String generated by default algorithm will be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        path = utils.append_uri(self.version, 'service', service)
        params = {}

        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        params[b'unbind'] = None

        body = {}

        return self._send_request(http_methods.PUT, path,
                                  body=json.dumps(body), params=params,
                                  config=config)

    @required(service=(bytes, str),
              authList=list)
    def user_service_add_auth(self, service,
                              authList, client_token=None, config=None):
        """
        Add a new auth information to user service

        :param service:
                domain name of the service
        :type service: string

        :param authList:
                List of Auth information
        :type service: list<Auth>

        :param client_token:
                If the clientToken is not specified by the user,
                a random String generated by default algorithm will be used.
        :type client_token: string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        path = utils.append_uri(self.version, 'service', service)
        params = {}

        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        params[b'addAuth'] = None

        body = {}
        body['authList'] = authList
        return self._send_request(http_methods.PUT, path,
                                  body=json.dumps(body), params=params,
                                  config=config)

    @required(service=(bytes, str),
              authList=list)
    def user_service_edit_auth(self, service,
                               authList, client_token=None, config=None):
        """
        Edit auth information to user service
        :param service:
                domain name of the service
        :type service: string

        :param authList:
                List of Auth information
        :type service: list<Auth>

        :param client_token:
                If the clientToken is not specified by the user,
                a random String generated by default algorithm will be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        path = utils.append_uri(self.version, 'service', service)
        params = {}

        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        params[b'editAuth'] = None

        body = {}
        body['authList'] = authList

        return self._send_request(http_methods.PUT, path,
                                  body=json.dumps(body), params=params,
                                  config=config)

    @required(service=(bytes, str),
              uidList=list)
    def user_service_remove_auth(self, service,
                                 uidList, client_token=None, config=None):
        """
        Remove auth information from user service

        :param service:
                domain name of the service
        :type service: string

        :param uidList:
                List of uid
        :type service: list<String>

        :param client_token:
                If the clientToken is not specified by the user,
                a random String generated by default algorithm will be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        path = utils.append_uri(self.version, 'service', service)
        params = {}

        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        params[b'removeAuth'] = None

        body = {}
        body['uidList'] = uidList

        return self._send_request(http_methods.PUT, path,
                                  body=json.dumps(body), params=params,
                                  config=config)

    def get_user_service_list(self, marker=None,
                              maxKeys=None, client_token=None, config=None):
        """
        Get list of user service

        :param marker:
                Mark the start position of query
        :type service: string

        :param maxKeys:
               Max number of one page, default number is 1000
        :type service: integer

        :param client_token:
                If the clientToken is not specified by the user,
                a random String generated by default algorithm will be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        path = utils.append_uri(self.version, b'service')
        params = {}

        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        if marker is not None:
            params[b'marker'] = marker

        if maxKeys is not None:
            params[b'maxKeys'] = maxKeys
        else:
            params[b'maxKeys'] = 1000

        body = {}
        return self._send_request(http_methods.GET, path,
                                  body=json.dumps(body), params=params,
                                  config=config)

    @required(service=(bytes, str))
    def get_user_service_detail(self, service,
                                client_token=None, config=None):
        """
        Get user service detail information

        :param service:
                domain name of the service
        :type service: string

        :param client_token:
                If the clientToken is not specified by the user,
                a random String generated by default algorithm will be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        path = utils.append_uri(self.version, b'service', service)
        params = {}

        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        body = {}
        return self._send_request(http_methods.GET, path,
                                  body=json.dumps(body), params=params,
                                  config=config)

    @required(service=(bytes, str))
    def delete_user_service(self, service,
                            client_token=None, config=None):
        """
        Delete user service

        :param service:
                domain name of the service
        :type service: string

        :param client_token:
                If the clientToken is not specified by the user,
                a random String generated by default algorithm will be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """

        path = utils.append_uri(self.version, 'service', service)
        params = {}

        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        body = {}
        return self._send_request(http_methods.DELETE, path,
                                  body=json.dumps(body), params=params,
                                  config=config)


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.

    :return:
    :rtype string
    """
    return str(uuid.uuid4())


generate_client_token = generate_client_token_by_uuid
