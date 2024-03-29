# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.

"""
This module provides a client class for ACL.
"""

import copy
import json
import logging
import uuid
import sys

from baidubce import bce_base_client
from baidubce.auth import bce_v1_signer
from baidubce.http import bce_http_client
from baidubce.http import handler
from baidubce.http import http_methods
from baidubce import utils
from baidubce.utils import required
from baidubce import compat

if sys.version < '3':
    reload(sys)
    sys.setdefaultencoding('utf-8')

_logger = logging.getLogger(__name__)


class AclClient(bce_base_client.BceBaseClient):
    """
    ACL base sdk client
    """
    prefix = b'/v1'

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)

    def _merge_config(self, config=None):
        """
        :param config:
        :type config: baidubce.BceClientConfiguration
        :return:
        """
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
        if headers is None:
            headers = {b'Accept': b'*/*', b'Content-Type':
                b'application/json;charset=utf-8'}

        return bce_http_client.send_request(
            config, bce_v1_signer.sign, [handler.parse_error, body_parser],
            http_method, path, body, headers, params)

    @required(vpc_id=(bytes, str))
    def list_acl_entrys(self, vpc_id, config=None):
        """
        Get the detail information of acl for specific vpc.

        :param vpc_id:
            the vpc id
        :type vpc_id: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = utils.append_uri(self.prefix, 'acl')
        params = {}
        params[b'vpcId'] = vpc_id

        return self._send_request(http_methods.GET, path,
                                  params=params, config=config)

    @required(rule_list=list)
    def create_acl(self, rule_list, client_token=None, config=None):
        """
        Create  acl rules with the specified options.

        :param rule_list:
                a list contains acl rules.
                https://cloud.baidu.com/doc/VPC/API.html#AclRuleRequest
                The elements of the list are AclRuleRequest
        :type rule_list: list

        AclRuleRequest{
            :param subnetId:
                The subnet id which the acl rule applied to
            :type subnetId: string

            :param protocol:
                The parameter specify which protocol will the acl rule work on
            :value: "all" or ""tcp" or "udp" or "icmp"
            :type protocol: string

            :param sourceIpAddress:
                Source ip address which the rule applied to
            :type sourceIpAddress: string

            :param destinationIpAddress:
                Destination ip address which the rule applied to
            :type destinationIpAddress: string

            :param sourcePort:
                Port used by source ip address
            :value 1-65535
            :type sourcePort: string

            :param destinationPort:
                Port used by destination ip address
            :value 1-65535
            :type destinationPort:string

            :param position:
                Priority of the rule
            :value 1-5000,unique,The smaller the value, the higher the priority
            :type:position:Integer

            :param direction:
                The rule is a ingress or a egress rule
            :value: "ingress" or "egress"
            :type direction:string

            :param action:
                The rule is allowed or denied
            :value "allow" or "deny"
            :type action:string

            :param description(Optional):
                The option param to describe the acl rule.
            :type description: string
        }

        :param client_token:
            If the clientToken is not specified by the user,
            a random Stringgenerated by default algorithm will be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = utils.append_uri(self.prefix, 'acl', 'rule')
        params = {}

        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        body = {
            'aclRules': rule_list
        }

        return self._send_request(http_methods.POST, path,
                                  body=json.dumps(body), params=params,
                                  config=config)

    @required(subnet_id=(bytes, str))
    def list_subnet_acl(self, subnet_id, marker=None, max_keys=None, config=None):
        """
        Return a list of acl rules of specify subnet.

        :param subnet_id
            the id of subnet whhich the acl applied
        :type subnet_id: string

        :param marker
            The optional parameter marker specified in the original
            request to specify where in the results to begin listing.
            Together with the marker, specifies the list result
            which listing should begin. If the marker is not specified,
            the list result will listing from the first one.
        :type marker: string

        :param max_keys
            The optional parameter to specifies the max number of
            list result to return.
            The default value is 1000.
        :type max_keys: int

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
         """
        path = utils.append_uri(self.prefix, 'acl', 'rule')
        params = {}

        if marker is not None:
            params[b'marker'] = marker
        if max_keys is not None:
            params[b'maxKeys'] = max_keys

        params[b'subnetId'] = subnet_id
        return self._send_request(http_methods.GET, path,
                                  params=params, config=config)

    @required(acl_rule_id=(bytes, str))
    def delete_acl(self, acl_rule_id, client_token=None, config=None):
        """
        Delete the  specific acl rule.

        :param acl_rule_id:
            The id of the specified acl.
        :type acl_rule_id: string

        :param client_token:
            If the clientToken is not specified by the user, a random String
            generated by default algorithm will be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = utils.append_uri(self.prefix, 'acl', 'rule', acl_rule_id)
        params = {}
        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token
        return self._send_request(http_methods.DELETE, path,
                                  params=params, config=config)

    @required(acl_rule_id=(bytes, str))
    def update_acl(self, acl_rule_id, description=None,
                   protocol=None, source_ip_address=None,
                   destination_ip_address=None, source_port=None,
                   destination_port=None,
                   position=None, action=None,
                   client_token=None, config=None):
        """
        Modify the special attribute to new value of the acl owned by the user.

        :param acl_rule_id
                id of the acl to be modified
        :type acl_rule_id:string

        :param description:
                The option param to describe the acl rule.
        :type description: string

        :param protocol:
                 The parameter specify which protocol will the acl rule work on
        :value: "all" or ""tcp" or "udp" or "icmp"
        :type protocol: string

        :param source_ip_address:
                 source ip address which the rule applied to
        :type source_ip_address: string

        :param destination_ip_address:
                 destination ip address which the rule applied to
        :type destination_ip_address: string

        :param source_port:
                 port used by source ip address
        :value 1-65535
        :type source_port: string

        :param destination_port:
                 port used by destination ip address
        :value 1-65535
        :type destination_port:string

        :param position:
                 priority of the rule
        :value 1-5000,unique,The smaller the value, the higher the priority
        :type:position:Integer

        :param action:
                the rule is allowed or denied
        :value "allow" or "deny"
        :type action:string

        :param client_token:
                If the clientToken is not specified by the user, a random
                String generated by default algorithm will be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = utils.append_uri(self.prefix, 'acl', 'rule', acl_rule_id)
        params = {}

        if client_token is None:
            params[b'clientToken'] = generate_client_token()
        else:
            params[b'clientToken'] = client_token

        body = {}
        if description is not None:
            body['description'] = compat.convert_to_string(description)

        if protocol is not None:
            body['protocol'] = compat.convert_to_string(protocol)

        if source_ip_address is not None:
            body['sourceIpAddress'] = \
                compat.convert_to_string(source_ip_address)

        if destination_ip_address is not None:
            body['destinationIpAddress'] = \
                compat.convert_to_string(destination_ip_address)

        if source_port is not None:
            body['sourcePort'] = compat.convert_to_string(source_port)

        if destination_port is not None:
            body['destinationPort'] = \
                compat.convert_to_string(destination_port)

        if position is not None:
            body['position'] = position

        if action is not None:
            body['action'] = compat.convert_to_string(action)

        return self._send_request(http_methods.PUT, path, json.dumps(body),
                                  params=params, config=config)


def generate_client_token_by_uuid():
    """
    The default method to generate the random string for client_token
    if the optional parameter client_token is not specified by the user.

    :return:
    :rtype string
    """
    return str(uuid.uuid4())


generate_client_token = generate_client_token_by_uuid
