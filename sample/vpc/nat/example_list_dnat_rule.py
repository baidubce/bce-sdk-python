# !/usr/bin/env python
# coding=utf-8
"""
Samples for nat client.
"""

from baidubce import exception
from baidubce.services.vpc.nat_client import NatClient
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

def test_list_dnat_rule(nat_client, nat_id, marker=None, maxKeys=None):
    """
    listing dnat rule of a specified nat gateway.

    :param nat_id:
        The id of specified nat-gateway.
    :type nat_id: string

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

    Raise:
        BceHttpClientError: http request error
    """
    try:
        res = nat_client.list_dnat_rule(nat_id, marker, maxKeys)
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
    
    res = test_list_dnat_rule(nat_client, nat_id, maxKeys=10)
    print(res.rules)