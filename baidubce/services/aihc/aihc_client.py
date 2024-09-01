# Copyright 2014 Baidu, Inc.

"""
This module provides a client class for TSDB.
"""

import copy
import json
# import logging
from baidubce.auth import bce_v1_signer
from baidubce.bce_base_client import BceBaseClient
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_content_types
from baidubce.http import http_headers
from baidubce.http import http_methods
from baidubce.services.aihc import aihc_handler


# _logger = logging.getLogger(__name__)


class AIHCClient(BceBaseClient):
    """
    sdk client
    """

    def __init__(self, config=None):
        BceBaseClient.__init__(self, config)

    def create_aijob(
            self,
            client_token,
            resourcePoolId,
            payload):
        print('create_aijob is called')
        path = b"/api/v1/aijobs"
        params = {
            "clientToken": client_token,
            "resourcePoolId": resourcePoolId
            }
        body = json.dumps(payload).encode('utf-8')
        return self._send_request(http_methods.POST, path=path, body=body,
                                  params=params,
                                  body_parser=aihc_handler.parse_json)

    def delete_aijob(self, aijob_id):
        """
        delete job

        :param job_id: job id to delete
        :type job_id: string

        :return: bce_request_id
        :rtype: baidubce.bce_response.BceResponses
        """
        path = b'/api/v1/aijobs/' + aijob_id
        return self._send_request(http_methods.DELETE, path,
                                  body_parser=aihc_handler.parse_json)

    def get_aijob(self, aijob_id):
        """
        get aijob

        :param aijob_id: aijob id to delete
        :type aijob_id: string

        :return: aijob info
        :rtype: baidubce.bce_response.BceResponse
        """

        path = b'/api/v1/aijobs/' + aijob_id
        return self._send_request(http_methods.GET, path,
                                  body_parser=aihc_handler.parse_json)

    def get_all_aijobs(self, resourcePoolId):
        """
        get all aijobs

        :return: aijob dict
        :rtype: baidubce.bce_response.BceResponse
        """

        path = b'/api/v1/aijobs'
        return self._send_request(http_methods.GET, path,
                                  body_parser=aihc_handler.parse_json)

    def _merge_config(self, config):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(
            self, http_method, path,
            body=None,
            params=None,
            headers=None,
            config=None,
            body_parser=None):
        config = self._merge_config(config)
        if headers is None:
            headers = {http_headers.CONTENT_TYPE: http_content_types.JSON}
        if body_parser is None:
            body_parser = handler.parse_json
        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, path, body, headers, params)
