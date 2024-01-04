# !/usr/bin/env python
# coding=utf-8
"""
Samples for nat client.
"""

from baidubce import exception
from baidubce.services.vpc.nat_client import NatClient
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

def test_create_snat_rule(nat_client, nat_id, rule_name, source_cidr, public_ip_address):
    """
    create snat rule of a specified nat gateway.

    :param nat_id:
        The id of specified nat-gateway.
    :type nat_id: string

    :param rule_name:
        The name of snat rule.
    :type rule_name: string

    :param source_cidr:
        The source cidr of this snat rule.
    :type source_cidr: string

    :param public_ip_address:
        EIP address list to be bound
    :type eips: list<String>

    Raise:
        BceHttpClientError: http request error
    """
    try:
        res = nat_client.create_snat_rule(nat_id, rule_name, source_cidr, public_ip_address)
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
    nat_id = 'nat-xx'
    rule_name = 'test_snat_rule_create'
    source_cidr = '192.168.1.0/24'
    public_ip_address = ['100.88.14.90']
    
    res = test_create_snat_rule(nat_client, nat_id, rule_name, source_cidr, public_ip_address)
    print(res.rule_id)