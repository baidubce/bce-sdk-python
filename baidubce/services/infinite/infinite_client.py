#! usr/bin/python
# coding=utf-8

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
This module provides a client class for infinite.
"""

import copy
import logging
import warnings

import baidubce
from baidubce import utils
from baidubce.auth import bce_v1_signer
from baidubce.bce_base_client import BceBaseClient
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_headers
from baidubce.http import http_content_types
from baidubce.http import http_methods
from baidubce.utils import required
from baidubce.services import infinite
import httplib
from baidubce.exception import BceClientError
from baidubce.exception import BceServerError
from baidubce.bce_client_configuration import BceClientConfiguration
import uuid

_logger = logging.getLogger(__name__)

def _parse_http_response(http_response, response):
    if http_response.status / 100 == httplib.CONTINUE / 100:
        raise BceClientError('Can not handle 1xx http status code')
    if http_response.status / 100 == httplib.OK / 100:
        body = http_response.read()
        if body:
            response.__dict__.update({'Body': body})
        http_response.close()
        return True
    bse = BceServerError(http_response.reason, request_id=response.metadata.bce_request_id)
    bse.status_code = http_response.status
    http_response.close()
    raise bse


class InfiniteClient(BceBaseClient):
    """
    Infinite sdk client
    """
    def __init__(self, config=None):
        BceBaseClient.__init__(self, config)

    def predict(self, endpoint_name, body,
            variant_name=None, content_type='application/json', config=None):
        """
        predict
        
        :param endpoint_name: endpoint name
        :type endpoint_name: string
        
        :param body: request data
        :type body: binary string or dict
        
        :param variant_name: variant name or None
        :type variant_name: string
        
        :param content_type: content type,supports application/json,x-image,and x-recordio-protobuf
        :type content_type: string
        
        :param config: None
        :type config: BceClientConfiguration

        :return: response as following format
            {
                Body: 'predict result'
            }
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {}
        if variant_name is not None:
            params['variant'] = variant_name
        params['action'] = 'predict'

        default_encoding = baidubce.DEFAULT_ENCODING
        content_type = content_type + '; charset=' + default_encoding
        headers = {
            http_headers.CONTENT_TYPE: content_type,
            http_headers.BCE_REQUEST_ID: uuid.uuid4()
        }

        return self._send_request(
                http_method=http_methods.POST,
                function_name=endpoint_name + '/invocations',
                body=body,
                headers=headers,
                params=params,
                config=config)
        
    def debug(self, endpoint_name, body, variant_name=None,
            content_type='application/json', config=None):
        """
        debug
        
        :param endpoint_name: endpoint name
        :type endpoint_name: string
        
        :param body: request data
        :type body: binary or dict
        
        :param variant_name: variant name or None
        :type variant_name: string
        
        :param content_type: content type,supports application/json,x-image,and x-recordio-protobuf
        :type content_type: string
        
        :param config: None
        :type config: BceClientConfiguration

        :return: response as following format
            {
                Body: 'debug info'
            }
        :rtype: baidubce.bce_response.BceResponse
        """
        params = {}
        if variant_name is not None:
            params['variant'] = variant_name
        params['action'] = 'debug'
        
        default_encoding = baidubce.DEFAULT_ENCODING
        content_type = content_type + '; charset=' + default_encoding
        headers = {
            http_headers.CONTENT_TYPE: content_type,
            http_headers.BCE_REQUEST_ID: uuid.uuid4()
        }

        return self._send_request(
                http_method=http_methods.POST,
                function_name=endpoint_name + '/invocations',
                body=body,
                headers=headers,
                params=params,
                config=config)

    def get_endpoint_list(self, config=None):
        """
        get all endpoint
        
        :param config: None
        :type config: BceClientConfiguration

        :return: response as following format
            {
                Body: '{"endpointList":["ep1_name","ep2_name"]}'
            }
        :rtype: baidubce.bce_response.BceResponse
        """
        headers = {
            http_headers.CONTENT_TYPE: http_content_types.JSON,
            http_headers.BCE_REQUEST_ID: uuid.uuid4()
        }
        return self._send_request(
                http_method=http_methods.GET,
                function_name='list',
                headers=headers,
                config=config)

    def get_endpoint_info(self, endpoint_name, config=None):
        """
        get endpoint info
        
        :param endpoint_name: endpoint name
        :type endpoint_name: string
        
        :param config: None
        :type config: BceClientConfiguration

        :return: response as following format
            {
                Body: '{
                    "endpoint_uuid":"ep1",
                    "variant_configs":[
                        {
                            "variant_uuid":"v1",
                            "variant_name":"v1_name",
                            "...":"..."
                        }
                    ]
                }'
            }
        :rtype: baidubce.bce_response.BceResponse
        """
        headers = {
            http_headers.CONTENT_TYPE: http_content_types.JSON,
            http_headers.BCE_REQUEST_ID: uuid.uuid4()
        }
        return self._send_request(
                http_method=http_methods.GET,
                function_name=endpoint_name + '/info',
                headers=headers,
                config=config)
    
    @staticmethod
    def _get_path(config, function_name=None):
        return utils.append_uri(infinite.URL_PREFIX, function_name)

    def _merge_config(self, config):
        if config is None:
            return self.config
        else:
            self._check_config_type(config)
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(
            self, http_method, function_name=None,
            body=None, headers=None, params=None,
            config=None,
            body_parser=None):
        config = self._merge_config(config)
        path = InfiniteClient._get_path(config, function_name)
        if body_parser is None:
            body_parser = _parse_http_response
        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [body_parser],
            http_method, path, body, headers, params)
