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
from baidubce.utils import required


class AsClient(bce_base_client.BceBaseClient):
    """
    AS base sdk client
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

    @required(group_id=str, nodes=list)
    def detach_node(self, group_id, nodes):
        """
        Detach nodes from group
        :param group_id: the id of group
        :type group_id: string
        :param nodes: the list of node
        :type nodes: list
        :return: the result of detach node
        :rtype: dict
        """
        path = b'/group/%s' % compat.convert_to_bytes(group_id)
        params = {
            "detachNode": ""
        }
        body = {
            "nodes": nodes
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body), params=params)

    @required(rule_name=str, group_id=str, state=str, rule_type=str, action_type=str, action_num=int,
              cooldown_in_sec=int)
    def create_rule(self, rule_name, group_id, state, rule_type, action_type, action_num, cooldown_in_sec,
                    target_type="", target_id="", indicator="", threshold="0", unit="",
                    comparison_operator="", cron_time="", period_type=None, period_value=None,
                    period_start_time=None, period_end_time=None):

        """
        Create rule
        :param rule_name: the name of the rule
        :type rule_name: string
        :param group_id: the id of the group
        :type group_id: string
        :param state: the state of the rule, can be "ENABLE" or "DISABLE"
        :type state: string
        :param rule_type: the type of the rule, can be "ALARM", "CRONTAB", or "PERIOD"
        :type rule_type: string
        :param target_type: the type of the target
        :type target_type: string
        :param target_id: the id of the target
        :type target_id: string
        :param indicator: the indicator of the rule
        :type indicator: string
        :param threshold: the threshold of the rule
        :type threshold: string
        :param unit: the unit of the threshold
        :type unit: string
        :param comparison_operator: the comparison operator of the rule
        :type comparison_operator: string
        :param action_type: the action type of the rule, can be INCREASE, DECREASE, ADJUST
        :type action_type: string
        :param action_num: the number of actions to be performed
        :type action_num: int
        :param cron_time: the cron time of the rule
        :type cron_time: string
        :param cooldown_in_sec: the cooldown time in seconds
        :type cooldown_in_sec: int
        :param period_type: the period type of the rule
        :type period_type: string
        :param period_value: the period value of the rule
        :type period_value: int
        :param period_start_time: the start time of the period
        :type period_start_time: string
        :param period_end_time: the end time of the period
        :type period_end_time: string
        """
        path = b'/rule'
        body = {
            "ruleName": rule_name,
            "groupId": group_id,
            "state": state,
            "type": rule_type,
            "targetType": target_type,
            "targetId": target_id,
            "indicator": indicator,
            "threshold": threshold,
            "unit": unit,
            "comparisonOperator": comparison_operator,
            "actionType": action_type,
            "actionNum": action_num,
            "cronTime": cron_time,
            "cooldownInSec": cooldown_in_sec,
            "periodType": period_type,
            "periodValue": period_value,
            "periodStartTime": period_start_time,
            "periodEndTime": period_end_time
        }
        return self._send_request(http_methods.POST, path, body=json.dumps(body))

    @required(rule_id=str, rule_name=str, group_id=str, state=str, rule_type=str, action_type=str, action_num=int,
              cooldown_in_sec=int)
    def update_rule(self, rule_id, rule_name, group_id, state, rule_type, action_type, action_num, cooldown_in_sec,
                    target_type="", target_id="", indicator="", threshold="0", unit="",
                    comparison_operator="", cron_time="", period_type=None, period_value=None,
                    period_start_time=None, period_end_time=None):
        """
        Update rule
        :param rule_id: the id of the rule
        :type rule_id: string
        :param rule_name: the name of the rule
        :type rule_name: string
        :param group_id: the id of the group
        :type group_id: string
        :param state: the state of the rule, can be "ENABLE" or "DISABLE"
        :type state: string
        :param rule_type: the type of the rule, can be "ALARM", "CRONTAB", or "PERIOD"
        :type rule_type: string
        :param target_type: the type of the target
        :type target_type: string
        :param target_id: the id of the target
        :type target_id: string
        :param indicator: the indicator of the rule
        :type indicator: string
        :param threshold: the threshold of the rule
        :type threshold: string
        :param unit: the unit of the threshold
        :type unit: string
        :param comparison_operator: the comparison operator of the rule
        :type comparison_operator: string
        :param action_type: the action type of the rule, can be INCREASE, DECREASE, ADJUST
        :type action_type: string
        :param action_num: the number of actions to be performed
        :type action_num: int
        :param cron_time: the cron time of the rule
        :type cron_time: string
        :param cooldown_in_sec: the cooldown time in seconds
        :type cooldown_in_sec: int
        :param period_type: the period type of the rule
        :type period_type: string
        :param period_value: the period value of the rule
        :type period_value: int
        :param period_start_time: the start time of the period
        :type period_start_time: string
        :param period_end_time: the end time of the period
        :type period_end_time: string
        """
        path = b'/rule/%s' % compat.convert_to_bytes(rule_id)
        body = {
            "ruleName": rule_name,
            "groupId": group_id,
            "state": state,
            "type": rule_type,
            "targetType": target_type,
            "targetId": target_id,
            "indicator": indicator,
            "threshold": threshold,
            "unit": unit,
            "comparisonOperator": comparison_operator,
            "actionType": action_type,
            "actionNum": action_num,
            "cronTime": cron_time,
            "cooldownInSec": cooldown_in_sec,
            "periodType": period_type,
            "periodValue": period_value,
            "periodStartTime": period_start_time,
            "periodEndTime": period_end_time
        }
        return self._send_request(http_methods.PUT, path, body=json.dumps(body))

    @required(rule_id=str)
    def get_rule(self, rule_id):
        """
        Get rule
        :param rule_id: the id of the rule
        :type rule_id: string
        :return: the result of get rule
        :rtype: dict
        """
        path = b'/rule/%s' % compat.convert_to_bytes(rule_id)
        return self._send_request(http_methods.GET, path)

    @required(group_id=str)
    def list_rule(self, group_id, keyword="", keyword_type="", order="desc", order_by="createTime", page_no=1,
                  page_size=1000):
        """
        Query rule list
        :param group_id: the id of the group
        :type group_id: string
        :param keyword: the keyword of the rule
        :type keyword: string
        :param keyword_type: the type of the keyword
        :type keyword_type: string
        :param order: the order of the rule
        :type order: string
        :param order_by: the order by of the rule
        :type order_by: string
        :param page_no: the page number
        :type page_no: int
        :param page_size: the page size
        :type page_size: int
        """
        path = b'/rule'
        params = {
            "groupid": group_id,
            "keyword": keyword,
            "keywordType": keyword_type,
            "order": order,
            "orderBy": order_by,
            "pageNo": page_no,
            "pageSize": page_size
        }
        return self._send_request(http_methods.GET, path, params=params)

    def delete_rule(self, rule_ids=None, group_ids=None):
        """
        Delete rule
        :param rule_ids: the list of rule id
        :type rule_ids: list
        :param group_ids: the list of group id
        :type group_ids: list
        """
        if not rule_ids and not group_ids:
            raise ValueError("rule_ids and group_ids can not be empty at the same time")
        path = b'/rule'
        params = {
            "delete": ""
        }
        body = {
            "ruleIds": rule_ids,
            "groupIds": group_ids
        }
        return self._send_request(http_methods.POST, path, params=params, body=json.dumps(body))

    def get_records(self, group_id, page_no=1, page_size=1000, order=None, order_by="startTime",
                    start_time=None, end_time=None):
        """
           Get details of a specific group
           :param group_id:
                Group identifier
           :type group_id: str

           :param page_no:
                Page number
           :type page_no: int

           :param page_size:
                Page size
           :type page_size: int

           :param order:
               Order-ascending order or descending order
           :type order: string

           :param order_by:
               Order by parameter
           :type order_by: string

           :param start_time:
               Start time for filtering the results
           :type start_time: string

           :param end_time:
               End time for filtering the results
           :type end_time: string

           :return:
           rtype baidubce.bce_response.BceResponse
       """
        params = {
            b'groupid': group_id,
            b'order': order,
            b'orderBy': order_by,
            b'pageNo': page_no,
            b'pageSize': page_size,
            b'startTime': start_time,
            b'endTime': end_time,
        }
        path = b'/record'
        return self._send_request(http_methods.GET, path, params=params)

    def exec_rule(self, group_id, rule_id):
        """
           Execute a specific rule within a group
           :param group_id:
                Group identifier
           :type group_id: str

           :param rule_id:
                Rule identifier within the group
           :type rule_id: str

           :return:
           rtype baidubce.bce_response.BceResponse
       """

        group_id = compat.convert_to_bytes(group_id)
        path = b'/group/%s' % group_id
        params = {
            b'execRule': '',
        }
        body = {
            "ruleId": rule_id
        }
        return self._send_request(http_methods.POST, path, params=params, body=json.dumps(body))

    def scaling_up(self, group_id, node_count, zone, expansion_strategy=None):
        """
            Scale up a specific group

            :param group_id:
                Group identifier
            :type group_id: str

            :param node_count:
                Number of nodes to be added
            :type node_count: int

            :param zone:
                Zone where the nodes will be added
            :type zone: str

            :param expansion_strategy:
                Strategy to be used for the expansion, optional
            :type expansion_strategy: str, optional

            :return:
            rtype baidubce.bce_response.BceResponse
        """
        group_id = compat.convert_to_bytes(group_id)
        path = b'/group/%s' % group_id
        params = {
            b'scalingUp': '',
        }
        body = {
            "nodeCount": node_count,
            "zone": zone,
            "expansionStrategy": expansion_strategy
        }
        return self._send_request(http_methods.POST, path, params=params, body=json.dumps(body))

    def scaling_down(self, group_id, nodes):
        """
            Scale down a specific group

            :param group_id:
                Group identifier
            :type group_id: str

            :param nodes:
                Nodes to be removed
            :type nodes: list or str

            :return:
            rtype baidubce.bce_response.BceResponse
        """
        group_id = compat.convert_to_bytes(group_id)
        path = b'/group/%s' % group_id
        params = {
            b'scalingDown': '',
        }
        body = {
            "nodes": nodes,
        }
        return self._send_request(http_methods.POST, path, params=params, body=json.dumps(body))

    def adjust_node(self, group_id, adjust_num):
        """
            Adjust the number of nodes in a specific group

            :param group_id:
                Group identifier
            :type group_id: str

            :param adjust_num:
                Number to adjust the nodes by. This could be positive (for adding nodes) or
                negative (for removing nodes).
            :type adjust_num: int

            :return:
            rtype baidubce.bce_response.BceResponse
        """
        group_id = compat.convert_to_bytes(group_id)
        path = b'/group/%s' % group_id
        params = {
            b'adjustNode': '',
        }
        body = {
            "adjustNum": adjust_num,
        }
        return self._send_request(http_methods.POST, path, params=params, body=json.dumps(body))

    def attach_node(self, group_id, nodes):
        """
            Attach nodes to a specific group.

            :param group_id: str
                The unique identifier of the group to which the nodes will be attached.
            :param nodes: list or str
                The nodes that will be attached to the group.
                This can be a list of node identifiers or a single node identifier.

            :return: baidubce.bce_response.BceResponse
            rtype baidubce.bce_response.BceResponse
        """
        group_id = compat.convert_to_bytes(group_id)
        path = b'/group/%s' % group_id
        params = {
            b'attachNode': '',
        }
        body = {
            "nodes": nodes,
        }
        return self._send_request(http_methods.POST, path, params=params, body=json.dumps(body))
