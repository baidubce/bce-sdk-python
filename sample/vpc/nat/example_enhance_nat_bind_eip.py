# !/usr/bin/env python
# coding=utf-8
"""
Samples for nat client.
"""

from baidubce import exception
from baidubce.services.vpc.nat_client import NatClient
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials


def test_enhance_nat_bind_eip(nat_client, nat_id, bind_eips):
    """
    Bind EIPs to a specified enhance nat gateway.
    If a EIP is already bound to the nat gateway, unbind it first.
    If a shared_bandwidth EIP is bound to the nat gateway,
    one can bind more shared_bandwidth EIPs.

    :param nat_id:
        The id of specified enhance nat-gateway.
    :type nat_id: string

    :param bind_eips:
        A public EIP or one/more EIPs in shared-bandwidth group,
        which will be bound with the nat-gateway.
    :type bind_eips: list<String>

    :return:
    :rtype baidubce.bce_response.BceResponse

    Raise:
        BceHttpClientError: http request error
    """
    try:
        res = nat_client.enhance_nat_bind_eip(nat_id, bind_eips)
        return res
    except exception.BceHttpClientError as e:
        # 异常处理
        print(e.last_error)
        print(e.request_id)
        print(e.code)
        return None


if __name__ == "__main__":
    # create a nat client
    HOST = b''
    AK = b''
    SK = b''
    config = BceClientConfiguration(credentials=BceCredentials(AK, SK), endpoint=HOST)

    nat_client = NatClient(config)
    bind_eips = ["xxx.xxx.xxx.xxx", "xxx.xxx.xxx.xxx"]
    nat_id = "nat-xx"
    # bind EIPs to a specified nat gateway
    res = test_enhance_nat_bind_eip(nat_client, nat_id, bind_eips)
