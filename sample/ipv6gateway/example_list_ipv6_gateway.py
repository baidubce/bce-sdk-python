# !/usr/bin/env python
# coding=utf-8
"""
Samples for ipv6 gateway client.
"""

from baidubce import exception
from baidubce.services.ipv6gateway.ipv6gateway_client import IPv6GatewayClient
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials


def test_list_ipv6_gateway(ipv6gateway_client, vpc_id):
    """
    Return a list of ipv6-gateways, according to the vpc id of ipv6_gateways.

    :param vpc_id:
        The id of VPC.
    :type vpc_id: string

    :return:
    :rtype baidubce.bce_response.BceResponse
    """
    try:
        res = ipv6gateway_client.list_ipv6_gateways(vpc_id=vpc_id)
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
    vpc_id = "vpc-xx"
    # ipv6 gateway list
    ipv6gateway_list = test_list_ipv6_gateway(ipv6gateway_client, vpc_id)
    print(ipv6gateway_list)