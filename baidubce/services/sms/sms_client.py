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
This module provides a client class for BMR.
"""

import copy
import logging
import json

import baidubce
from baidubce.auth import bce_v1_signer
from baidubce import bce_base_client
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods
from baidubce.utils import required


_logger = logging.getLogger(__name__)


class SmsClient(bce_base_client.BceBaseClient):
    """
    Sms sdk client
    """

    prefix = '/v1'

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)

    @required(content_var=(str, unicode),
              receiver=list,
              template_id=(str, unicode))
    def send_message(self, content_var, receiver, template_id):
        """
        Create cluster

        :param content_var
        :type string

        :param receiver
        :type dict

        :param template_id
        :type string

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = '/message'
        params = None
        body = {
            'contentVar' : content_var,
            'receiver' : receiver,
            'templateId' : template_id
        }

        return self._send_request(http_methods.POST, path, params=params, body=json.dumps(body))

    @required(message_id=(str, unicode))
    def get_message_info(self, message_id):
        path = '/message/' + message_id
        params = None
        return self._send_request(http_methods.GET, path, params=params, body=None)

    def get_quota(self):
        path = '/quota'
        params = None
        return self._send_request(http_methods.GET, path, params=params, body=None)

    def _merge_config(self, config=None):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, path,
                      body=None, headers=None, params=None,
                      config=None, body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json

        return bce_http_client.send_request(
            config, sign_wrapper(['host', 'x-bce-date']), [handler.parse_error, body_parser],
            http_method, SmsClient.prefix + path, body, headers, params)


def sign_wrapper(headers_to_sign):
    """wrapper the bce_v1_signer.sign()."""
    def _wrapper(credentials, http_method, path, headers, params):
        return bce_v1_signer.sign(credentials, http_method, path, headers, params,
                                  headers_to_sign=headers_to_sign)
    return _wrapper

