# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
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
This module provides a client class for CDN.
"""

import copy
import logging
import uuid

from baidubce import bce_base_client
from baidubce.auth import bce_v1_signer
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods
from baidubce.utils import required


_logger = logging.getLogger(__name__)


class DumapClient(bce_base_client.BceBaseClient):
    """
    DumapClient
    """
    X_APP_ID = 'x-app-id'

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)

    @required(app_id=str, uri=str, params=dict)
    def call_open_api(self, app_id, uri, params, config=None):
        """
        call open_api
        :param app_id: app_id
        :type app_id: string
        :param uri: open api uri
        :type uri: string
        :param params: dict
        :type params:request params

        :param config: None
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype: baidubce.bce_response.BceResponse
                """
        return self._send_request(
            http_methods.GET,
            uri,
            params=params,
            headers={DumapClient.X_APP_ID: app_id},
            config=config)

    @staticmethod
    def _merge_config(self, config):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(
            self, http_method, path,
            body=None, headers=None, params=None,
            config=None):
        config = self._merge_config(self, config)
        headers['x-bce-request-id'] = uuid.uuid4()

        return bce_http_client.send_request(
            config, sign_wrapper(['host', 'x-bce-date', 'x-bce-request-id', 'x-app-id']),
            [handler.parse_error, parse_none],
            http_method, path, body, headers, params)


def sign_wrapper(headers_to_sign):
    """wrapper the bce_v1_signer.sign()."""
    def _wrapper(credentials, http_method, path, headers, params):
        return bce_v1_signer.sign(credentials, http_method, path, headers, params,
                                  headers_to_sign=headers_to_sign)

    return _wrapper


def parse_none(http_response, response):
    """If the body is not empty, convert it to a python object and set as the value of
    response.body. http_response is always closed if no error occurs.

    :param http_response: the http_response object returned by HTTPConnection.getresponse()
    :type http_response: httplib.HTTPResponse

    :param response: general response object which will be returned to the caller
    :type response: baidubce.BceResponse

    :return: always true
    :rtype bool
    """
    body = http_response.read()
    if body:
        response.body=body
    http_response.close()
    return True