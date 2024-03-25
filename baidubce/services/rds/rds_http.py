#! usr/bin/python
# -*-coding:utf-8 -*-
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
This module provides a http client request
"""


import copy
import json
import uuid
import logging

import http.client

from baidubce import utils
from baidubce.services import rds
from baidubce.utils import required
from baidubce.auth import bce_v1_signer
from baidubce.http import http_headers
from baidubce.http import bce_http_client
from baidubce.exception import BceClientError
from baidubce.exception import BceServerError
from baidubce.bce_base_client import BceBaseClient
from baidubce.bce_client_configuration import BceClientConfiguration

_logger = logging.getLogger(__name__)


def _parse_result(http_response, response):
    """
     parse  http_response to response

    :param http_response:
        The HTTP response that needs to be converted
    :type  http_response:

    :param response:
        convert target response
    :type  response:

    :return:
    """
    if http_response.status / 100 == http.client.CONTINUE / 100:
        raise BceClientError('Can not handle 1xx http status code')
    bse = None
    body = http_response.read()
    if body:
        d = json.loads(body)

        if http_response.status / 100 != http.client.OK / 100:
            r_code = d['code']
            # 1000 means success
            if r_code != '1000':
                bse = BceServerError(d['message'],
                                     code=d['code'],
                                     request_id=d['requestId'])
            else:
                response.__dict__.update(
                    json.loads(body, object_hook=utils.dict_to_python_object).__dict__)
                http_response.close()
                return True
        elif http_response.status / 100 == http.client.OK / 100:
            try:
                response.__dict__.update(
                    json.loads(body, object_hook=utils.dict_to_python_object).__dict__)
                http_response.close()
            except Exception as alias:
                result = response.__dict__
                result["result"] = body
                response.__dict__.update(result)
                http_response.close()
            return True
    elif http_response.status / 100 == http.client.OK / 100:
        return True

    if bse is None:
        bse = BceServerError(http_response.reason, request_id=response.metadata.bce_request_id)
    bse.status_code = http_response.status
    raise bse  # pylint: disable-msg=E0702


class HttpRequest(BceBaseClient):
    """
     this is http client model

     :param BceBaseClient:
     :type  BceBaseClient:
    """

    def __init__(self, config):
        """
        :param config:
        :type config: rds_http.HttpRequest
        """
        if config is not None:
            self._check_config_type(config)
        BceBaseClient.__init__(self, config)

    @required(config=BceClientConfiguration)
    def _check_config_type(self, config):
        return True

    @staticmethod
    def _get_path_v1(config, function_name=None, key=None):
        """
         get path one

        :param config:
        :type config: rds_http.HttpRequest

        :param function_name:
        :type function_name: None

        :param key:
        :type key: None

        :return:
        """
        return utils.append_uri(rds.URL_PREFIX_V1, function_name, key)

    @staticmethod
    def _get_path_v2(config, function_name=None, key=None):
        """
        get path one

       :param config:
       :type config: rds_http.HttpRequest

       :param function_name:
       :type function_name: None

       :param key:
       :type key: None

       :return:
       """
        return utils.append_uri(rds.URL_PREFIX_V2, function_name, key)

    @staticmethod
    def _bce_rds_sign(credentials, http_method, path, headers, params, timestamp=0,
                      expiration_in_seconds=1800, headers_to_sign=None):
        """
        Request for signature

        :param credentials:
            Signature voucher
        :type credentials:

        :param http_method:
            get, post, put, delete
        :type http_method:

        :param path:
            Request path
        :type path:

        :param headers:
            Request header parameters
        :type headers:

        :param params:
            Request url parameters
        :type params:

        :param timestamp:
            Request time
        :type timestamp:

        :param expiration_in_seconds:
            Request expiration time
        :type expiration_in_seconds:

        :param headers_to_sign:
            Request headers sign
        :type headers_to_sign:

        :return:
        """
        headers_to_sign_list = [b"host",
                                b"content-md5",
                                b"content-length",
                                b"content-type"]

        if headers_to_sign is None or len(headers_to_sign) == 0:
            headers_to_sign = []
            for k in headers:
                k_lower = k.strip().lower()
                if k_lower.startswith(http_headers.BCE_PREFIX) or k_lower in headers_to_sign_list:
                    headers_to_sign.append(k_lower)
            headers_to_sign.sort()
        else:
            for k in headers:
                k_lower = k.strip().lower()
                if k_lower.startswith(http_headers.BCE_PREFIX):
                    headers_to_sign.append(k_lower)
            headers_to_sign.sort()

        return bce_v1_signer.sign(credentials,
                                  http_method,
                                  path,
                                  headers,
                                  params,
                                  timestamp,
                                  expiration_in_seconds,
                                  headers_to_sign)

    def _merge_config(self, config):
        """
        @param config:
        @return:
        """
        if config is None:
            return self.config
        else:
            self._check_config_type(config)
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, function_name=None, key=None, body=None, headers=None,
                      params=None, config=None, body_parser=None, api_version=1):
        """
        Send HTTP request

        :param http_method:
            get, post, put, delete
         :type http_method:

        :param function_name:
            Request Method Name
        :type function_name:

        :param key:
            Public Key
        :type key:

        :param body:
            For non get requests with parameters in the body
        :type body:

        :param headers:
            Request header parameters
        :type headers:

        :param params:
            Request URL parameters
        :type params:

        :param config:
        :type config:
        :param body_parser:
            body_parser paramter
        type body_parser:

        :param api_version:
            request http version， default v1
        :type body_parser:
        :return:
        """
        if params is None:
            params = {"clientToken": uuid.uuid4()}
        config = self._merge_config(config)
        path = {
            1: HttpRequest._get_path_v1,
            2: HttpRequest._get_path_v2,
        }[api_version](config, function_name, key)

        if body_parser is None:
            body_parser = _parse_result
        base_header = {b'Accept': b'*/*', b'Content-Type': b'application/json;charset=utf-8'}
        if headers is None:
            headers = base_header
        else:
            headers.update(base_header)
        return bce_http_client.send_request(config, HttpRequest._bce_rds_sign, [body_parser],
                                            http_method, path, body, headers, params)
