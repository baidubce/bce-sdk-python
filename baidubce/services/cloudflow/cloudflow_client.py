"""
This module provides a client class for BOS CloudFlow.
"""

import copy
import logging

from baidubce.bce_base_client import BceBaseClient
from baidubce.auth import bce_v1_signer
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods
from baidubce.http import http_content_types
from baidubce.http import http_headers
from baidubce.utils import required
from baidubce.services.cloudflow import cloudflow_model as cfm


_logger = logging.getLogger(__name__)


class CloudFlowClient(BceBaseClient):
    """
    sdk client
    """
    path = b'/v1/'

    


    def __init__(self, config=None):
        BceBaseClient.__init__(self, config)

    def _merge_config(self, config):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    

    @staticmethod
    def _bce_cloudflow_sign(credentials, http_method, path, headers, params,
                           timestamp=0, expiration_in_seconds=1800,
                           headers_to_sign=None):
        """
        CloudFlow API signature adaptation method
        """
        headers_to_sign_list = [b"host", b"content-md5",
                                b"content-length", b"content-type"]

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


    def _send_request(self, http_method, params=None, body=None, headers=None,
                       config=None, body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json

        if headers is None:
            headers = {http_headers.CONTENT_TYPE: b'application/json'}

        path = CloudFlowClient.path

        return bce_http_client.send_request(config, self._bce_cloudflow_sign,
            [handler.parse_error, body_parser], http_method, path, body, headers, params)


    @required(create_task_info=(cfm.CreateTaskInfo))
    def create_migration(self, create_task_info, config=None):
        """
        create migration task
        """
        body = create_task_info.to_json_string()
        params = {
            cfm.MigrationInterface.POSTMIGRATION: None
        }
        return self._send_request(http_methods.POST, params=params,
                                  body=body, config=config)

    @required(create_task_list_info=(cfm.CreateTaskListInfo))
    def create_migration_from_list(self, create_task_list_info, config=None):
        """
        create migration task from list
        """
        body = create_task_list_info.to_json_string()
        params = {
            cfm.MigrationInterface.POSTMIGRATIONFROMLIST: None
        }
        return self._send_request(http_methods.POST, params=params,
                                  body=body, config=config)

    @required(task_id=(str))
    def get_migration(self, task_id, config=None):
        """
        get migration task
        """
        params = {
            cfm.MigrationInterface.GETMIGRATION: None,
            b'taskId': task_id
        }
        return self._send_request(http_methods.GET, params=params, config=config)

    def list_migration(self, config=None):
        """
        list migration task
        """
        params = {
            cfm.MigrationInterface.LISTMIGRATION: None
        }
        return self._send_request(http_methods.GET, params=params, config=config)

    @required(task_id=(str))
    def get_migration_result(self, task_id, config=None):
        """
        get migration task result
        """
        params = {
            cfm.MigrationInterface.GETMIGRATIONRESULT: None,
            b'taskId': task_id
        }
        return self._send_request(http_methods.GET, params=params, config=config)

    @required(task_id=(str))
    def pause_migration(self, task_id, config=None):
        """
        pause migration task
        """
        params = {
            cfm.MigrationInterface.PAUSEMIGRATION: None,
            b'taskId': task_id
        }
        return self._send_request(http_methods.POST, params=params, config=config)

    @required(task_id=(str))
    def resume_migration(self, task_id, config=None):
        """
        resume migration task
        """
        params = {
            cfm.MigrationInterface.RESUMEMIGRATION: None,
            b'taskId': task_id
        }
        return self._send_request(http_methods.POST, params=params, config=config)

    @required(task_id=(str))
    def retry_migration(self, task_id, config=None):
        """
        retry migration task
        """
        params = {
            cfm.MigrationInterface.RETRYMIGRATION: None,
            b'taskId': task_id
        }
        return self._send_request(http_methods.POST, params=params, config=config)

    @required(task_id=(str))
    def delete_migration(self, task_id, config=None):
        """
        delete migration task
        """
        params = {
            cfm.MigrationInterface.DELETEMIGRATION: None,
            b'taskId': task_id
        }
        return self._send_request(http_methods.DELETE, params=params, config=config)
