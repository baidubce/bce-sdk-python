# !/usr/bin/env python
# coding=utf-8
"""
Samples for nat client.
"""

from baidubce import exception
from baidubce.services.vpc.nat_client import NatClient
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

def test_delete_dnat_rule(nat_client, nat_id, dnat_rule_id):
    """
    delete dnat rule of a specified nat gateway.

    :param nat_id:
        The id of specified nat-gateway.
    :type nat_id: string

    :param dnat_rule_id:
    The id of specified snat rule.
    :type dnat_rule_id: string   

    :return:
    :rtype baidubce.bce_response.BceResponse

    Raise:
        BceHttpClientError: http request error
    """
    try:
        res = nat_client.delete_dnat_rule(nat_id, dnat_rule_id)
        return res
    except exception.BceHttpClientError as e:
        #异常处理
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

    nat_id = "nat-xx"

    dnat_rule_id = "rule-xx"
    
    # delete a dnat rule
    res = test_delete_dnat_rule(nat_client, nat_id, dnat_rule_id)