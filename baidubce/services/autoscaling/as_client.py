"""
This module provides a client class for AS.
"""
import copy
import json
import uuid

from baidubce import bce_base_client, compat
from baidubce.auth import bce_v1_signer
from baidubce.http import handler, bce_http_client, http_methods
from baidubce.services.autoscaling import as_handler


class AsClient(bce_base_client.BceBaseClient):
    """
    AS base sdk client
    """
    version = b'/v1'

    content_type_header_key = b"content-type"
    content_type_header_value = b"application/json;charset=utf-8"
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
            config, bce_v1_signer.sign, [as_handler.parse_error, body_parser],
            http_method, AsClient.version + path, body, headers, params)

    def get_as_group_list(self, page_no=1, page_size=1000, keyword=None, keyword_type=None, order=None, order_by=None):
        """
            Get autoscaling group list
            :param page_no:
                 page_no
            :type page_no: int

            :param keyword:
                query keyword
            :type keyword: string

            :param keyword_type:
                query keyword type
            :type keyword_type: string

            :param order:
                order-ascending order or descending order
            :type order: string

            :param order_by:
                order by param
            :type order_by:

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        params = {
            b'keyword': keyword,
            b'keywordType': keyword_type,
            b'order': order,
            b'orderBy': order_by,
            b'pageNo': page_no,
            b'pageSize': page_size,
        }
        path = b'/group'
        return self._send_request(http_methods.GET, path, params=params)

    def get_as_group_detail(self, group_id):
        """
            Get autoscaling group detail
            :param group_id:
                autoscaling group_id
            :type group_id: string
            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(group_id) <= 0:
            raise ValueError('group_id should not be none or empty string')
        group_id = compat.convert_to_bytes(group_id)
        path = b'/group/%s' % group_id
        return self._send_request(http_methods.GET, path)

    def get_as_group_node_list(self, group_id, page_no=1, page_size=1000, keyword=None, keyword_type=None, order=None,
                               order_by=None):
        """
            Get autoscaling group node list

            :param group_id:
                autoscaling group_id
            :type group_id: string

            :param page_no:
                 page_no
            :type page_no: int

            :param keyword:
                query keyword
            :type keyword: string

            :param keyword_type:
                query keyword type
            :type keyword_type: string

            :param order:
                order-ascending order or descending order
            :type order: string

            :param order_by:
                order by param
            :type order_by:

            :return:
            :rtype baidubce.bce_response.BceResponse
        """
        if len(group_id) <= 0:
            raise ValueError('group_id should not be none or empty string')
        params = {
            b'groupid': group_id,
            b'keyword': keyword,
            b'keywordType': keyword_type,
            b'order': order,
            b'orderBy': order_by,
            b'pageNo': page_no,
            b'pageSize': page_size,
        }
        path = b'/node'
        return self._send_request(http_methods.GET, path, params=params)

    def delete_group(self, group_ids):
        """
            Get autoscaling group node list

            :param group_ids:
                autoscaling group_ids
            :type group_ids: list of strings
        """
        if len(group_ids) <= 0:
            raise ValueError('group_id should not be none or empty string')
        path = b'/group/delete'
        body = {
            "groupIds": group_ids
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body))

    def create_group(self, group_name=None, config=None, health_check=None, blb=None, rds=None, scs=None,
                     shrinkage_strategy=None, zone_infos=None, assign_tag_info=None, node_list=None,
                     eip=None, billing=None, cmd_config=None, bcc_name_config=None):
        """
            Create autoscaling group

            :param group_name:
                autoscaling group_name
            :type group_name: string

            :param config:
                 autoscaling group config
            :type config: dict

            :param health_check:
                autoscaling group health check info
            :type health_check: dict

            :param blb:
                blb info
            :type blb: list of strings

            :param rds:
                rds info
            :type rds: list of strings

            :param scs:
                scs info
            :type scs: list of strings

            :param shrinkage_strategy:
                autoscaling group shrinkage strategy
            :type shrinkage_strategy: string

            :param zone_info:
                autoscaling group zone info
            :type zone_info: dict

            :param assign_tag_info:
                autoscaling group tag info
            :type assign_tag_info: dict

            :param nodes:
                autoscaling group nodes
            :type nodes: dict

            :param eip:
                autoscaling group eip info
            :type eip: dict

            :param billing:
                autoscaling group billing info
            :type billing: dict

            :param cmd_config:
                autoscaling group cmd config
            :type cmd_config: dict

            :param bcc_name_config:
                autoscaling group bcc name config
            :type bcc_name_config: dict

            :return:
            :rtype baidubce.bce_response.BceResponse
        """

        path = b'/group'
        body = {
            'groupName': group_name,
            'config': config,
            'healthCheck': health_check,
            'blb': blb,
            'rds': rds,
            'scs': scs,
            'shrinkageStrategy': shrinkage_strategy,
            'zoneInfo': zone_infos,
            'assignTagInfo': assign_tag_info,
            'nodes': node_list,
            'eip': eip,
            'billing': billing,
            'cmdConfig': cmd_config,
            'bccNameConfig': bcc_name_config
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body))
