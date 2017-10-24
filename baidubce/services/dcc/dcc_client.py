# -*- coding: utf-8 -*-

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
This module provides a client class for DCC.
"""

import copy

from baidubce import utils
from baidubce.auth import bce_v1_signer
from baidubce.bce_base_client import BceBaseClient
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods
from baidubce.utils import required


class DccClient(BceBaseClient):
    """
    Dcc base sdk client
    """
    version = '/v1'
    prefix = '/dedicatedHost'

    def __init__(self, config=None):
        """
        :type config: baidubce.BceClientConfiguration
        :param config:
        """
        BceBaseClient.__init__(self, config)

    def list_dedicated_hosts(self, zone_name=None, marker=None, max_keys=None, config=None):
        """
            Return a list of dedicatedHosts owned by the authenticated user.

            :param zone_name:
                the name of available zone
            :type zone_name: string

            :param marker:
                The optional parameter marker specified in the original request to specify
                where in the results to begin listing.
                Together with the marker, specifies the list result which listing should begin.
                If the marker is not specified, the list result will listing from the first one.
            :type marker: string

            :param max_keys:
                The optional parameter to specifies the max number of list result to return.
                The default value is 1000.
            :type max_keys: int

            :param config:
            :type config: baidubce.BceClientConfiguration

            :return: list of dedicatedHost model, for example:

            :rtype baidubce.bce_response.BceResponse
        """
        path = self._get_path()
        params = {}
        if marker is not None:
            params['marker'] = marker
        if max_keys is not None:
            params['maxKeys'] = max_keys
        if zone_name is not None:
            params['zoneName'] = zone_name

        return self._send_request(http_methods.GET, path, params=params, config=config)

    @required(host_id=(str, unicode))
    def get_dedicated_host(self, host_id, config=None):
        """
        Get the detail information of specified dedicatedHost.
        :param host_id:
            The id of dedicatedHost
        :type host_id: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return: dedicatedHost model
        :rtype baidubce.bce_response.BceResponse
        """
        path = self._get_path() + '/%s' % host_id
        return self._send_request(http_methods.GET, path, config=config)

    @staticmethod
    def _get_path(prefix=None):
        """
        :type prefix: string
        :param prefix: path prefix
        """
        if prefix is None:
            prefix = DccClient.prefix
        return utils.append_uri(DccClient.version, prefix)

    def _merge_config(self, config):
        """

        :type config: baidubce.BceClientConfiguration
        :param config:
        :return:
        """
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, path, body=None, headers=None, params=None,
                      config=None, body_parser=None):
        """

        :param http_method:
        :param path:
        :param body:
        :param headers:
        :param params:

        :type config: baidubce.BceClientConfiguration
        :param config:

        :param body_parser:

        :return: baidubce.BceResponse
        """
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json

        if headers is None:
            headers = {'Accept': '*/*', 'Content-Type': 'application/json;charset=utf-8'}

        return bce_http_client.send_request(config, bce_v1_signer.sign,
                                            [handler.parse_error, body_parser],
                                            http_method, path, body, headers, params)
