# !/usr/bin/env python
# coding=utf-8
"""
Samples for nat client.
"""

from baidubce import exception
from baidubce.services.vpc.nat_client import NatClient
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

def test_update_nat(nat_client, nat_id, name):
    """
    Update the name of a specified nat-gateway.

    :param nat_id:
        The id of specified nat-gateway.
    :type nat_id: string

    :param name:
        The new name of the nat-gateway
    :type name: string

    :return:
    :rtype baidubce.bce_response.BceResponse

    Raise:
        BceHttpClientError: http request error
    """
    try:
        res = nat_client.update_nat(nat_id, name)
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
    
    res = test_update_nat(nat_client, nat_id, "new_name_of_nat")
