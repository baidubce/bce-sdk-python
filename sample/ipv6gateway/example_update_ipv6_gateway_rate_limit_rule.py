# !/usr/bin/env python
# coding=utf-8
"""
Samples for ipv6gateway client.
"""
import uuid

from baidubce import exception
from baidubce.services.ipv6gateway.ipv6gateway_client import IPv6GatewayClient
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials


def test_update_ipv6_gateway_rate_limit_rule(ipv6gateway_client, gateway_id, rate_limit_rule_id,
                                             ingress_bandwidthInMbps, egress_bandwidthInMbps):
    """
    delete ipv6 gateway rate limit rule.

    :param gateway_id:
        the ID of the ipv6 gateway.
    :type gateway_id: string

    :param rate_limit_rule_id:
        the ID of the ipv6 gateway rate limit rule.
    :type rate_limit_rule_id: string

     :param ingress_bandwidthInMbps:
        The ingress bandwidth of rate limit rule.
    :type ingress_bandwidthInMbps: int

    :param egress_bandwidthInMbps:
        The egress bandwidth of rate limit rule.
    :type egress_bandwidthInMbps: int

    :return:
    :rtype baidubce.bce_response.BceResponse

    Raise:
        BceHttpClientError: http request error
    """
    try:
        res = ipv6gateway_client.update_ipv6_gateway_rate_limit_rule(gateway_id, rate_limit_rule_id,
                                                                     ingress_bandwidthInMbps, egress_bandwidthInMbps)
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
    rate_limit_rule_id = b'ipv6_qos-xx'

    res = test_update_ipv6_gateway_rate_limit_rule(ipv6gateway_client, gateway_id, rate_limit_rule_id,
                                                   ingress_bandwidthInMbps=5, egress_bandwidthInMbps=5)
