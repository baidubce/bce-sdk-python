"""
This module provides a client class for CA.
"""
import copy
import json
import uuid

from baidubce import bce_base_client, compat
from baidubce.auth import bce_v1_signer
from baidubce.http import handler, bce_http_client, http_methods
from baidubce.services.ca import ca_handler
from baidubce.utils import required


class CaClient(bce_base_client.BceBaseClient):
    """
    CA base sdk client
    """
    version = b'/v1'

    content_type_header_key = b"content-type"
    content_type_header_value = b"application/json;charset=UTF-8"
    request_id_header_key = b"x-bce-request-id"

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)

    def _merge_config(self, config=None):
        if config is None:
            return self.config
        else:
            new_config = copy.copy(self.config)
            new_config.merge_non_none_values(config)
            return new_config

    def _send_request(self, http_method, path,
                      body=None, headers=None, params=None, config=None, body_parser=None):
        config = self._merge_config(config)
        if body_parser is None:
            body_parser = handler.parse_json
        if headers is None:
            headers = {}
        if self.content_type_header_key not in headers:
            headers[self.content_type_header_key] = self.content_type_header_value
        if self.request_id_header_key not in headers:
            headers[self.request_id_header_key] = uuid.uuid4()

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [ca_handler.parse_error, body_parser],
            http_method, CaClient.version + path, body, headers, params)

    def batch_get_agent(self, instance_list=None):
        """
        Batch get agent info

        :param instance_list:
         Instance List
        :type instance: dict
        """
        path = b'/ca/agent/batch'
        body = {
            "hosts": instance_list
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body))

    def create_action(self, execution=None, user_id=None, action=None, targets=None,
                      parameters=None, target_selector=None, target_selector_type=None):
        """
        create execution
        :param execution:
        execution info
        :type execution: string

        :param user_id:
        user_id
        :type user_id: string

        :param action:
        action info
        :type action: dict

        :param targets:
        targets info
        :type targets:list

        :param parameters:
        parameters info
        :type parameters:dict

        :param target_selector:
        target_selector info
        :type target_selector:dict

        :param target_selector_type:
        target_selector_type info
        :type target_selector_type:string

        """
        path = b'/ca/action'
        body = {
            "execution": execution,
            "action": action,
            "targets": targets,
            "userId": user_id,
            "parameters": parameters,
            "targetSelector": target_selector,
            "targetSelectorType": target_selector_type
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body))

    def delete_action(self, id):
        """
        Delete action
        :param id: The ID of the execution to be deleted
        :type id: str
        """
        id = compat.convert_to_bytes(id)
        path = b'/ca/action/%s' % id
        return self._send_request(http_methods.DELETE, path)

    def get_action(self, id, user_id):
        """
        Query id
        :param id: The ID of the execution to be queried
        :type id: str

        Query user_id
        :param user_id: user_id
        :type user_id: str

        """
        path = b'/ca/action'
        params = {
            "userId": user_id,
            "id": id
        }
        return self._send_request(http_methods.GET, path, params=params)

    def update_action(self, action=None, execution=None):
        """
        :param action:
        action info
        :type action: dict

        :param execution
        execution info
        :type execution: string
        """
        path = b'/ca/action'
        body = {
            "action": action,
            "execution": execution,
        }
        return self._send_request(http_methods.PUT, path, body=json.dumps(body))

    def action_list(self, action=None, page_no=None, page_size=None, sort=None, ascending=None, user_id=None):
        """
        :param action:
        action info
        :type action: dict

        :param page_no:
        page number
        :type page_no: int

        :param page_size:
        page number
        :type page_size: int

        :param sort:
        sort order
        :type sort: str

        :param ascending:
        ascending order
        :type ascending: bool

        :param user_id:
        :type user_id: str
        """
        path = b'/ca/action/list'
        body = {
            "action": action,
            "pageNo": page_no,
            "pageSize": page_size,
            "sort": sort,
            "ascending": ascending,
            "userId": user_id
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body))

    def action_run(self, action=None, parameters=None, user_id=None,
                   target_selector_type=None, targets=None, target_selector=None):
        """
        :param action:
        action info
        :type action: dict

        :param parameters:
        :param target_selector_type:map

        :param user_id:
        :type user_id: str

        target selector type
        :type target_selector_type: str

        :param targets:
        :type targets: list

        :param target_selector:
        :type target_selector: dict
        """
        path = b'/ca/actionRun'
        body = {
            "action": action,
            "parameters": parameters,
            "targetSelectorType": target_selector_type,
            "targets": targets,
            "targetSelector": target_selector,
            "userId": user_id,
            "execution": "RUN"
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body))

    def get_action_run(self, id=None, user_id=None):
        """
        Query id
        :param id: The ID of the execution to be queried
        :type id: str

        user_id
        :user_id id: str
        """
        params = {
            "userId": user_id,
            "id": id
        }
        path = b'/ca/actionRun'
        return self._send_request(http_methods.GET, path, params=params)

    def action_run_list(self, action=None, page_no=None, page_size=None, sort=None, ascending=None, user_id=None,
                        start_time=None, end_time=None, keyword=None, keyword_type=None, run_id=None, is_inited=False):
        """
        :param action:
        action info
        :type action: dict

        :param page_no:
        page number
        :type page_no: int

        :param page_size:
        page number
        :type page_size: int

        :param sort:
        sort order
        :type sort: str

        :param ascending:
        ascending order
        :type ascending: bool

        :param user_id:
        :type user_id: str

        :param start_time:
        start time
        :type start_time:

        :param end_time:
        end time
        :type end_time:

        :param keyword:
        keyword type
        :type keyword: str

        :param keyword_type:
        keyword type
        :type keyword_type: str

        :param run_id:
        run id
        :type run_id: str

        :param is_inited:
        is inited or not inited
        :type is_inited: bool
        """
        body = {
            "action": action,
            "pageNo": page_no,
            "pageSize": page_size,
            "sort": sort,
            "ascending": ascending,
            "userId": user_id,
            "startTime": start_time,
            "endTime": end_time,
            "keyword": keyword,
            "keyword_type": keyword_type,
            "runId": run_id,
            "isInited": is_inited
        }
        path = b'/ca/actionRun/list'
        return self._send_request(http_methods.POST, path, body=json.dumps(body))

    def action_log(self, run_id=None, child_id=None, cursor=None):
        """
        :param run_id:
        :type run_id: str

        :param child_id:
        :type child_id: str

        :param cursor:
        :type cursor: int
        """
        body = {
            "runId": run_id,
            "childId": child_id,
            "cursor": cursor
        }
        path = b'/ca/log'
        return self._send_request(http_methods.POST, path, body=json.dumps(body))
