# !/usr/bin/env python
# coding=utf-8
"""
Samples for nat client.
"""

from baidubce import exception
from baidubce.services.vpc.nat_client import NatClient
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

def test_list_nat(nat_client, vpc_id=None, nat_id=None, name=None,
                  ip=None, marker=None, max_keys=None):
    """
    Return a list of nat-gateways, according to the ID,
    name or bound EIP of nat-gateways. If not specified,
    will return a full list of nat gateways in VPC.

    :param vpc_id:
        The id of VPC.
    :type vpc_id: string

    :param nat_id:
        The id of specified nat-gateway.
    :type nat_id: string

    :param name:
        The name of specified nat-gateway.
    :type name: string

    :param ip:
        The EIP associated with nat-gateway.
    :type ip: string

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
    try:
        res = nat_client.list_nats(vpc_id=vpc_id, nat_id=nat_id, name=name, ip=ip, marker=marker, max_keys=max_keys)
        nat_list  = res.nats
        return nat_list
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
    vpc_id = "vpc-xx"
    # nat list
    nat_list = test_list_nat(nat_client, vpc_id)
    print(nat_list)