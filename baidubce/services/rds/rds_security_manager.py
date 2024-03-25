#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
This module defines RdsSecurityManager interface
"""

import json

from baidubce.utils import required
from baidubce.http import http_methods
from baidubce.services.rds import rds_http
from baidubce.services.rds.models import rds_security_model
from baidubce.services.rds.custom.requestparam import rds_request_param_object as request_param


class RdsSecurityManager(rds_http.HttpRequest):
    """
      this is RdsSecurityManager openApi interface
     :param rds_http.HttpRequest:
    """

    def __init__(self, config):
        """
        :param config:
        :type config: baidubce.BceClientConfiguration
        """

        rds_http.HttpRequest.__init__(self, config)

    @required(instance_id=(str))
    def whit_list(self, instance_id, config=None):
        """
         query whit list

        :param instance_id: the specified instance id
        :type instance_id: str

        :param config:
        :type config: baidubce.BceClientConfiguration
        :return:
        """

        return rds_security_model.WhiteList(
            self._send_request(http_method=http_methods.GET,
                               function_name='instance',
                               key='/' + instance_id + '/securityIp',
                               config=config,
                               api_version=1))

    @required(instance_id=(str), security_ips=(list), e_tag=(str))
    def update_whit_list(self, instance_id, security_ips, e_tag, config=None):
        """
         update whit list

        :param instance_id: the specified instance id
        :type instance_id: str

        :param security_ips:
            Set the IP addresses of the whitelist, separated by commas (,)
            for example:  [ "xx.xx.xx.xx","xx.xx.xx.xx" ]
        :type security_ips: list

        :param e_tag:
            The ETag value is obtained by querying the interface
        :type e_tag: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        data = {"securityIps": security_ips}
        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key='/' + instance_id + '/securityIp',
                                  headers={b"x-bce-if-match": e_tag},
                                  body=json.dumps(data, cls=request_param.JsonWrapper),
                                  config=config,
                                  api_version=1)

    @required(instance_id=(str))
    def obtain_ssl_encrypted_info(self, instance_id, config=None):
        """
        obtain ssl encrypted info

        :param instance_id: the specified instance id
        :type instance_id: str

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        return rds_security_model.SslState(
            self._send_request(http_method=http_methods.GET,
                               function_name='instance',
                               key='/ssl/' + instance_id,
                               config=config,
                               api_version=1))

    @required(instance_id=(str), status=(bool))
    def set_ssl_status(self, instance_id, status, config=None):
        """
         Enable and disable ssl

        :param instance_id:
            the specified instance id
        :type instance_id: str

        :param status:  true: open ssl, false: close ssl
        :type status: bool

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        """

        data = {"sslAccessible": status}
        return self._send_request(http_method=http_methods.PUT,
                                  function_name='instance',
                                  key='/ssl/' + instance_id,
                                  params={"sslAccessible": None},
                                  body=json.dumps(data),
                                  config=config,
                                  api_version=1)

    def obtain_ssl_ca(self, config=None):
        """
         Obtaining a ca Certificate

        :param config:
        ：type config: baidubce.BceClientConfiguration
        :return:
        """

        return self._send_request(http_method=http_methods.GET,
                                  function_name='instance',
                                  key='/ssl/static/ca/',
                                  config=config,
                                  api_version=1)
