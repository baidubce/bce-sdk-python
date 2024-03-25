# !/usr/bin/env python
# coding=utf-8
"""
Samples for nat client.
"""

from baidubce import exception
from baidubce.services.vpc.nat_client import NatClient
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials

def test_batch_create_snat_rule(nat_client, nat_id, rules):
    """
    batch create snat rules of a specified nat gateway.

    :param nat_id:
        The id of specified nat-gateway.
    :type nat_id: string

    :param snat_rules:
        snat rules, every rule contains ruleName, sourceCIDR, privateIpsAddress.
    :type snat_rules: list<dict>

    :return:
    :rtype baidubce.bce_response.BceResponse

    Raise:
        BceHttpClientError: http request error
    """
    try:
        res = nat_client.batch_create_snat_rule(nat_id=nat_id, snat_rules=rules)
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
    nat_id = 'nat-bzawefgr3mg4'
    
    rules = [
        {
            'ruleName': 'test_snat_rule1',
            'publicIpsAddress': ["100.88.14.90"],
            'sourceCIDR': "192.168.16.0/20",
        },
        {
            'ruleName': 'test_snat_rule2',
            'publicIpsAddress': ["100.88.14.90"],
            'sourceCIDR': "192.168.1.0/24",
        }
    ]
    # create snat rule
    res = test_batch_create_snat_rule(nat_client, nat_id=nat_id, rules=rules)
    print(res.snat_rule_ids)