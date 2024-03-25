# !/usr/bin/env python
# coding=utf-8
"""
Samples for ipv6 gateway client.
"""

from baidubce import exception
from baidubce.services.ipv6gateway.ipv6gateway_client import IPv6GatewayClient
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials


def test_list_ipv6_gateway_egress_only_rule(ipv6gateway_client, gateway_id, marker=None, max_keys=None):
    """
    Return a list of ipv6-gateway egress only rules.

    :param gateway_id:
        the ID of the ipv6 gateway.
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

    :return:
    :rtype baidubce.bce_response.BceResponse
    """
    try:
        res = ipv6gateway_client.list_ipv6_gateway_egress_only_rules(gateway_id, marker=marker, max_keys=max_keys)
        return res
    except exception.BceHttpClientError as e:
        # 异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None


if __name__ == "__main__":
    # create a ipv6 gateway client
    HOST = b''
    AK = b''
    SK = b''
    config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)

    ipv6gateway_client = IPv6GatewayClient(config)
    gateway_id = b'ipv6-xx'
    # ipv6 gateway list
    ipv6gateway_egress_only_rule_list = test_list_ipv6_gateway_egress_only_rule(ipv6gateway_client, gateway_id)
    print(ipv6gateway_egress_only_rule_list)