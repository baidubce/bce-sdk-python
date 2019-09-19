# Copyright 2017 Baidu, Inc.
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
This module provides a client class for VCA.
"""

import copy
import json
import logging
from builtins import str
from builtins import bytes

from baidubce.auth import bce_v1_signer
from baidubce.bce_base_client import BceBaseClient
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods
from baidubce.utils import required

_logger = logging.getLogger(__name__)


class VcaClient(BceBaseClient):
    """
    vca client
    """

    def __init__(self, config=None):
        BceBaseClient.__init__(self, config)

    @required(source=(bytes, str))
    def put_media(self, source, preset=None, notification=None, config=None):
        """
        Analyze a media.
        :param source: media source
        :type source: string or unicode
        :param preset: analyze preset name
        :type preset: string or unicode
        :param notification: notification name
        :type notification: string or unicode
        :return: **Http Response**
        """
        body = {
            'source': source
        }
        if preset is not None:
            body['preset'] = preset
        if notification is not None:
            body['notification'] = notification
        return self._send_request(http_methods.PUT, b'/v2/media',
                                  body=json.dumps(body),
                                  config=config)

    @required(source=(bytes, str))
    def get_media(self, source, config=None):
        """
        Get analyze result, make sure called put_media before calling get_media
        :param source: media source
        :type source: string or unicode
        :return: **Http Response**
        """
        return self._send_request(http_methods.GET, b'/v2/media',
                                  params={b'source': source},
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
            config=None,
            body_parser=None):
        config = self._merge_config(self, config)
        if body_parser is None:
            body_parser = handler.parse_json

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, path, body, headers, params)
