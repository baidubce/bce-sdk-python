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
This module provides a client class for IPv6Gateway.
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
from baidubce.services.ipv6gateway import ipv6gateway_model
from baidubce import utils
from baidubce.utils import required
from baidubce import compat

if sys.version < '3':
    reload(sys)
    sys.setdefaultencoding('utf-8')

_logger = logging.getLogger(__name__)

default_billing_to_purchase_created = ipv6gateway_model.Billing('Postpaid')
default_billing_to_purchase_reserved = ipv6gateway_model.Billing()


class IPv6GatewayClient(bce_base_client.BceBaseClient):
    """
    IPv6Gateway sdk client
    """
    version = b'/v1'

    def __init__(self, config=None):
        bce_base_client.BceBaseClient.__init__(self, config)

    def _merge_config(self, config=None):
        """
        :param config:
        :type config: baidubce.BceClientConfiguration
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

    @required(name=(bytes, str),
              vpc_id=(bytes, str),
              bandwidthInMbps=(bytes, int))
    def create_ipv6_gateway(self, name, vpc_id, bandwidthInMbps, billing=None,
                            client_token=None, config=None):
        """
        Create a ipv6-gateway with the specified options.

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
        :type client_token: string

        :param name:
            The name of ipv6-gateway that will be created.
        :type name: string

        :param vpc_id:
            The id of VPC.
        :type vpc_id: string

        :param bandwidthInMbps:
            The number of bandwidth.
        :type bandwidthInMbps: int

        :param billing:
            Billing information.
        :type billing: nat_model.Billing

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = utils.append_uri(self.version, 'IPv6Gateway')
        if client_token is None:
            client_token = generate_client_token()
        params = {b'clientToken': client_token}
        if billing is None:
            billing = default_billing_to_purchase_created
        body = {
            'name': compat.convert_to_string(name),
            'vpcId': compat.convert_to_string(vpc_id),
            'bandwidthInMbps': compat.convert_to_string(bandwidthInMbps),
            'billing': billing.__dict__
        }
        return self._send_request(http_methods.POST,
                                  path, body=json.dumps(body),
                                  params=params, config=config)

    @required(vpc_id=(bytes, str))
    def list_ipv6_gateways(self, vpc_id, config=None):
        """
        Return a list of ipv6-gateways, according to the VPC ID,
        will return a full list of ipv6 gateways in VPC.

        :param vpc_id:
            The id of VPC.
        :type vpc_id: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = utils.append_uri(self.version, 'IPv6Gateway')
        params = {b'vpcId': vpc_id}
        return self._send_request(http_methods.GET, path,
                                  params=params, config=config)

    @required(gateway_id=(bytes, str))
    def delete_ipv6_gateway(self, gateway_id, client_token=None, config=None):
        """
        delete a  specified ipv6-gateway.

        :param gateway_id:
            The id of specified ipv6-gateway.
        :type gateway_id: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by user,
            a random String generated by default algorithm will be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = utils.append_uri(self.version, 'IPv6Gateway', gateway_id)
        if client_token is None:
            client_token = generate_client_token()
        params = {
            b'clientToken': client_token
        }

        return self._send_request(http_methods.DELETE,
                                  path, params=params, config=config)

    @required(gateway_id=(bytes, str),
              bandwidthInMbps=(bytes, int))
    def resize_ipv6_gateway(self, gateway_id, bandwidthInMbps, client_token=None, config=None):
        """
        resize a specified ipv6-gateway bandwidth.

        :param gateway_id:
            The id of specified ipv6-gateway.
        :type gateway_id: string

        :param bandwidthInMbps:
            The number of bandwidth.
        :type bandwidthInMbps: int

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by user,
            a random String generated by default algorithm will be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = utils.append_uri(self.version, 'IPv6Gateway', gateway_id)
        if client_token is None:
            client_token = generate_client_token()
        params = {
            b'resize': None,
            b'clientToken': client_token
        }
        body = {
            'bandwidthInMbps': compat.convert_to_string(bandwidthInMbps)
        }

        return self._send_request(http_methods.PUT,
                                  path, body=json.dumps(body), params=params, config=config)

    @required(gateway_id=(bytes, str),
              cidr=(bytes, str))
    def create_ipv6_gateway_egress_only_rule(self, gateway_id, cidr,
                                             client_token=None, config=None):
        """
        Create a ipv6-gateway egress only rule with the specified options.

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
        :type client_token: string

        :param gateway_id:
            The id of ipv6 gateway.
        :type gateway_id: string

        :param cidr:
            The cidr of egress only rule.
        :type cidr: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = utils.append_uri(self.version, 'IPv6Gateway', gateway_id, 'egressOnlyRule')
        if client_token is None:
            client_token = generate_client_token()
        params = {b'clientToken': client_token}
        body = {
            'cidr': compat.convert_to_string(cidr),
        }
        return self._send_request(http_methods.POST,
                                  path, body=json.dumps(body),
                                  params=params, config=config)

    @required(gateway_id=(bytes, str))
    def list_ipv6_gateway_egress_only_rules(self, gateway_id, marker=None, max_keys=None, config=None):
        """
        Return a list of ipv6-gateway egress only rules, according to the ipv6 gateway ID,
        will return a full list of ipv6 gateway egress only rules in ipv6 gateway.

        :param gateway_id:
            The id of ipv6 gateway.
        :type gateway_id: string

        :param marker:
            The optional parameter marker specified in the original
            request to specify where in the results to begin listing.
            Together with the marker, specifies the list result which
            listing should begin. If the marker is not specified,
            the list result will listing from the first one.
        :type marker: string

        :param max_keys:
            The optional parameter to specifies the max number of list
            result to return.
            The default value is 1000.
        :type max_keys: int

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = utils.append_uri(self.version, 'IPv6Gateway', gateway_id, 'egressOnlyRule')
        params = {}
        if marker is not None:
            params[b'marker'] = marker
        if max_keys is not None:
            params[b'maxKeys'] = max_keys
        return self._send_request(http_methods.GET, path,
                                  params=params, config=config)

    @required(gateway_id=(bytes, str),
              egress_only_rule_id=(bytes, str))
    def delete_ipv6_gateway_egress_only_rule(self, gateway_id, egress_only_rule_id, client_token=None, config=None):
        """
        delete a  specified ipv6-gateway egress only rule.

        :param gateway_id:
            The id of specified ipv6-gateway.
        :type gateway_id: string

        :param egress_only_rule_id:
            The id of specified ipv6-gateway egress only rule.
        :type egress_only_rule_id: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by user,
            a random String generated by default algorithm will be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = utils.append_uri(self.version, 'IPv6Gateway', gateway_id, 'egressOnlyRule', egress_only_rule_id)
        if client_token is None:
            client_token = generate_client_token()
        params = {
            b'clientToken': client_token
        }

        return self._send_request(http_methods.DELETE,
                                  path, params=params, config=config)

    @required(gateway_id=(bytes, str),
              ipv6_address=(bytes, str),
              ingress_bandwidthInMbps=(bytes, int),
              egress_bandwidthInMbps=(bytes, int))
    def create_ipv6_gateway_rate_limit_rule(self, gateway_id, ipv6_address,
                                            ingress_bandwidthInMbps, egress_bandwidthInMbps,
                                            client_token=None, config=None):
        """
        Create a ipv6-gateway rate limit rule with the specified options.

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if client token is provided.
        :type client_token: string

        :param gateway_id:
            The id of ipv6 gateway.
        :type gateway_id: string

        :param ipv6_address:
            The ipv6 addrss of rate limit rule.
        :type ipv6_address: string

        :param ingress_bandwidthInMbps:
            The ingress bandwidth of rate limit rule.
        :type ingress_bandwidthInMbps: int

        :param egress_bandwidthInMbps:
            The egress bandwidth of rate limit rule.
        :type egress_bandwidthInMbps: int

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = utils.append_uri(self.version, 'IPv6Gateway', gateway_id, 'rateLimitRule')
        if client_token is None:
            client_token = generate_client_token()
        params = {b'clientToken': client_token}
        body = {
            'ipv6Address': compat.convert_to_string(ipv6_address),
            'ingressBandwidthInMbps': compat.convert_to_string(ingress_bandwidthInMbps),
            'egressBandwidthInMbps': compat.convert_to_string(egress_bandwidthInMbps),
        }
        return self._send_request(http_methods.POST,
                                  path, body=json.dumps(body),
                                  params=params, config=config)

    @required(gateway_id=(bytes, str))
    def list_ipv6_gateway_rate_limit_rules(self, gateway_id, marker=None, max_keys=None, config=None):
        """
        Return a list of ipv6-gateway rate limit rules, according to the ipv6 gateway ID,
        will return a full list of ipv6 gateway rate limit rules in ipv6 gateway.

        :param gateway_id:
            The id of ipv6 gateway.
        :type gateway_id: string

        :param marker:
            The optional parameter marker specified in the original
            request to specify where in the results to begin listing.
            Together with the marker, specifies the list result which
            listing should begin. If the marker is not specified,
            the list result will listing from the first one.
        :type marker: string

        :param max_keys:
            The optional parameter to specifies the max number of list
            result to return.
            The default value is 1000.
        :type max_keys: int

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = utils.append_uri(self.version, 'IPv6Gateway', gateway_id, 'rateLimitRule')
        params = {}
        if marker is not None:
            params[b'marker'] = marker
        if max_keys is not None:
            params[b'maxKeys'] = max_keys
        return self._send_request(http_methods.GET, path,
                                  params=params, config=config)

    @required(gateway_id=(bytes, str),
              rate_limit_rule_id=(bytes, str))
    def delete_ipv6_gateway_rate_limit_rule(self, gateway_id, rate_limit_rule_id, client_token=None, config=None):
        """
        delete a  specified ipv6-gateway rate limit rule.

        :param gateway_id:
            The id of specified ipv6-gateway.
        :type gateway_id: string

        :param rate_limit_rule_id:
            The id of specified ipv6-gateway rate limit rule.
        :type rate_limit_rule_id: string

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by user,
            a random String generated by default algorithm will be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = utils.append_uri(self.version, 'IPv6Gateway', gateway_id, 'rateLimitRule', rate_limit_rule_id)
        if client_token is None:
            client_token = generate_client_token()
        params = {
            b'clientToken': client_token
        }

        return self._send_request(http_methods.DELETE,
                                  path, params=params, config=config)

    @required(gateway_id=(bytes, str),
              rate_limit_rule_id=(bytes, str),
              ingress_bandwidthInMbps=(bytes, int),
              egress_bandwidthInMbps=(bytes, int))
    def update_ipv6_gateway_rate_limit_rule(self, gateway_id, rate_limit_rule_id,
                                            ingress_bandwidthInMbps, egress_bandwidthInMbps,
                                            client_token=None, config=None):
        """
        update a  specified ipv6-gateway rate limit rule.

        :param gateway_id:
            The id of specified ipv6-gateway.
        :type gateway_id: string

        :param rate_limit_rule_id:
            The id of specified ipv6-gateway rate limit rule.
        :type rate_limit_rule_id: string

        :param ingress_bandwidthInMbps:
            The ingress bandwidth of rate limit rule.
        :type ingress_bandwidthInMbps: int

        :param egress_bandwidthInMbps:
            The egress bandwidth of rate limit rule.
        :type egress_bandwidthInMbps: int

        :param client_token:
            An ASCII string whose length is less than 64.
            The request will be idempotent if clientToken is provided.
            If the clientToken is not specified by user,
            a random String generated by default algorithm will be used.
        :type client_token: string

        :param config:
        :type config: baidubce.BceClientConfiguration

        :return:
        :rtype baidubce.bce_response.BceResponse
        """
        path = utils.append_uri(self.version, 'IPv6Gateway', gateway_id, 'rateLimitRule', rate_limit_rule_id)
        if client_token is None:
            client_token = generate_client_token()
        params = {
            b'clientToken': client_token
        }
        body = {
            'ingressBandwidthInMbps': compat.convert_to_string(ingress_bandwidthInMbps),
            'egressBandwidthInMbps': compat.convert_to_string(egress_bandwidthInMbps),
        }

        return self._send_request(http_methods.PUT,
                                  path, body=json.dumps(body),
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
